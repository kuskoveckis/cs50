from cs50 import get_int

# This is Mario less solution

while True:
    height = get_int("Height: ")
    if height > 0  and height <= 8:
        break
n = height
for i in range(height):
    for x in range(n-1):
         print(" ", end="")
    for j in range(i+1):
        print("#", end="")
    n = n-1
    print()