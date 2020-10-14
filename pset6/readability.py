from cs50 import get_string
import re

text = get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i in text:
    if re.search("^[a-zA-Z]$", i):
        letters += 1
    if re.search("\s", i):
        words += 1
    if re.search("[.!?]", i):
        sentences += 1

index = 0.0588 * (100 * letters / words) - 0.296 * (100 * sentences / words) - 15.8

if index >= 16:
    print("Grade 16+")
elif index > 1 and index < 16:
    print(f"Grade {round(index)}")
else:
    print("Before Grade 1")