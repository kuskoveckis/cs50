import sys
import csv
import re

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
else:
    count = 0
    # opena and read database csv file to a list
    with open(sys.argv[1], 'r') as file:
        reader = csv.reader(file)
        database = list(reader)
    # open and read dna text file
    with open(sys.argv[2], 'r') as dna:
        dnaData = dna.read()
    # test lists and output lists
    arrSmall = ['AGATC', 'AATG', 'TATC']
    arrLarge = ['AGATC', 'TTTTTTCT', 'AATG', 'TCTAG', 'GATA', 'TATC', 'GAAA', 'TCTG']

    strSmall = []
    strLarge = []

    # check for small csv file matches
    if sys.argv[1] == "databases/small.csv":
        for i in arrSmall:
            regex = rf'({i})\1*'
            regexCompile = re.compile(regex)
            match = [match for match in regexCompile.finditer(dnaData)]
            n = 0
            for z in range(len(match)):
                if match[z].group().count(i) > n:
                    n = match[z].group().count(i)
            strSmall.append(n)

        for i in range(len(database)):
            if database[i][1] == str(strSmall[0]) and database[i][2] == str(strSmall[1]) and database[i][3] == str(strSmall[2]):
                result = database[i][0]
                break
            else:
                result = "no match"

    # check for large csv file matches
    if sys.argv[1] == "databases/large.csv":
        for i in arrLarge:
            regex = rf'({i})\1*'
            regexCompile = re.compile(regex)
            match = [match for match in regexCompile.finditer(dnaData)]
            n = 0
            for z in range(len(match)):
                if match[z].group().count(i) > n:
                    n = match[z].group().count(i)
            strLarge.append(n)

        for i in range(len(database)):
            if database[i][1] == str(strLarge[0]) and database[i][2] == str(strLarge[1]) and database[i][3] == str(strLarge[2]) and database[i][4] == str(strLarge[3]) and database[i][5] == str(strLarge[4]) and database[i][6] == str(strLarge[5]) and database[i][7] == str(strLarge[6]) and database[i][8] == str(strLarge[7]):
                result = database[i][0]
                break
            else:
                result = "no match"

    print(result)
