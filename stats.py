import pygame
import os
green = (36, 143, 46)

def center_text(text, list):
    x = list[0]
    y = list[1]
    w = list[2]
    h = list[3]
    return text.get_rect(center=(int(x + 0.5 * w), int(y + 0.5 * h)))

class Stats():
    def __del__(self):
        print("Menu statystyk usunięte")
    def __init__(self, stats, window):
        self.stats = stats
        self.width_rect = 200
        self.height_rect = 50
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 25)
        self.font_arrow = pygame.font.Font("OpenSans-Regular.ttf", 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.center_x = int((1000 - self.width_rect) / 2)
        self.textbox = pygame.Rect(int((1000 - 500)/2), 100, 500, 400)
        self.button_back = pygame.Rect(self.center_x, 600, self.width_rect, self.height_rect)
        self.num_players = len(stats)
        print(stats[0])


    def draw(self, window):

        window.fill(green)
        pygame.draw.rect(window, self.basic_col, self.button_back)
        pygame.draw.rect(window, self.basic_col, self.textbox)
        #pygame.draw.rect(window, self.basic_col, self.lost_rect)
        i = 1

        #text = []
        for player in self.stats:
            string = "Player " + str(i) + " won " + str(player[0]) + ", lost " + str(player[1]) + " and tied " +str(player[2]) +" games."
            text = self.font.render(string, True, self.font_color)
            height = self.textbox[3]/self.num_players
            window.blit(text, center_text(text, (self.textbox[0],self.textbox[1] + (i-1)*height,self.textbox[2],height)))
            print(string)
            print(i)
            #str_2 = "Balance is " + self.bilans + "$."
            i += 1

        # text_1 = self.font.render(str_1, True, self.font_color)
        # text_2 = self.font.render(str_2, True, self.font_color)
        text_back = self.font_arrow.render("Back to menu", True, self.font_color)


        #pygame.draw.rect(window, self.basic_col, self.textbox)


        #window.blit(text_1, center_text(text_1, (self.textbox[0],self.textbox[1],self.textbox[2],self.textbox[3]/2)))

        window.blit(text_back, center_text(text_back, self.button_back))
        pygame.display.flip()

    def check_all_buttons(self, pos, window):
        if self.click(self.button_back, pos[0], pos[1]):
            return ("back to menu")

    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            return True
