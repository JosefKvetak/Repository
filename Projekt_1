"""
Projekt_1.py: první projekt do Engeto Online Python Akademie

author: Josef Květák
email: josef.kvetak@gmail.com
"""

TEXTS = [
    '''Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30 and the Union Pacific Railroad,
    which traverse the valley.''',
    '''At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.''',
    '''The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.'''
]

USERS = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

print("----------------------------------------")
username = input("username:").strip()
password = input("password:").strip()
print("----------------------------------------")

if USERS.get(username) != password:
    print("unregistered user, terminating the program..")
    exit()

print(f"Welcome to the app, {username}")
print(f"We have {len(TEXTS)} texts to be analyzed.")
print("----------------------------------------")
text_choice = input(f"Enter a number btw. 1 and {len(TEXTS)} to select: ").strip()
print("----------------------------------------")

if not text_choice.isdigit():
    print("You did not enter a number, terminating the program..")
    exit()

text_choice = int(text_choice)
if not (1 <= text_choice <= len(TEXTS)):
    print("Selected number is out of range, terminating the program..")
    exit()

selected_text = TEXTS[text_choice - 1]

import string

words = [
    word.strip(string.punctuation)
    for word in selected_text.split()
    if word.strip(string.punctuation)
]

word_count = len(words)
titlecase_count = sum(1 for w in words if w.istitle())
uppercase_count = sum(1 for w in words if w.isupper() and not w.isdigit())
lowercase_count = sum(1 for w in words if w.islower())
numeric_count = sum(1 for w in words if w.isdigit())
numeric_sum = sum(int(w) for w in words if w.isdigit())

print(f"There are {word_count} words in the selected text.")
print(f"There are {titlecase_count} titlecase words.")
print(f"There are {uppercase_count} uppercase words.")
print(f"There are {lowercase_count} lowercase words.")
print(f"There are {numeric_count} numeric strings.")
print(f"The sum of all the numbers {numeric_sum}")
print("----------------------------------------")
print("LEN|  OCCURENCES  |NR.")

lengths = {}
for w in words:
    l = len(w)
    lengths[l] = lengths.get(l, 0) + 1

for length in sorted(lengths):
    stars = '*' * lengths[length]
    print(f"{length:>3}|{stars:<15}|{lengths[length]}")
