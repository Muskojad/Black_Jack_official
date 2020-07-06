#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU PLANUJE DODAWAĆ FUNKCJE, KTÓRE MAJĄ UŁATWIĆ MI TESTOWANIE KODU
#

import resources


def print_player_list(game):
    for i in range(0, resources.NUM_PLAYERS):
        print(game.player_list[i])
