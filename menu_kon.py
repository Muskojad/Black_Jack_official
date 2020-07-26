import pygame
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
    def __init__(self, won , lost, window):
        self.won = won
        self.lost = lost
        self.width_rect = 200
        self.height_rect = 50
        self.font = pygame.font.SysFont('Arial', 25)
        self.font_arrow = pygame.font.SysFont('Arial', 20)
        self.font_color = (0, 0, 0)
        self.basic_col = (29, 59, 207)
        self.center_x = int((1000 - self.width_rect) / 2)
        self.button_back = pygame.Rect(self.center_x, 300, self.width_rect, self.height_rect)
        self.lost_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        self.won_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        self.pass_rect = pygame.Rect(self.center_x, 100, self.width_rect, self.height_rect)
        pygame.time.wait(2000)

    def draw(self, window):

        window.fill(green)
        pygame.draw.rect(window, self.basic_col, self.button_back)
        #pygame.draw.rect(window, self.basic_col, self.lost_rect)

        text_back = self.font_arrow.render("Back to menu", True, self.font_color)
        text_lost = self.font_arrow.render("You lost", True, self.font_color)
        text_won = self.font_arrow.render("You won", True, self.font_color)
        text_pass = self.font_arrow.render("Pass", True, self.font_color)

        if self.won and not self.lost:
            pygame.draw.rect(window, self.basic_col, self.won_rect)
            window.blit(text_won, center_text(text_won, self.won_rect))
        if not self.won and self.lost:
            pygame.draw.rect(window, self.basic_col, self.lost_rect)
            window.blit(text_lost, center_text(text_lost, self.lost_rect))
        if self.won and self.lost:
            pygame.draw.rect(window, self.basic_col, self.pass_rect)
            window.blit(text_pass, center_text(text_pass, self.pass_rect))

        window.blit(text_back, center_text(text_back, self.button_back))
        #window.blit(text_lost, center_text(text_lost, self.lost_rect))
        pygame.display.flip()

    def check_all_buttons(self, pos, window):
        if self.click(self.button_back, pos[0], pos[1]):
            return ("restart")

    def click(self, button, x, y):
        if button.x < x < button.x + button.w and button.y < y < button.y + button.h:
            return True
