from cs50 import get_float

while True:
    dollars = get_float("Change owed: ")
    if dollars > 0:
        break

coins = 0

summ = 0

quarters = 25
dimes = 10
nickels = 5
cent = 1

cents = round((dollars*100), 2)

while cents >= quarters:
    cents = cents - quarters
    coins += 1
while cents >= dimes and cents < quarters:
    cents = cents - dimes
    coins += 1
while cents >= nickels and cents < dimes:
    cents = cents - nickels
    coins += 1
while cents >= cent and cents < nickels:
    cents = cents - cent
    coins += 1

print(f"{coins}")

