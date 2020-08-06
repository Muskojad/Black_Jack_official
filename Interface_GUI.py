import pygame
import numpy
from logic import Cards
from menu_kon import Menu_kon

width_w = 1000
height_w = 700

def center_text(text, list):
    x = list[0]
    y = list[1]
    w = list[2]
    h = list[3]
    return text.get_rect(center=(int(x + 0.5 * w), int(y + 0.5 * h)))

class Interface_GUI():
    def __del__(self):
        print("interface usuniety")
    def __init__(self, num_decks, hotseat, window, time):
        self.num_decks = num_decks
        self.hotseat = hotseat
        self.time_left = time
        self.font = pygame.font.SysFont('Arial', 25)
        self.font_arrow = pygame.font.SysFont('Arial', 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.bet_col = (29, 186, 207)
        self.time_col = (29, 207, 56)
        self.width_rect = 100
        self.height_rect = 50
        self.center_x = int((width_w - self.width_rect) / 2)
        self.dist = 50

        self.y = height_w - self.dist - self.height_rect;
        self.x_start = int((width_w - 4 * self.width_rect - 3 * self.dist)/2)
        self.x_hit = self.x_start
        self.x_stand = self.x_start + self.dist + self.width_rect
        self.x_double = self.x_start + 2*(self.dist + self.width_rect)
        self.x_split = self.x_start + 3*(self.dist + self.width_rect)

        self.button_hit = pygame.Rect(self.x_hit, self.y, self.width_rect, self.height_rect)
        self.button_stand = pygame.Rect(self.x_stand, self.y, self.width_rect, self.height_rect)
        self.button_double = pygame.Rect(self.x_double, self.y, self.width_rect, self.height_rect)
        self.button_split = pygame.Rect(self.x_split, self.y, self.width_rect, self.height_rect)
        self.button_time = pygame.Rect(950-self.dist-self.width_rect, self.dist, self.width_rect+50, self.height_rect)

        self.cards = Cards(self.num_decks, window)
        self.it_x = 0
        self.it_y = 0


    def draw(self, window):
        pygame.draw.rect(window, self.basic_col, self.button_hit)
        pygame.draw.rect(window, self.basic_col, self.button_stand)
        pygame.draw.rect(window, self.basic_col, self.button_double)
        pygame.draw.rect(window, self.basic_col, self.button_split)

        text_hit = self.font.render("Hit", True, self.font_color)
        text_stand = self.font.render("Stand", True, self.font_color)
        text_double = self.font.render("Double", True, self.font_color)
        text_split = self.font.render("Split", True, self.font_color)

        if self.time_left <= 0:
            text_time = self.font.render("0 s left", True, self.font_color)
        else:
            text_time = self.font.render(str("% .2f" %(self.time_left)) + "s left" , True, self.font_color)

        if self.hotseat:
            pygame.draw.rect(window, self.time_col, self.button_time)
            window.blit(text_time, center_text(text_time, self.button_time))
        window.blit(text_hit, center_text(text_hit, self.button_hit))
        window.blit(text_stand, center_text(text_stand, self.button_stand))
        window.blit(text_double, center_text(text_double, self.button_double))
        window.blit(text_split, center_text(text_split, self.button_split))

    def check_all_buttons(self, pos, window):
        if self.can_click:
            self.basic_col = (29, 59, 207)
            if self.click(self.button_hit, pos[0], pos[1]):
                print("Hit")
                busted = self.cards.hit()
                if busted:
                    #self.update_cards(window)
                    self.cards.odslon = True
                    print('test')
                    menu_kon = Menu_kon(0, 1, window)
                    return ("end", menu_kon)
                
            if self.click(self.button_stand, pos[0], pos[1]):
                print("Stand")
                krupier = self.cards.krupier()
                self.cards.odslon = True
                #self.update_cards(window) ####################
                menu_kon = Menu_kon(krupier[0], krupier[1], window)
                return ("end", menu_kon)
        else:
            self.basic_col = (192, 192,192)
        #self.update_cards(window)
        return ("", "")


    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            return True

    def update_cards(self, window, it):
        self.can_click = False
        x_0 = 0
        while x_0 < len(self.cards.talia_gracza) and x_0 <it:
            x = self.cards.talia_gracza[x_0]
            print(it)
            nazwa_pliku = x[1] + "_" + x[2] + ".png"
            #print(nazwa_pliku)
            x_start = 425
            img = pygame.image.load(nazwa_pliku)
            window.blit(img, (x_start + (x_0 * 80), 350 ))
            if self.it_x == x_0:
                #pygame.time.wait(1000)
                self.it_x += 1
            #pygame.display.update(0, self.y/2, width_w, self.y/2)
            x_0 += 1




            #print(x)
        print("")
        #pygame.time.wait(1000)
        y_0 = 0
        while y_0 < len(self.cards.talia_krupiera) and y_0 + x_0 <it:
            y = self.cards.talia_krupiera[y_0]
            nazwa_pliku = y[1] + "_" + y[2] + ".png"
            print(nazwa_pliku)
            if not self.cards.odslon and len(self.cards.talia_krupiera) == 2 and y_0 == 1:
                window.blit(pygame.image.load("tyl.png"), (425 + (y_0 * 80), 100))
            else:
                window.blit(pygame.image.load(nazwa_pliku), (425 + (y_0 * 80), 100))

            if self.it_y == y_0:
                #pygame.time.wait(1000)
                print("xd")
                self.it_y += 1
            #pygame.display.update(0, 0, width_w, self.y/2)
            y_0 += 1

        if y_0 == len(self.cards.talia_krupiera):
            self.can_click = True
            #print(y)


