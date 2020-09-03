#!/usr/bin/python
# -*- coding: utf-8 -*-


from resources import DEFAULT_DECK_NA, DEFAULT_BET, DEFAULT_CARDS, DEFAULT_SCORE, DEFAULT_BUDGET, \
    DEFAULT_DECK_LEN, BET_MIN, NA_DECK_LEN, DEFAULT_FLAGS, NUM_DECKS, NUM_PLAYERS
from random import shuffle
from typing import NewType
from typing import List, Tuple, Dict
from copy import deepcopy, copy
import time
import colours as col
from os import system, name


# UWAGA poniższy kod korzysta z pewnych założeń, których spełnienie jest konieczne do poprawnego działania programu;
#   1. Gracze mają różne imiona.
#   2. Nie można użyć split wiecej niż raz na 'rundę' (rozdzielonych kart nie można ponownie rozdzielić)
#   3. Od razu mam rozwiązanie dla wielu graczy,w game tworzona jest lista obiektów player
#   4. Zakładam, że defaultowe wartości gry wynoszą odpowiednio:
#       score = 0,  player.cards = [[]],   bet = 10,    dealer.cards = [[]],    imie = "player{numer gracza}"
#       budget = 200,   liczba graczy = 1,  liczba talii = 1
#
#   5. Jest problem z draw - potrzeba instancji klasy game żeby istniała talia na której draw wykonuje operacje

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def create_player_names():
    return [f"player {i + 1}" for i in range(NUM_PLAYERS)]


def create_deck():
    deck = NUM_DECKS * DEFAULT_DECK_NA
    shuffle(deck)
    return deck


def draw(cards):
    cards.append(DECK.pop(0))


def draw_hand(cards):
    draw(cards)
    draw(cards)


DECK = deepcopy(create_deck())


def create_players(llcards, llflags, llbets, llscores, lnames, lbudgets):
    return [Player(deepcopy(lcards), deepcopy(lflags), deepcopy(lbets), deepcopy(lscores), name2, budget) for
            lcards, lflags, lbets, lscores, name2, budget in zip(llcards, llflags, llbets, llscores, lnames, lbudgets)]


Card = NewType("Card", Tuple[str, int, str])
Cards = NewType("Cards", List[Card])


def game_loop():
    game = Game()
    game.first_round()
    game.first_turn()
    while game.run_next_turn():
        game.next_turn()
    game.final_turn()
    while game.run_next_round():
        game.next_round()
        game.first_turn()
        while game.run_next_turn():
            game.next_turn()
        game.final_turn()
    game.final_round()


class Game:

    def __init__(self, llcards=None, llflags=None, llscores=None, llbets=None, lnames=None, lbudgets=None,
                 dealer_cards=None):
        self.__llscores = llscores if llscores is not None else deepcopy(NUM_PLAYERS * [DEFAULT_SCORE])
        self.__llbets = llbets if llbets is not None else deepcopy(NUM_PLAYERS * [DEFAULT_BET])
        self.__llcards = llcards if llcards is not None else deepcopy(NUM_PLAYERS * [DEFAULT_CARDS])
        self.__llflags = llflags if llflags is not None else deepcopy(NUM_PLAYERS * [DEFAULT_FLAGS])
        self.__lnames = lnames if lnames is not None else deepcopy(create_player_names())
        self.__lbudgets = lbudgets if lbudgets is not None else deepcopy(NUM_PLAYERS * [DEFAULT_BUDGET])

        self.plbrkn = []
        self.pllst = create_players(self.__llcards, self.__llflags, self.__llbets,
                                    self.__llscores, self.__lnames, self.__lbudgets)
        self.dealer = Dealer(dealer_cards) if dealer_cards is not None else Dealer()

    def __str__(self) -> str:
        report = 'Game.__str__() called\n'
        report += f'Liczba graczy w grze : {len(self.pllst)}\nLiczba graczy bez pieniędzy : {len(self.plbrkn)}\n'
        for player in self.pllst:
            report += str(player)
        return report

    def first_turn(self) -> None:
        draw_hand(self.dealer.hand.cards)
        for player in self.pllst:
            for hand in player.hands_nt:
                draw_hand(hand.cards)
            player.calculate_scores()
            self.show_dealers_card()
            player.choice(self.dealer)
            player.check_for_split()
            player.calculate_scores()
            player.check_for_bust()
            player.lists_override()
            time.sleep(2)
            clear()
            player.choice_result()
            input("wcisnij enter aby wybrac kolejnego gracza")
            clear()

    def next_turn(self) -> None:
        for player in self.pllst:
            player.choice(self.dealer)
            player.check_for_split()
            player.calculate_scores()
            player.check_for_bust()
            player.lists_override()
            time.sleep(5)
            clear()
            player.choice_result()
            input("wcisnij enter aby wybrac kolejnego gracza")
            clear()

    def run_next_turn(self) -> bool:
        run = 0
        for player in self.pllst:
            run += len(player.hands_nt)
        return bool(run)

    def final_turn(self) -> None:
        print("All players either lost or chose to stand!")
        self.dealer.draw_until_17_or_higher()
        self.determine_round_outcome()
        self.CENR()
        input("Press Enter to continue...")

    def first_round(self) -> None:
        self.subtract_bets_from_budgets()

    def next_round(self) -> None:
        self.subtract_bets_from_budgets()
        for player in self.pllst:
            player.reset_player()
        self.dealer.reset_dealer()

    def run_next_round(self) -> bool:
        return bool(len(self.pllst))

    def final_round(self):
        outcome = "Game over!\nHere are the game results:"
        scores = [(player.name, player.budget) for player in self.pllst + self.plbrkn]

        def sort(elem):
            return elem[1]

        scores.sort(key=sort)
        for index, score in enumerate(scores):
            name1, wynik = scores
            outcome += f'{index + 1}. {name1} finished the game with {wynik}$\n'
        return outcome

    def show_dealers_card(self):
        print(f"Dealer's card : {self.dealer.hand.cards[0]}") if self.run_next_turn() else print(
            f"Dealer's cards : {self.dealer.hand.cards}")

    def determine_round_outcome(self):
        if self.dealer.hand.score > 21:
            print("Dealer busted! All those who didn't bust win!")
            for player in self.pllst:
                for hand in player.hands_stand:
                    hand.win()
        else:
            for player in self.pllst:
                index = 1
                for hand in player.hands_stand:
                    print(f"{player.name} has {len(player.hands_stand + player.hands_busted)} hand(s), "
                          f"{len(player.hands_busted)} of which are busted.")
                    outcome = f"{player.name} - Hand {index} - "
                    difference = abs(self.dealer.hand.score - 21) - abs(hand.score - 21)
                    if difference > 0:
                        pot = hand.win()
                        player.budget += pot
                        if hand.flags['blackJack']:
                            outcome += f"win - Black Jack! pot : {pot} = {hand.bet} * 2,5"
                        else:
                            outcome += f'win - pot : {pot}'
                    if difference == 0:
                        pot = hand.draw()
                        player.budget += pot
                        outcome += f"draw - original bet returned ({pot} = {hand.bet})"
                    else:
                        pot = hand.loss(self.dealer)
                        player.budget += pot
                        if pot == 0:
                            outcome += "loss"
                        else:
                            outcome += "loss - bet returned thanks to insurance"
                    print(outcome if not outcome else "outcome jest puste")

    def CENR(self):
        npllst = []
        for player in self.pllst:
            if player.can_afford_new_round():
                npllst.append(player)
            else:
                self.plbrkn.append(player)
        self.pllst = npllst

    def subtract_bets_from_budgets(self) -> None:  # OBLICZA BUDŻET PO ODJĘCIU ZAKŁĄDU (PRZY WEJŚCIU DO NOWEJ RUNDY)
        for player in self.pllst:
            for hand in player.hands_nt:
                player.budget -= hand.bet


class HandDealer:
    def __init__(self, cards: List[Card] = None, score: int = None):
        self.score = score if score is not None else deepcopy(DEFAULT_SCORE[0])
        self.cards = cards if cards is not None else deepcopy(DEFAULT_CARDS[0])

    def __str__(self):
        report = f"HandDealer.__str__() called\n"
        report += f"Cards : {self.cards}\n"
        report += f"Score : {self.score}\n"
        return report


class Hand(HandDealer):
    def __init__(self, cards=None, flags=None, bet=None, score=None):
        super().__init__(cards, score)
        self.flags = flags if flags is not None else deepcopy(DEFAULT_FLAGS[0])
        self.bet = bet if bet is not None else deepcopy(DEFAULT_BET[0])

    def __str__(self):
        report = f"Hand.__str__() called for id : {id(self)}\n"
        report += f"Cards : {self.cards}\n"
        report += f"Flags : {self.flags}\n"
        report += f"Bet : {self.bet}\n"
        report += f"Score : {self.score}\n"
        return report

    def __eq__(self, other):
        if type(other) == tuple:
            return False
        return self.cards == other.cards and self.flags == other.flags and \
               self.bet == other.bet and self.score == other.score

    def can_hit(self):
        return not self.flags["DD"]

    def can_stand(self):
        return not self.flags["stand"]

    def can_DD(self):
        return not self.flags["hit"]

    def can_split(self):
        if len(self.cards) == 2:
            _, card1, _ = self.cards[0]
            _, card2, _ = self.cards[1]
            return card1 == card2

        else:
            return False

    def can_insure(self, dealer):
        return dealer.hand.cards[0][0] == "Ace"

    def win(self):
        return 2 * self.bet if not self.flags["blackJack"] else 2.5 * self.bet

    def loss(self, dealer):
        return 0 if not (self.flags["insurance"] and dealer.hand.score == 21) else self.bet

    def draw(self):
        return self.bet


class Player:

    def __init__(self, lcards, lflags, lbets, lscores, name3, budget):
        self.hands_nt = [Hand(deepcopy(cards), deepcopy(flags), copy(bet), copy(score)) for cards, flags, bet, score in
                         zip(lcards, lflags, lbets, lscores)] if \
            (lcards, lflags, lbets, lscores) != (None, None, None, None) else [Hand()]
        self.name = name3
        self.budget = budget
        self.hands_stand = []
        self.hands_busted = []

    def __str__(self):
        report = f"\tPlayer.__str__() called\n"
        report += "\u001b[31m"
        report += f"Name : {self.name}\n"
        report += "\u001b[37m"
        report += f"Budget : {self.budget}\n"
        report += f"{self.name}.hands_nt : {self.hands_nt}\n"
        report += f"{self.name}.hands_stand : {self.hands_stand}\n"
        report += f"{self.name}.hands_busted : {self.hands_busted}\n"
        return report

    def hit(self, hand):
        draw(hand.cards)
        hand.flags["hit"] = True

    def stand(self, hand):
        hand.flags["stand"] = True
        self.hands_stand.append(hand)

    def DD(self, hand):
        if self.can_afford_new_bet(hand):
            draw(hand.cards)
            hand.bet *= 2
            hand.flags["DD"] = True
            self.stand(hand)
        else:
            print(f"Gracza {self.name} nie stac na Double Down")

    def split(self, hand):
        index = self.hands_nt.index(hand)
        hand.flags["split"] = True
        self.hands_nt = [elem for elem in self.hands_nt if elem != hand]
        self.budget -= hand.bet
        hand1, hand2 = Hand([hand.cards[0]], hand.flags, hand.bet), Hand([hand.cards[1]], hand.flags, hand.bet)
        self.hands_nt.insert(index, (hand1, hand2))

    def insure(self, hand):
        if self.can_afford_insurance(hand):
            hand.flags["insurance"] = True
        else:
            print(f"Gracza {self.name} nie stac na isurance")

    def can_afford_insurance(self, hand):
        return hand.bet * 0.5 >= self.budget

    def can_afford_new_bet(self, hand):
        return hand.bet <= self.budget

    def can_afford_new_round(self):
        return self.budget >= BET_MIN

    def choice(self, dealer):
        for index, hand in enumerate(self.hands_nt):
            run = True
            print(f"1) hit 2) stand  3) split  4) DD 5) insure\n| " + col.RED + f"{self.name},"
                                    + col.MAGENTA + f" hand {index + 1}" + col.WHITE + f" score and carts: {hand.score} : {hand.cards} : ")
            while run:
                choice = input()
                if choice == "1":
                    if hand.can_hit():
                        self.hit(hand)
                        run = False
                    else:
                        print(f"Hand {self.hands_nt.index(hand) + 1} of {self.name} can't hit\n")
                elif choice == "2":
                    if hand.can_stand():
                        self.stand(hand)
                        run = False
                    else:
                        print(f"Hand {self.hands_nt.index(hand) + 1} of {self.name} can't stand\n")
                elif choice == "3":
                    if hand.can_split():
                        self.split(hand)
                        run = False
                    else:
                        print(f"Hand {self.hands_nt.index(hand) + 1} of {self.name} can't split\n")
                elif choice == "4":
                    if hand.can_DD():
                        self.DD(hand)
                        run = False
                    else:
                        print(f"Hand {self.hands_nt.index(hand) + 1} of {self.name} can't DD\n")
                elif choice == "5":
                    if hand.can_insure(dealer):
                        self.insure(hand)
                        run = False
                    else:
                        print(f"Hand {self.hands_nt.index(hand)} of {self.name} can't ins\n")
                else:
                    print("Invalid input please tye again")

    def choice_result(self):
        message = ""
        blo = 1
        for index, hand in enumerate(self.hands_stand+self.hands_busted+self.hands_nt):
            check_sum = len([value for value in hand.flags.values() if value])
            if hand.flags["hit"]:
                message += col.RED + f"{self.name}," + col.MAGENTA + f" hand {index + 1}" + col.WHITE + \
                              f" chose to hit -  {hand.score}  : {hand.cards[:-1]} + {hand.cards[-1]}\n"
                message += col.RED + " - unfortunately he busted" + col.WHITE if hand.score > 21 else ""
            if hand.flags["stand"] and not hand.flags["DD"]:
                message += col.RED + f"{self.name}," + col.MAGENTA + f" hand {index + 1}" + col.WHITE + \
                              f" chose to stand -  {hand.score}  : {hand.cards}\n"
            if hand.flags["split"] and check_sum == 1:
                if blo % 2:
                    index_split = index + 1
                    message += col.RED + f"{self.name}," + col.MAGENTA + f" hand {index + 1}" + col.WHITE + \
                      f" chose to split his hand {index_split}\n" if not blo % 2 else ""
                    message += f"hand {index + 1} -  {hand.score}  : {hand.cards}\n"
                    blo += 1
                else:
                    message += f"hand {index + 1} -  {hand.score}  : {hand.cards}\n"
                    blo += 1
            if hand.flags["DD"]:
                message += col.RED + f"{self.name}," + col.MAGENTA + f" hand {index + 1}" + col.WHITE + \
                              f" chose to double down -  {hand.score}  : {hand.cards[:-1]} + {hand.cards[-1]}\n"
                message += col.RED + " - unfortunately he busted" + col.WHITE if hand.score > 21 else ""
            if hand.flags["insurance"]:
                message += col.RED + f"{self.name}," + col.MAGENTA + f" hand {index + 1}" + col.WHITE + \
                              f" chose to insure -  {hand.score}  : {hand.cards}\n"
        print(message)

    def check_for_bust(self):
        for hand in self.hands_nt:
            if hand.score > 21:
                self.hands_busted.append(hand)

    def check_for_split(self):
        nowa_lista = []
        for elem in self.hands_nt:
            if type(elem) == tuple:
                nowa_lista.append(elem[0])
                nowa_lista.append(elem[1])
            else:
                nowa_lista.append(elem)
        self.hands_nt = nowa_lista


    def lists_override(self):
        self.hands_nt = [hand for hand in self.hands_nt if hand not in self.hands_stand + self.hands_busted]

    def get_flags(self):
        return [hand.flags for hand in self.hands_nt]

    def reset_flags(self):
        for hand in self.hands_nt:
            hand.flags = DEFAULT_FLAGS

    def calculate_scores(self):
        for hand in self.hands_nt:
            nscore = 0
            for card in hand.cards:
                nscore += card[1]
            hand.score = nscore

    def reset_player(self):
        self.hands_nt = [Hand()]
        self.hands_stand = []
        self.hands_busted = []


class Dealer:

    def __init__(self, cards: List[Cards] = None, score=None):
        self.hand = HandDealer(cards=cards, score=score) if (cards, score) != (None, None) else HandDealer()

    def reset_dealer(self):
        self.hand = HandDealer()

    def calculate_score(self):
        aces = []
        nscore = 0
        for card in self.hand.cards:
            if card[1] != 0:
                nscore += card[1]
            else:
                index = self.hand.cards.index(card)
                aces.append((index, card))
        self.hand.score = nscore
        for index, card in aces:
            _, point, colour = card
            if self.hand.score <= 10:
                point = 11
            else:
                point = 1
            new_card = ("Ace", point, colour)
            self.hand.score += point
            self.hand.cards.insert(index, new_card)

    def draw_until_17_or_higher(self):
        self.calculate_score()
        message = f"Dealer's cards and score : {self.hand.cards} : {self.hand.score}"
        message += " < 17" if self.hand.score < 17 else ""
        print(message)
        while self.hand.score < 17:
            draw(self.hand.cards)
            self.calculate_score()
            print(f"Dealer draws {self.hand.cards[-1]}")
            time.sleep(2)
        else:
            print(f"Dealer's final cards and score : {self.hand.cards} : {self.hand.score}")


def main():
    game_loop()

main()
