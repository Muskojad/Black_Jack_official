#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

from classes import Game


def main():
    game = Game()
    print(game.deck)
    game.insert_cut()
    print(game.deck)

main()
