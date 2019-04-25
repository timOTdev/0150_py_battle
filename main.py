from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Spells
fire = Spell("Fire", 10, 400, "black")
thunder = Spell("Thunder", 10, 400, "black")
blizzard = Spell("Blizzard", 10, 400, "black")
meteor = Spell("Meteor", 20, 400, "black")
quake = Spell("Quake", 14, 600, "black")
cure = Spell("Cure", 12, 800, "white")
cura = Spell("Cura", 18, 1000, "white")

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_magic = [fire, meteor, cure]


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("HiPotion", "potion", "Heals 100 HP", 100)
superpotion = Item("SuperPotion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixer", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("HiElixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_inventory = [{"name": potion, "quantity": 15}, {"name": hipotion, "quantity": 5},
                    {"name": superpotion, "quantity": 5}, {"name": elixir, "quantity": 5},
                    {"name": hielixir, "quantity": 2}, {"name": grenade, "quantity": 5}]

# Create Characters
player1 = Person("Ironman  ", 4000, 700, 350, 34, player_magic, player_inventory)
player2 = Person("Hulk     ", 7000, 200, 400, 34, player_magic, player_inventory)
player3 = Person("Hawkeye  ", 3500, 1, 280, 34, player_magic, player_inventory)

enemy1 = Person("Imp      ", 2500, 400, 250, 30, enemy_magic, [])
enemy2 = Person("Thanos   ", 10000, 800, 900, 200, enemy_magic, [])
enemy3 = Person("Imp      ", 2500, 400, 250, 30, enemy_magic, [])

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
    print("\n")

    # PLAYER ACTION PHASE
    for player in players:
        print("=====================")
        player.choose_action()

        while True:
            choice = input("Choose action: ")
            try:
                user_choice = int(choice)
                index = int(user_choice) - 1
                if 0 <= index <= 2:
                    break
                else:
                    print("Choice needs to be a valid option.")
            except ValueError:
                print("Choice needs to be a number.")

        if index == 0:
            player.choose_target(enemies)

            while True:
                target = input("CHOOSE TARGET:")
                try:
                    user_target = int(target)
                    index = int(user_target) - 1
                    if 0 <= index <= len(enemies) - 1:
                        target = index
                        break
                    else:
                        print("Choice needs to be a valid option.")
                except ValueError:
                    print("Choice needs to be a number.")

            dmg = player.generate_damage()
            enemies[target].take_damage(dmg)

            print("You attacked " + enemies[target].name.replace(" ", "") + " for " + str(dmg) + " points of damage.")

            if enemies[target].get_hp() == 0:
                print(enemies[target].name.replace(" ", "") + " has perished.")
                del enemies[target]
        elif index == 1:
            player.choose_magic()  # display magic options

            while True:
                magic_choice = input("CHOOSE MAGIC:")
                try:
                    target = int(magic_choice)
                    index = int(target) - 1
                    if 0 <= index <= len(player.magic) - 1:
                        magic_choice = index
                        break
                    else:
                        print("Choice needs to be a valid option.")
                except ValueError:
                    print("Choice needs to be a number.")

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
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
                player.choose_target(enemies)

                while True:
                    target = input("CHOOSE TARGET:")
                    try:
                        user_target = int(target)
                        index = int(user_target) - 1
                        if 0 <= index <= len(enemies) - 1:
                            target = index
                            break
                        else:
                            print("Choice needs to be a valid option.")
                    except ValueError:
                        print("Choice needs to be a number.")

                magic_dmg = spell.generate_damage()
                enemies[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " +
                      enemies[target].name.replace(" ", "") + bcolors.ENDC)

                if enemies[target].get_hp() == 0:
                    print(enemies[target].name.replace(" ", "") + " has perished.")
                    del enemies[target]

        elif index == 2:
            player.choose_item()

            while True:
                item_choice = input("CHOOSE ITEM:")
                try:
                    user_choice = int(item_choice)
                    index = int(user_choice) - 1
                    if 0 <= index <= len(player.inventory) - 1:
                        item_choice = index
                        break
                    else:
                        print("Choice needs to be a valid option.")
                except ValueError:
                    print("Choice needs to be a number.")

            if player.inventory[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            item = player.inventory[item_choice]["name"]
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
                player.choose_target(enemies)

                while True:
                    target = input("CHOOSE TARGET:")
                    try:
                        user_target = int(target)
                        index = int(user_target) - 1
                        if 0 <= index <= len(enemies) - 1:
                            target = index
                            break
                        else:
                            print("Choice needs to be a valid option.")
                    except ValueError:
                        print("Choice needs to be a number.")

                enemies[target].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " +
                      enemies[target].name.replace(" ", "") + bcolors.ENDC)

                if enemies[target].get_hp() == 0:
                    print(enemies[target].name.replace(" ", "") + " has perished.")
                    del enemies[target]

    print("-------------------------------------------------")

    # ENEMY ACTION PHASE
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        target = random.randrange(0, len(players))

        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for " +
                  str(enemy_dmg) + " points of damage.")

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has perished.")
                del players[target]

        elif enemy_choice == 1:
            spell = enemy.choose_enemy_spell()

            if spell is None:
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for " +
                      str(enemy_dmg) + " points of damage.")
                continue

            magic_dmg = spell.generate_damage()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for " +
                      str(magic_dmg) + " HP." + bcolors.ENDC)
            elif spell.type == "black":
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + " " + spell.name + "'s deals " +
                      str(magic_dmg) + " points of damage to " + players[target].name.replace(" ", "") +
                      bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has perished.")
                del players[target]

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
