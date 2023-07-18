import random

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    miles_traveled = 0
    natives_miles_traveled = -20
    thirst = 0
    camel_tiredness = 0
    canteen_drinks = 3

    print("""
Welcome to Camel!
You have stolen a camel to make your way across the great Mobi desert.
The natives want their camel back and are chasing you down! Survive your
desert trek and outrun the natives.

----------""")

    done = False
    while not done:
        distance_from_natives = miles_traveled - natives_miles_traveled

        random1 = random.randint(7, 14)
        random2 = random.randint(10, 20)
        random3 = random.randint(1, 3)
        random4 = random.randint(5, 12)
        random5 = random.randint(1, 20)

        user_choice = input("""
A. Drink from your canteen.
B. Ahead moderate speed
C. Ahead full speed.
D. Stop and rest.
E. Status check.
Q. Quit.
Your choice? """)
        print()
        if user_choice.upper() == "Q":  # Quit game
            done = True
            print("The game has been quit.")

        elif user_choice.upper() == "E":  # Check status
            print("Miles traveled: " + str(miles_traveled) + "\nDrinks left in canteen: " + str(canteen_drinks) +
                  "\nThe natives are " +str(distance_from_natives) + " miles behind you.")

        elif user_choice.upper() == "D":  # Stop and rest
            print("You stop and rest for the night. Your camel is happy")
            camel_tiredness = 0
            natives_miles_traveled += random1

        elif user_choice.upper() == "C":  # Ahead full speed
            print("You traveled " + str(random2) + " miles.")
            miles_traveled += random2
            natives_miles_traveled += random1
            thirst += 1
            camel_tiredness += random3
            if random5 == 2:
                print("You came across an oasis, you refill your canteen and rest.")
                thirst = 0
                camel_tiredness = 0
                canteen_drinks = 3
            elif random5 == 1:
                print("You were hit by a sandstorm.")
                thirst += 1
                camel_tiredness += random3

        elif user_choice.upper() == "B":  # Ahead moderate speed
            print("You traveled " + str(random4) + " miles.")
            miles_traveled += random4
            natives_miles_traveled += random1
            thirst += 1
            camel_tiredness += 1
            if random5 == 2:
                print("You found an oasis, you refill your canteen and rest.")
                thirst = 0
                camel_tiredness = 0
                canteen_drinks = 3
            elif random5 == 1:
                print("You were hit by a sandstorm.")
                thirst += 1
                camel_tiredness += random3

        elif user_choice.upper() == "A" and canteen_drinks > 0:  # Drink from canteen
            print("You took a drink from your canteen. How refreshing.")
            thirst = 0
            canteen_drinks -= 1

        elif canteen_drinks == 0:  # If they want to drink from the empty canteen
            print("There is no water left in your canteen.")

        else:
            print("What are you, stupid?")

        if 4 < thirst < 7:
            print("You are thirsty!")

        elif thirst > 6:
            print("You died of thirst!")
            done = True

        if 5 < camel_tiredness < 9:
            print("Your camel is getting tired.")

        elif camel_tiredness > 8:
            print("Your camel is dead.")
            done = True

        if 15 > distance_from_natives > 0:
            print("The natives are getting close!")

        elif distance_from_natives <= 0:
            print("The natives caught you.")
            done = True

        elif miles_traveled >= 200:
            print("You got out of the desert. You win!")
            done = True


main()
