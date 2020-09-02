#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   W TYM PLIKU TESTUJE KOD
#

a = [[1,2]]

a = [elem if type(elem) != tuple else unpack_list(list_gen(elem)) for elem in a]
for index, elem in enumerate(a):



print(a)
