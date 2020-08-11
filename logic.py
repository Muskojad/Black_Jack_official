import random
from menu_kon import Menu_kon

talia_0 = [
    (11, "As", "Pik"),
    (3, "3", "Kier"),
    (3, "3", "Kier"),
    (3, "3", "Kier"),
    (3, "3", "Kier"),
    (3, "3", "Kier"),
    (5, "5", "Karo"),
    (7, "7", "Pik"),
    #(9, "9", "Trefl"),
    #(10, "Dama", "Pik"),
    #(11, "As", "Pik"),
    #(10, "Krol", "Karo")
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
        self.talia_split = []
        #print(self.talia_gracza)
        self.it = 4
        self.odslon = False
        self.in_split = False
        #self.possible = ["hit", "double"]
        self.possible_dict = {"hit": True, "stand":True, "double":True, "split":False, "insure":False}
    def hit(self):
        self.talia_gracza.append(self.talia[self.it])
        self.it += 1
        print("dodales")
        suma = 0
        for y in self.talia_gracza:
            suma += y[0]
        if suma > 21:
            return True
            #print("busted")
            #menu_kon = Menu_kon(0, 1, self.window)
        return False

    def hit_split(self):
        self.talia_split.append(self.talia[self.it])
        self.it += 1
        print("dodales do splitu")
        suma = 0
        for y in self.talia_split:
            suma += y[0]
        if suma > 21:
            self.in_split = False


    def split(self):
        self.talia_split.append(self.talia_gracza[0])
        self.talia_gracza.pop()
        self.in_split = True

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

    def possible(self):
        print(self.talia_gracza[0][0])
        print("dfdfdfdfd")
        #print(self.talia_gracza[1][0])
        if len(self.talia_gracza) == 2:
            self.possible_dict["double"] = True
        else:
            self.possible_dict["double"] = False
        if len(self.talia_gracza) >=2 and self.talia_gracza[0][0] == self.talia_gracza[1][0] and self.possible_dict["double"]:
            self.possible_dict["split"] = True
        else:
            self.possible_dict["split"] = False
        if self.talia_krupiera[0][1] == "As":
            self.possible_dict["insure"] = True
        else:
            self.possible_dict["insure"] = False



# talia_krupiera = [
#         (11,"As","Pik"),
#         (105,"5","Trefl"),
#         ]
