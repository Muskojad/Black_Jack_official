import pygame
import os
import pickle
green = (36, 143, 46)

def center_text(text, list):
    x = list[0]
    y = list[1]
    w = list[2]
    h = list[3]
    return text.get_rect(center=(int(x + 0.5 * w), int(y + 0.5 * h)))

class Menu_kon():
    def __del__(self):
        print("Menu kon usuniete")
    def __init__(self, money, window):
        self.money = money
        self.width_rect = 200
        self.height_rect = 50
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 25)
        self.font_arrow = pygame.font.Font("OpenSans-Regular.ttf", 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.center_x = int((1000 - self.width_rect) / 2)
        self.button_back = pygame.Rect(self.center_x, 600, self.width_rect, self.height_rect)
        self.textbox = pygame.Rect(self.center_x, 100, self.width_rect, 400)
        # self.lost_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        # self.won_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        # self.pass_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        self.num_players = len(money)
        if os.path.exists("stats"):
            list = pickle.load(open("stats", "rb"))
        else:
            list = [[0,0,0,0]]
        while len(list) < len(money):
            list.append([0,0,0,0])
        i = 0
        for player in money:
            if player > 0:
                list[i][0] += 1
            elif player < 0:
                list[i][1] += 1
            else:
                list[i][2] += 1
            list[i][3] += player
            i += 1
        pickle.dump(list, open("stats", "wb"))
        if os.path.exists("save"):
            os.remove("save")
        #pygame.time.wait(2000)

    def draw(self, window):

        window.fill(green)
        pygame.draw.rect(window, self.basic_col, self.button_back)
        pygame.draw.rect(window, self.basic_col, self.textbox)

        text_back = self.font_arrow.render("Back to menu", True, self.font_color)
        text_lost = self.font_arrow.render("You lost " + str(abs(10)) + "$", True, self.font_color)
        text_won = self.font_arrow.render("You won " + str(10) + "$", True, self.font_color)
        text_pass = self.font_arrow.render("Pass", True, self.font_color)
        i = 1
        for player in self.money:
            if player > 0:
                text = self.font_arrow.render("Player "+str(i)+" won " + str(player) + "$", True, self.font_color)
            elif player < 0:
                text = self.font_arrow.render("Player " + str(i) + " lost " + str(player) + "$", True, self.font_color)
            else:
                text = self.font_arrow.render("Player " + str(i) + "tied", True, self.font_color)
            height = self.textbox[3] / self.num_players
            window.blit(text, center_text(text, (self.textbox[0],self.textbox[1] + (i-1)*height,self.textbox[2],height)))
            i += 1

        window.blit(text_back, center_text(text_back, self.button_back))
        #window.blit(text_lost, center_text(text_lost, self.lost_rect))
        pygame.display.flip()

    def check_all_buttons(self, pos, window):
        if self.click(self.button_back, pos[0], pos[1]):
            return ("restart")

    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            return True
