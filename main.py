import pygame
from menu_kon import Menu_kon
from menu_GUI import Menu

width_w = 1000
height_w = 700

green = (36, 143, 46)


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
    it = 0
    time_game = 0
    menu = Menu()

    time2 = 0.0
    # Pętla główna
    while game_work:

        # cykle
        time += clock.tick(30)
        # if time > (1000 / 5): #20 cykli na sekunde
        time2 += time


        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_work = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    game = menu.check_all_buttons(event.pos, window)
                    if game[0] == "start":
                        in_menu = False
                        in_game = True
                elif in_game:
                    interface = game[1].check_all_buttons(event.pos, window)
                    if interface[0] == "end":
                        #game[1].update_cards(window, True)
                        in_game = False
                        in_menu_kon = False
                        it += 1
                        time_game = 0
                elif in_menu_kon:
                    kon = interface[1].check_all_buttons(event.pos, window)
                    if kon == "restart":
                        in_menu = True
                        in_menu_kon = False
                        del game
                        it = 0
                        time_game = 0
                        frap = True
                        print("GH")

        window.fill(green)
        if in_menu:
            menu.draw(window)
            # print("s")
            pygame.display.flip()
        elif in_game:
            game[1].time_left -= time/1000

            game[1].draw(window)
            length = len(game[1].cards.talia_gracza) + len(game[1].cards.talia_krupiera)
            if time_game > 1000 and it < length:
                it +=1
                time_game = 0
            game[1].update_cards(window, it)
            pygame.display.flip()
            time_game += time
            if game[1].time_left <= 0 and game[1].hotseat:
                in_game = False
                in_menu_kon = False
                krupier = game[1].cards.krupier()
                interface = ("end", Menu_kon(krupier[0], krupier[1], window))
                time_game = 0
                #it += 1
        # pygame.display.flip()
        elif not in_game and not in_menu_kon:
            length = len(game[1].cards.talia_gracza) + len(game[1].cards.talia_krupiera)
            if time_game > 5000 and it <= length:
                it += 1
                time_game = 0
            time_game += time
            game[1].cards.odslon = True
            print(game[1].cards.odslon, "sssssssssssssss")
            game[1].update_cards(window, it)
            print(game[1].cards.talia_krupiera)
            #pygame.time.wait(100)
            pygame.display.flip()
            #pygame.time.wait(5000)
            if it == length + 1:
                in_menu_kon = True
        elif in_menu_kon:
            interface[1].draw(window)
        time = 0.0
        # interface.update()
        # print("g")
        # print(interface.get_feedback())


talia = (
("as", 0, "Kier"), ("jedynka", 1, "Kier"), ("dwojka", 2, "Kier"), ("trojka", 3, "Kier"), ("czworka", 4, "Kier"),
("piatka", 5, "Kier"))  # ,
# (szostka,6, Kier), (dziewiatka,9, Kier), (dziesiatka,10, Kier), (jopek,10, Kier), (dama,10, Kier),
# (krol,10, Kier), (as,0, Pik), (jedynka,1, Pik), (dwojka,2, Pik), (trojka,3, Pik), (czworka,4, Pik),
# (piatka,5, Pik), (szostka,6, Pik), (dziewiatka,9, Pik), (dziesiatka,10, Pik), (jopek,10, Pik), (dama,10, Pik),
# (krol,10, Pik), (as,0, Trefl), (jedynka,1, Trefl), (dwojka,2, Trefl), (trojka,3, Trefl), (czworka,4, Trefl),
# (piatka,5, Trefl), (szostka,6, Trefl), (dziewiatka,9, Trefl), (dziesiatka,10, Trefl), (jopek,10, Trefl),
# (dama,10, Trefl), (krol,10, Trefl), (as,0, Karo), (jedynka,1, Karo), (dwojka,2, Karo), (trojka,3, Karo),
# (czworka,4, Karo), (piatka,5, Karo), (szostka,6, Karo), (dziewiatka,9, Karo), (dziesiatka,10, Karo),
# (jopek,10, Karo), (dama,10, Karo), (krol,10, Karo))


talia_gracza = [
    (11, "As", "Pik"),
    (3, "3", "Kier"),
    (5, "5", "Karo"),
    (7, "7", "Pik"),
    (9, "9", "Trefl"),
    (10, "Dama", "Pik"),
    (11, "As", "Pik"),
    (10, "Król", "Karo")
]

talia_gracza_po_spilt = [
    # (1,"As","Pik"),
    # (3,"3","Kier")
]

talia_krupiera = [
    (11, "As", "Pik"),
    (105, "5", "Trefl"),
]
if __name__ == "__main__":
    main()
