def give_money1(money):
    money += 100


def give_money2(person):
    person.money += 100


class Person:
    def __init__(self):
        self.name = ""
        self.money = 0


def main():
    bob = Person()
    bob.name = "Bob"
    bob.money = 100


    give_money1(bob.money)
    give_money2(bob)
    print(bob.money)

main()


class Cat:
    def __init__(self):
        self.name = "Boots"
    def meow(self):
        print("meow")


kitkat = Cat()
kitkat.meow()


class Monster:

    def __init__(self, name, health):
        self.name = name
        self.health = health
        print(self.health)
    def decrease_health(self, damage):
        self.health -= damage
        print(self.health)
        if self.health <= 0:
            print("The monster has died!")

mike = Monster("Mike", 100)
mike.decrease_health(10)
mike.decrease_health(89)
mike.decrease_health(1)
print(mike.health)

johnny = Monster("Johnny", 200)
johnny.decrease_health(30)

class Boat():
    def __init__(self):
        self.tonnage = 0
        self.name = ""
        self.is_docked = True

    def dock(self):
        if self.is_docked:
            print("You are already docked.")
        else:
            self.is_docked = True
            print("Docking")

    def undock(self):
        if not self.is_docked:
            print("You aren't docked.")
        else:
            self.is_docked = False
            print("Undocking")

class Submarine(Boat):
    def submerge(self):
        print("Submerge!")


b = Boat()

b.dock()
b.undock()
b.undock()
b.dock()
b.dock()