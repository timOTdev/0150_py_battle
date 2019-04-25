from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

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
hielixir = Item("HiElixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_inventory = [{"name": potion, "quantity": 15}, {"name": hipotion, "quantity": 5},
                    {"name": superpotion, "quantity": 5}, {"name": elixir, "quantity": 5},
                    {"name": hielixir, "quantity": 2}, {"name": grenade, "quantity": 5}]

# Create Characters
player1 = Person("Ironman  ", 4000, 700, 350, 34, player_magic, player_inventory)
player2 = Person("The Hulk ", 7000, 200, 400, 34, player_magic, player_inventory)
player3 = Person("Hawkeye  ", 3000, 1, 280, 34, player_magic, player_inventory)

enemy1 = Person("Imp      ", 1250, 400, 250, 30, [], [])
enemy2 = Person("Thanos   ", 10000, 800, 600, 200, [], [])
enemy3 = Person("Imp      ", 1250, 400, 250, 30, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

while running:

    # PLAYER AND ENEMY STATS
    print("\n\n")
    print("NAME                       HP                                  MP")
    for player in players:
        player.get_player_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    # PLAYER ACTION PHASE
    for player in players:
        print("=====================")
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            target = player.choose_target(enemies)
            dmg = player.generate_damage()
            enemies[target].take_damage(dmg)
            print("You attacked " + enemies[target].name.replace(" ", "") + " for " + str(dmg) + " points of damage.")

            if enemies[target].get_hp() == 0:
                print(enemies[target].name.replace(" ", "") + " has perished.")
                del enemies[target]
        elif index == 1:
            player.choose_magic()  # display magic options
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough Mp.\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP." + bcolors.ENDC)
            elif spell.type == "black":
                spell = player.magic[magic_choice]
                target = player.choose_target(enemies)
                magic_dmg = spell.generate_damage()
                enemies[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " +
                      enemies[target].name.replace(" ", "") + bcolors.ENDC)

                if enemies[target].get_hp() == 0:
                    print(enemies[target].name.replace(" ", "") + " has perished.")
                    del enemies[target]

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
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "HiElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                target = player.choose_target(enemies)
                enemies[target].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " +
                      enemies[target].name.replace(" ", "") + bcolors.ENDC)

                if enemies[target].get_hp() == 0:
                    print(enemies[target].name.replace(" ", "") + " has perished.")
                    del enemies[target]

    # ENEMY ACTION PHASE
    enemy_choice = 1

    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks " + players[target].name.replace(" ", "") + " for " + str(enemy_dmg) + " points of damage.")

    print("-------------------------------------------------")


    # CHECK GAME CONDITIONS
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
