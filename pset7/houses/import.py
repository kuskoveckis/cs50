import sys
import csv
from cs50 import SQL

if len(sys.argv) != 2 or not (sys.argv[1].endswith(".csv")):
    print("Usage: python import.py data.csv")
    sys.exit(1)

open("students.db", "w").close()
db = SQL("sqlite:///students.db")

db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")
with open(sys.argv[1], 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["name"]
        house = row["house"]
        birth = row["birth"]
        n = None
        spt = name.split()
        if len(spt) == 2:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       spt[0], n, spt[1], house, int(birth))
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       spt[0], spt[1], spt[2], house, int(birth))
