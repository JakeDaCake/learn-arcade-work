class Room:
    def __init__(self, description, north, east, south, west):
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def main():
    done = False
    current_room = 0
    while not done:
        room_list = []
        room0 = Room("You find yourself in the master bedroom, there is a bed pushed up against the southern wall,\na closet on the western wall, and a large, fluffy red carpet that takes up half of the floor.\nThis room hasn't been lived in for a quite some time. There is a door on the east wall.", None, 1, None, None)
        room_list.append(room0)
        room1 = Room("You have entered the south hall. It is a narrow room with not much going on other than a door to the\nwest, the east, and an open doorway without a door to the north.""", 4, 0, None, 2)
        room_list.append(room1)
        room2 = Room("This is the dining room, the ceiling is curved creating a sort of dome with a chandelier hanging from\nthe center,  it clinks around subtly due to the slight draft coming from the open window\non the southern wall of the room. There is a door on the west wall and a much smaller one on the north wall.", 5, None, None, 1)
        room_list.append(room2)
        room3 = Room("This is the second bedroom, clearly made to house two children, two twin-sized beds sit opposite from\neat other on the northwest and southwest corners of the room, tods are strewn about\nevery which way and it smells like paint. There is a door on the east wall.", None, 4, None, None)
        room_list.append(room3)
        room4 = Room("You are now in the north hall, there was once an elaborate spiral staircase going down the center of this\nvery wide room but now part of the ceiling has caved in and the stairs are\n inaccessible. There are rooms to the west, east, and south, there is a balcony to the north.", 6, 5, 1, 3)
        room_list.append(room4)
        room5 = Room("This is the kitchen, a single broken plate is on the floor at the center of the room.\nThe sink is leaking. it sounds like a metronome. There is a door to the south and another one to\nthe west", None, None, 2, 4)
        room_list.append(room5)
        room6 = Room("The balcony is a semicircle jutting out from the manor's otherwise very flat north facade.\n The air smells and tastes like salt water, sprays of seawater sting your eyes.\nTo the south you may once again enter the manor, to the north is the ocean.", 7, None, 4, None)
        room_list.append(room6)
        room7 = Room("You jumped off the balcony and drowned.", None, None, None, None)
        room_list.append(room7)

        print()
        print(str(room_list[current_room].description))
        user_input = input("Where will you go? ")
        if user_input.upper() == "NORTH" or "N":
            next_room = room_list[current_room].north
            if next_room is None:
                print("You faceplant into a wall.")
                print()
            else:
                current_room = next_room
                print()

        elif user_input.upper() == "EAST" or "E":
            next_room = room_list[current_room].east
            if next_room is None:
                print("You faceplant into a wall.")
                print()
            else:
                current_room = next_room
                print()

        elif user_input.upper() == "SOUTH" or "S":
            next_room = room_list[current_room].south
            if next_room is None:
                print("You faceplant into a wall.")
                print()
            else:
                current_room = next_room
                print()

        elif user_input.upper() == "WEST" or "W":
            next_room = room_list[current_room].west
            if next_room is None:
                print("You faceplant into a wall.")
                print()
            else:
                current_room = next_room
                print()

        print(str(room_list[current_room].description))

main()
