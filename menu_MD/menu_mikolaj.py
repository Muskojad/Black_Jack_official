#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

BUTTON_HOVER_COL = (120, 100, 240)
BUTTON_COL = (203, 140, 0)
BACKGROUND_COL = (230, 230, 255)

pygame.init()

win = pygame.display.set_mode((500, 500))
win.fill(BACKGROUND_COL)
pygame.display.set_caption("Test 1.0")


def No_assignment():
    print("No function assigned!")


class Window:
    def __init__(self, *args, **kwargs):
        self.window = win
        self.buttons = []
        self.function = args[0] if args else No_assignment


class Options(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        a = Button(BUTTON_COL, 150, 50, 200, 50, "A", self.function)
        b = Button(BUTTON_COL, 150, 150, 200, 50, "B", self.function)
        c = Button(BUTTON_COL, 150, 250, 200, 50, "C", self.function)

        menu_button = Button(BUTTON_COL, 100, 350, 300, 50, "Return to main menu", self.function)
        self.buttons = [a, b, c, menu_button]


class Menu(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game_button = Button(BUTTON_COL, 150, 50, 200, 50, "Begin the game", self.function)
        lb_button = Button(BACKGROUND_COL, 150, 150, 200, 50, "Leader Boards", self.function)
        options_button = Button(BUTTON_COL, 150, 250, 200, 50, "Options", self.function)
        a = Button(BUTTON_COL, 150, 350, 75, 50, "A", self.function)
        b = Button(BUTTON_COL, 275, 350, 75, 50, "B", self.function)
        self.buttons = [game_button, lb_button, options_button, a, b]


class LeaderBoards(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        a = Button(BUTTON_COL, 150, 50, 200, 50, "Score 1", self.function)
        b = Button(BUTTON_COL, 150, 150, 200, 50, "Score 2", self.function)
        c = Button(BUTTON_COL, 150, 250, 200, 50, "Score 2", self.function)

        menu_button = Button(BUTTON_COL, 100, 350, 300, 50, "Return to main menu", self.function)
        self.buttons = [a, b, c, menu_button]


class Button(Window):
    def __init__(self, colour, x, y, width, height, text='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.func = args[0]

    def __str__(self):
        return f"{self.text}"

    def draw(self, outline=None):
        if outline:
            pygame.draw.rect(self.window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            self.window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class GUI:
    def __init__(self):
        self.menu = Menu(self.switch_to_options())
        self.options = Options()
        self.leader_boards = LeaderBoards()
        self.current_screen = {"menu": True, "options": False, "LB": False}

    def switch_to_menu(self):
        print("switch_to_menu called")
        self.current_screen["menu"] = True
        self.current_screen["options"] = False
        self.current_screen["LB"] = False

    def switch_to_options(self):
        print("switch_to_options called")
        self.current_screen["options"] = True
        self.current_screen["LB"] = False
        self.current_screen["menu"] = False

    def switch_to_LB(self):
        print("switch_to_LB called")
        self.current_screen["LB"] = True
        self.current_screen["options"] = False
        self.current_screen["menu"] = False

    def get_active_buttons(self):
        for screen, status in self.current_screen.items():
            if screen == "menu" and status:
                return self.menu.buttons
            if screen == "options" and status:
                return self.options.buttons
            if screen == "LB" and status:
                return self.leader_boards.buttons


class Game:
    def __init__(self):
        self.gui = GUI()
        self.run = True
        self.active_screen = []
        self.pos = ()

    def redrawWindow(self):
        win.fill(BACKGROUND_COL)
        for b in self.active_screen:
            b.draw()

    def getCurrentScreen(self):
        return self.gui.current_screen

    def gameLoop(self):

        while self.run:
            self.redrawWindow()
            pygame.display.update()
            self.active_screen = self.gui.get_active_buttons()

            for event in pygame.event.get():
                self.pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    quit()

                for button in self.active_screen:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button.is_over(self.pos):
                            print(f'button {button.text} was pressed')
                            button.func()

                    if event.type == pygame.MOUSEMOTION:
                        if button.is_over(self.pos):
                            button.color = BUTTON_HOVER_COL
                        else:
                            button.color = BUTTON_COL


game = Game()
game.gameLoop()
