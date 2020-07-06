#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

import classes
import utility

deck = classes.Deck()
game = classes.Game()

game.first_round(deck)
game.enter_new_round()
utility.print_player_list(game)
game.player_list[0].
#game.round_menu(deck)
