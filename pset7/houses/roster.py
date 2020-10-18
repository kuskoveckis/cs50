import sys
from cs50 import SQL

if len(sys.argv) != 2:
    print("Usage: python roster.py house")
    exit(1)

house = sys.argv[1]
db = SQL("sqlite:///students.db")
db_list = db.execute("SELECT first, middle, last, birth FROM students WHERE house=? ORDER BY last ASC, first", house)
for row in db_list:
    if row["middle"] == None:
        print(row['first'] + " " + row['last'] + ", born" + " " + str(row['birth']))
    else:
        print(row['first'] + " " + row['middle'] + " " + row['last'] + ", born" + " " + str(row['birth']))