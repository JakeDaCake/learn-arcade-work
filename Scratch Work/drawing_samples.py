class Cat:
    population = 0

    def __init__(self, name):
        self.name = name
        Cat.population += 1

def main():
    cat1 = Cat("Pat")
    cat2 = Cat("Pepper")
    cat3 = Cat("Pouncy")

    print("The cat population is:", Cat.population)

main()

