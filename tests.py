#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

had_hit = False
had_stood = False
had_doubled = False


def can_double_down1():
    if not had_hit and not had_stood and not had_doubled:
        return True
    else:
        return False


def can_double_down2():
    return not had_hit and not had_stood and not had_doubled


print(can_double_down1())
print(can_double_down2())
