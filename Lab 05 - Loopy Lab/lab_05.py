"""
for i in range(1, 10):
    for j in range(1, 10):
        if i * j < 10:
            print(" ", end="")
        print(i * j, end=" ")
    print()
"""

for i in range(1, 10):
    for y in range(10 - i):
        print(" ", end=" ")
    for j in range(i):
        print(j + 1, end=" ")
    for x in range(i, 1, -1):
        print(x - 1, end=" ")
    print()

for i in range(10):
    for j in range(i + 2):
        print(" ", end=" ")
    for x in range(1, 9 - i):
        print(x, end=" ")
    for y in range(7 - i, 0, -1):
        print(y, end=" ")
    print()

my_list = [101, 20, 10, 50, 60]
for item in my_list:
    print(item)
