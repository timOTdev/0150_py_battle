import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, inventory):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.inventory = inventory
        self.actions = ["Attack", "Magic", "Inventory"]

    def get_player_stats(self):
        # HP SPACE ADJUST
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        hp_adjusted = ""

        if len(hp_string) < 7:
            hp_counter = 7 - len(hp_string)

            while hp_counter > 0:
                hp_adjusted += " "
                hp_counter -= 1

            hp_adjusted += hp_string
        else:
            hp_adjusted = hp_string


        # HP BAR TICKS
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 100 / 4

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        # MP SPACE ADJUST
        mp_string = str(self.mp) + "/" + str(self.maxmp)
        mp_adjusted = ""

        if len(mp_string) < 7:
            mp_counter = 7 - len(mp_string)

            while mp_counter > 0:
                mp_adjusted += " "
                mp_counter -= 1

            mp_adjusted += mp_string
        else:
            mp_adjusted = mp_string

        # MP BAR TICKS
        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 100 /10

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        print("                         _________________________           __________")
        print(bcolors.BOLD + self.name + "       " +
              hp_adjusted + " |" +
              bcolors.OKGREEN + hp_bar + bcolors.ENDC + "| " +
              mp_adjusted + " |" +
              bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def get_enemy_stats(self):
        # HP SPACE ADJUST
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        hp_adjusted = ""

        if len(hp_string) < 11:
            hp_counter = 11 - len(hp_string)

            while hp_counter > 0:
                hp_adjusted += " "
                hp_counter -= 1

            hp_adjusted += hp_string
        else:
            hp_adjusted = hp_string

        # HP BAR TICKS
        hp_bar = ""
        hp_ticks = (self.hp / self.maxhp) * 100 / 2

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        print("                           __________________________________________________")
        print(bcolors.BOLD + self.name + "     " +
              hp_adjusted + " |" +
              bcolors.FAIL + hp_bar + bcolors.ENDC + "| ")

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def heal(self, dmg):
        self.hp += dmg
        return self.hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for action in self.actions:
            print("    " + str(i) + ".", action)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "INVENTORY:" + bcolors.ENDC)
        for item in self.inventory:
            print("    " + str(i) + ".", item["name"].name, ":", item["name"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1
