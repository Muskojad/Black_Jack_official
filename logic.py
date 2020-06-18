import random
from menu_kon import Menu_kon

talia_0 = [
    (11, "As", "Pik"),
    (3, "3", "Kier"),
    (5, "5", "Karo"),
    (7, "7", "Pik"),
    (9, "9", "Trefl"),
    (10, "Dama", "Pik"),
    (11, "As", "Pik"),
    (10, "Krol", "Karo")
]


class Cards(object):
    def __init__(self, num_decks, window):
        self.window = window
        #hile num_decks > 0:
         #   talia = talia_0.append(talia_0)
        self.talia = random.sample(talia_0 * num_decks, len(num_decks*talia_0))
        #print(self.talia)
        #self.num_decks = num_decks
        self.talia_krupiera = self.talia[:2]
        #print(self.talia_krupiera)
        self.talia_gracza = self.talia[2:4]
        #print(self.talia_gracza)
        self.it = 4
    def hit(self):
        self.talia_gracza.append(self.talia[self.it])
        self.it += 1
        print("dodales")
        suma = 0
        for y in self.talia_gracza:
            suma += y[0]
        if suma > 21:
            return True
            print("busted")
            menu_kon = Menu_kon(0, 1, self.window)
        return False
    def krupier_hit(self):
        self.talia_krupiera.append(self.talia[self.it])

        self.it += 1
        #self.krupier()
    def krupier(self):
        sum = 0
        #print('ff')
        for x in self.talia_krupiera:
            sum += x[0]
        while sum < 17:
            self.krupier_hit()
            sum = 0
            for x in self.talia_krupiera:
                sum += x[0]

            print("krupier hit")

        sum_gracz = 0
        for y in self.talia_gracza:
            sum_gracz += y[0]
        print("HHHHHHHHHHHHHHHHH")
        if abs(21-sum) < abs(21-sum_gracz):
            return (0, 1)
            menu_kon = Menu_kon(0, 1, self.window)
            print("przegrałeś")
        elif abs(21-sum) == abs(21-sum_gracz):
            print("remis")
            return (1, 1)
            menu_kon = Menu_kon(1, 1, self.window)
        else:
            print("wygrales")
            return (1, 0)
            menu_kon = Menu_kon(1, 0, self.window)



# talia_krupiera = [
#         (11,"As","Pik"),
#         (105,"5","Trefl"),
#         ]
