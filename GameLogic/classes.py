#!/usr/bin/python
# -*- coding: utf-8 -*-


from resources import DEFAULT_DECK, DEFAULT_BET, DEFAULT_CARDS, DEFAULT_SCORE, DEFAULT_BUDGET
from random import shuffle
from typing import NewType
from typing import List, Tuple
from copy import deepcopy, copy


# UWAGA poniższy kod korzysta z pewnych założeń, których spełnienie jest konieczne do poprawnego działania programu;
#   1. Gracze mają różne imiona.
#   2. Nie można użyć split wiecej niż raz na 'rundę' (rozdzielonych kart nie można ponownie rozdzielić)
#   3. Od razu mam rozwiązanie dla wielu graczy,w game tworzona jest lista obiektów player
#   4. Zakładam, że defaultowe wartości gry wynoszą odpowiednio:
#       score = 0,  player.cards = [[]],   bet = 10,    dealer.cards = [[]],    imie = "player{numer gracza}"
#       budget = 200,   liczba graczy = 1,  liczba talii = 1
#
#   5. Jest problem z draw - potrzeba instancji klasy game żeby istniała talia na której draw wykonuje operacje

def create_player_names(num_players):
    names = []
    for i in range(num_players):
        names.append(f"player {i + 1}")
    return names


def create_deck(num_decks):
    return shuffle(num_decks * DEFAULT_DECK)


def create_players(num_players, scores, players_cards, bets, players_names, budgets):
    players = []
    for i in range(num_players):
        players.append(Player(cards=players_cards[i], score=scores[i], bet=bets[i],
                              budget=budgets[i], name=players_names[i]))
    return players


Cards = NewType("Card", List[Tuple[str, int, str]])


class Game:

    def __init__(self, deck: Cards = None, scores: List[int] = None, players_cards: List[Cards] = None,
                 players_bets: List[float] = None, dealer_cards: List[Cards] = None,
                 players_names: List[str] = None, budgets: List[int] = None, num_players: int = 1, num_decks: int = 1):
        self.num_decks = num_decks
        self.deck = deck if deck is not None else deepcopy(create_deck(num_decks))
        self.__scores = scores if scores is not None else copy(num_players * DEFAULT_SCORE)
        self.__bets = players_bets if players_bets is not None else copy(num_players * DEFAULT_BET)
        self.__players_cards = players_cards if players_cards is not None else copy(num_players * DEFAULT_CARDS)
        self.__players_names = players_names if players_names is not None else create_player_names(num_players)
        self.__budgets = budgets if budgets is not None else copy(num_players * DEFAULT_BUDGET)

        self.shared_budgets = {}
        self.dealer = Dealer(dealer_cards) if dealer_cards is not None else Dealer(DEFAULT_CARDS)
        self.player_list = create_players(num_players=num_players, scores=self.__scores, budgets=self.__budgets,
                                          players_cards=self.__players_cards, bets=self.__bets,
                                          players_names=self.__players_names)

    def __str__(self):
        report = ""
        for player in self.player_list:
            report += f"\nPlayer {self.player_list.index(player) + 1}. data:\ncards: {player.cards}\n" \
                      f"score: {player.score}\nbet: {player.bet}\nbudget: {player.budget}\nname: {player.name}\n"

        return f"Created {len(self.player_list)} player(s):" + report

    def draw(self):
        return self.deck.pop(0)

    def get_dealers_hand(self):
        return self.dealer.had_ace

    # DOKONUJE ZAMIANY GRACZA, KTÓRY WYWOŁAŁ SPLIT NA 2 OBIEKTY TYPU GRACZ

    def create_hands(self, player, player_index):
        self.shared_budgets[f"{player.name} shared budget"] = SharedBudget(player.budget, player_index)
        first_hand = Player(cards=deepcopy(player.cards[0]), score=deepcopy(player.score), bet=deepcopy(player.bet),
                            budget=0, name=f"{player.name} first hand")
        second_hand = Player(cards=deepcopy(player.cards[1]), score=deepcopy(player.score), bet=deepcopy(player.bet),
                             budget=0, name=f"{player.name} second hand")
        first_hand.budget = self.shared_budgets[f"{player.name} shared budget"]
        second_hand.budget = self.shared_budgets[f"{player.name} shared budget"]
        return [first_hand, second_hand]

    def split(self):
        for player_index, player in enumerate(self.player_list):
            if player.do_split and not player.had_split:
                hands = self.create_hands(player, player_index)
                self.player_list.pop(player_index)
                self.player_list.insert(player_index, hands[0])
                self.player_list.insert(player_index + 1, hands[1])
            else:
                pass


class Entity(object):

    def __init__(self, cards=[], score=0):
        self.cards = cards
        self.score = score

    # OBLICZA AKTUALNY WYNIK
    def calculate_score(self):
        self.score = 0
        for card in self.cards:
            _, point, _ = card
            self.score += point

    # ZWRACA AKTUALNY WYNIK
    def get_score(self):
        return self.score


class SharedBudget:
    def __init__(self, budget, index):
        self.budget = budget
        self.index = index

    def __str__(self):
        return f"Shared Budget of player {self.index+1} budget: {self.budget}"

    def change_budget(self, x):
        self.budget = x


class Player(Entity):

    def __init__(self, cards: list, score: int, bet: float, name: str, budget: float):
        super().__init__(cards=cards, score=score)
        self.bet = bet
        self.name = name
        self.budget = budget
        self.do_split: bool = False
        self.had_hit: bool = False
        self.had_split: bool = False
        self.had_stood: bool = False
        self.had_doubled: bool = False

    def __str__(self):
        report = "Player __str__ called"
        report += f"\nPlayer data:\ncards: {self.cards}\n" \
                  f"score: {self.score}\nbet: {self.bet}\nbudget: {self.budget}\nname: {self.name}\n"

        return report

    # USTAWIA WARTOŚĆ ZAKŁADU
    def set_bet(self, new_bet):
        self.bet = new_bet

    # METODY SPRAWDZAJĄCE

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ SPLIT
    def can_split(self):
        _, card1, _ = self.cards[0]
        _, card2, _ = self.cards[1]

        if card1 == card2 and not self.had_hit and not self.had_split:
            return True
        else:
            return False

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ DOUBLE DOWN
    def can_double_down(self):
        if not self.had_hit:
            return True
        else:
            return False

    # SPRAWDZA CZY GRACZ MOŻE UŻYĆ INSURANCE
    def can_insure(self):
        raise NotImplementedError()

    # METODY WŁAŚCIWE

    def hit(self, game):
        if not self.had_doubled:
            game.draw()
            self.had_hit = True
        else:
            print('After doubling down you cannot draw any more cards')

    def stand(self):
        self.had_stood = True

    def double_down(self):
        if self.can_double_down():
            self.set_bet(2 * self.bet)
            self.hit()
            self.had_doubled = True
        else:
            print('You cannot double down')

    def split(self):
        if self.can_split():
            self.do_split = True
        else:
            print('You cannot split')


class Dealer(Entity):

    def __init__(self, cards=[], score=0):
        super().__init__(cards=cards, score=score)
        self.had_ace: bool = False
        self.has_score_higher_than_or_eq_to_17: bool = False

    def check_ace(self):
        if self.cards[0][0] == 'ace':
            had_ace = True

    def check_if_score_higher_than_or_eq_to_17(self):
        if self.cards[0][1] + self.cards[1][1] <= 16:
            self.has_score_higher_than_or_eq_to_17 = True
