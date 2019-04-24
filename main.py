from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("HiPotion", "potion", "Heals 100 HP", 100)
superpotion = Item("SuperPotion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixer", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("HiElixir", "potion", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_inventory = [{"name": potion, "quantity": 15}, {"name": hipotion, "quantity": 5},
                    {"name": superpotion, "quantity": 5}, {"name": elixir, "quantity": 5},
                    {"name": hielixir, "quantity": 2}, {"name": grenade, "quantity": 5}]

# Create Characters
player1 = Person("Ironman :", 784, 480, 60, 34, player_magic, player_inventory)
player2 = Person("The Hulk:", 903, 240, 60, 34, player_magic, player_inventory)
player3 = Person("Hawkeye :", 403, 140, 60, 34, player_magic, player_inventory)
enemy = Person("Thanos  :", 1098, 300, 45, 25, [], [])

players = [player1, player2, player3]
running = True
i = 0

while running:

    # PLAYER STATS
    print("\n\n")
    print("NAME                     HP                                  MP")
    print("                         _________________________           __________")
    for player in players:
        player.get_stats()
    print("\n")

    # PLAYER ACTION PHASE
    for player in players:
        print("=====================")
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for", dmg, "points of damage.")
        elif index == 1:
            player.choose_magic()  # display magic options
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough Mp.\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1
            item = player.inventory[item_choice]["name"]

            if item_choice == -1:
                continue

            if player.inventory[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.inventory[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop) + " points of damage." + bcolors.ENDC)

    # ENEMY ACTION PHASE
    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points of damage.")

    print("-------------------------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")

    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy defeated you!" + bcolors.ENDC)
        running = False
