#!/usr/bin/python3
import re
import sys
import pickle

class Letter():
    def __init__(self, char, start, end):
        self.char = char
        self.start = start
        self.end = end

class Word():
    def __init__(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end
        self.letters = []

# Open the text field file
try:
    text_field = open(sys.argv[1], 'r').read()
except:
    print("Input file not found")
    sys.exit()

# Regex expressions to appropriately split the TextGrid
item = re.compile(r'item \[.*\]:')
interval = re.compile(r'intervals \[.*\]:')

# Parse actual data out
items = item.split(text_field)[2:]
for i in range(len(items)):
    items[i] = interval.split(items[i])

# Parse out the letters 
letters = []
# items[0] is the character level
for char_info in items[0]:
    char_info = char_info.split('\n')
    for i in range(len(char_info)):
        char_info[i] = char_info[i].strip()
        if char_info[i] == "":
            continue
        char_info[i] = char_info[i].split('= ')[1]
    
    try:
        if "sp" not in char_info[3]:
            char = Letter(char_info[3], float(char_info[1]), float(char_info[2]))
            letters.append(char)
    except:
        pass

# Parse out the words
words = []
# items[1] is the word layer
for word_info in items[1]: 
    word_info = word_info.split('\n')
    for i in range(len(word_info)):
        word_info[i] = word_info[i].strip()
        if word_info[i] == "":
            continue
        word_info[i] = word_info[i].split('= ')[1]
    
    try:
        word = Word(word_info[3], float(word_info[1]), float(word_info[2]))
        words.append(word)
    except:
        pass

# Make the words the parent of the appropriate letters
for word in words:
    for letter in letters:
        if letter.start < word.start or letter.end > word.end:
            continue

        word.letters.append(letter.char[1:-1])

# Write ARPABet words to file, space separated
try:
    output = open(sys.argv[2], 'w')
except:
    print("Cannot write to file")
    sys.exit()
for word in words:
    if len(word.letters) > 0:
        output.write("".join(word.letters) + " ")
output.close()

pickle.dump(words, open(sys.argv[2] + '.pkl', 'wb'))
