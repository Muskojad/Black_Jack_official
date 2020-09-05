import pygame
import pickle
from menu_kon import Menu_kon
from menu_GUI import Menu
import copy
import classes


width_w = 1000
height_w = 700

green = (36, 143, 46)
blue_1 = (51, 204, 255)
blue_2 = (0, 153, 204)
blue_3 = (0, 96, 128)
beige = (245,245,220)


def main():
    # część inicjalizacyjna :
    print("Hello")
    pygame.init()
    time = 0.0
    clock = pygame.time.Clock()
    # interface = Interface(talia_gracza,talia_gracza_po_spilt,talia_krupiera)
    game_work = True
    window = pygame.display.set_mode((width_w, height_w))
    in_menu = True
    in_game = False
    in_menu_kon = False
    in_stats = False
    it = 0
    time_game = 0
    load_list = []
    menu = Menu()

    time2 = 0.0
    # Pętla główna
    while game_work:
        time += clock.tick(30)
        time2 += time


        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_work = False
                if in_game:
                    load_list.append([copy.deepcopy(game[1].game), it, in_menu, in_game, game[1].time_left, menu.num_decs, menu.hotseat, menu.bet, game[1].current_player])
                    pickle.dump(load_list, open("save", "wb"))
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    game = menu.check_all_buttons(event.pos, window)
                    if game[0] == "start":
                        in_menu = False
                        in_game = True
                    if game[0] == "load":
                        in_menu = game[2][2]
                        in_game = game[2][3]
                        it = game[2][1]
                        load_list = game[3]
                        game[1].load_it = len(game[3])
                        #game[1].current_player = game[3][-1]
                        #popraw
                    if game[0] == "stats":
                        in_menu = False
                        in_stats = True
                elif in_game:
                    interface = game[1].check_all_buttons(event.pos, window)
                    #print(load_list[0][0].talia_gracza, "       ", len(load_list))
                    if interface[0] == "end_busted":
                        #in_game = False
                        in_menu_kon = False
                        #it += 1
                        time_game = 0
                    if interface[0] == "end":
                        #game[1].update_cards(window, True)
                        #in_game = False
                        in_menu_kon = False
                        #it += 1
                        time_game = 0
                    if interface == "undo":
                        game[1].game = copy.deepcopy(load_list[-2][0])
                        game[1].time_left = load_list[-2][4]
                        #print(str(load_list[-2][8]) + " load list player")
                        print(game[1].load_it)
                        game[1].current_player = load_list[-2][8]
                        game[1].load_it -= 1
                        game[1].game.pllst[game[1].current_player].choice_processing_functions()
                        it = load_list[-2][1]
                        load_list.pop()
                    if interface == "hit":
                        it += 1
                    if interface != "nothing_clicked" and interface != "undo":

                        player = game[1].current_player
                        print("player " + str(player))
                        game[1].game.pllst[player].choice_processing_functions()
                        player += 1

                        if not game[1].game.run_next_turn():
                            game[1].game.final_turn()
                            lista_kon =[]
                            for player in game[1].game.pllst:
                                lista_kon.append(player.budget[0])
                            menu_kon = Menu_kon(lista_kon, window)
                            in_game = False
                            in_menu_kon = False
                            count = 0
                            for a in game[1].game.pllst[game[1].current_player].hands_nt:
                                for b in a.cards:
                                    count += 1
                            for a in game[1].game.pllst[game[1].current_player].hands_stand:
                                for b in a.cards:
                                    count += 1
                            for a in game[1].game.pllst[game[1].current_player].hands_busted:
                                for b in a.cards:
                                    count += 1
                            it = count
                            print("koniec!!!!!!!!!!")
                            break
                            #return 0
                        while player >= classes.NUM_PLAYERS or len(game[1].game.pllst[player].hands_nt) == 0: ###################
                            player += 1
                            if player >= classes.NUM_PLAYERS:
                                player = 0

                        pygame.display.flip()
                        if not in_game or game[1].current_player == 0:
                            window.fill(green)
                        elif game[1].current_player == 1:
                            window.fill(blue_1)
                        elif game[1].current_player == 2:
                            window.fill(blue_2)
                        elif game[1].current_player == 3:
                            window.fill(blue_3)
                        game[1].draw(window)
                        game[1].update_cards(window, it)

                        pygame.display.flip()

                        load_list.append(
                            [copy.deepcopy(game[1].game), it, in_menu, in_game, game[1].time_left, menu.num_decs,
                             menu.hotseat,
                             menu.bet, player])

                        pygame.time.wait(1500)
                        game[1].current_player = player

                        game[1].load_it += 1






                elif in_menu_kon:
                    kon = menu_kon.check_all_buttons(event.pos, window)
                    if kon == "restart":
                        in_menu = True
                        in_menu_kon = False
                        del game
                        it = 0
                        time_game = 0
                        frap = True
                        #print("GH")

                elif in_stats:
                    go_back = game[1].check_all_buttons(event.pos, window)
                    if go_back:
                        in_menu = True
                        in_stats = False
                        del game

        if not in_game or game[1].current_player == 0:
            window.fill(green)
        elif game[1].current_player == 1:
            window.fill(blue_1)
        elif game[1].current_player == 2:
            window.fill(blue_2)
        elif game[1].current_player == 3:
            window.fill(blue_3)
        if in_menu:
            menu.draw(window)
            # print("s")
            pygame.display.flip()
        elif in_game:
            game[1].time_left -= time/1000

            game[1].draw(window)
            if game[1].game.pllst[0].hands_nt:
                lennn = len(game[1].game.pllst[0].hands_nt[0].cards)
            else:
                lennn = 2
            length = lennn + len(game[1].game.dealer.hand.cards)# + len(game[1].cards.talia_split)
            if time_game > 1000 and it < length:
                it +=1
                time_game = 0
                if it == 4:
                    load_list.append(
                        [copy.deepcopy(game[1].game),
                         it, in_menu, in_game, game[1].time_left, menu.num_decs, menu.hotseat,
                         menu.bet,game[1].current_player])
                    game[1].load_it += 1
            game[1].update_cards(window, it)
            pygame.display.flip()
            time_game += time
            if game[1].time_left <= 0 and game[1].hotseat:
                print("koniec czasu")
                #return 0
                in_game = False
                in_menu_kon = True
                menu_kon = Menu_kon([-game[1].game.pllst[0].budget[0]], window)##########################################
                #krupier = game[1].cards.krupier()   ###################
                #interface = ("end", Menu_kon(krupier[0], krupier[1], window))#####################
                time_game = 0
                #it += 1
        # pygame.display.flip()
        elif not in_game and not in_menu_kon and not in_stats:

            count_2 = count + len(game[1].game.dealer.hand.cards)
            #print(count)
            print(it)
            print(count_2)
            #length = len(game[1].game.pllst[game[1].current_player].hands_nt[0].cards) + len(game[1].game.dealer.hand.cards) + len(game[1].game.pllst[game[1].current_player].hands_nt[0].cards)
            if time_game > 2000 and it <= count_2:#length:
                it += 1
                time_game = 0
            time_game += time

            game[1].update_cards(window, it)

            pygame.display.flip()

            if it == count_2 + 1:
                in_menu_kon = True
                print("xd")
                print(it)

        elif in_menu_kon:
            #print("koniec")
            menu_kon.draw(window)

        elif in_stats:
            game[1].draw(window)

        time = 0.0



if __name__ == "__main__":
    main()
