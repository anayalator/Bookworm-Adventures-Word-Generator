import operator
import math
import os

cwd = os.path.dirname(os.path.realpath(__file__))

with \
open(cwd + "/words.txt","r") as words, \
open(cwd + "/colors.txt","r") as colorWords, \
open(cwd + "/metals.txt","r") as metalWords, \
open(cwd + "/mammals.txt","r") as mammalWords:
    dictionary = [line.strip() for line in words]
    colors = [line.strip() for line in colorWords]
    metals = [line.strip() for line in metalWords]
    mammals = [line.strip() for line in mammalWords]

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',\
'qu','r','s','t','u','v','w','x','y','z']
    
#enter tile and first letter of its color
#prints the top 10 strongest words:
#(word, [num of letters worth, actual number of letters in word])
#not all letters are worth the same, different gems have different multipliers
def generate(treasures = [], numWords = 10, numLetters = 16):
    Tiles = []
    Words = {}
    
    while True:
        tile = raw_input('Enter tile: ')
        if 1 <= len(tile) <= 3 and tile.isalpha():
            if tile in alphabet:
                letter = tile
                gem = 'n'
            elif tile[0] in alphabet:
                letter = tile[0]
                gem = tile[1]
            elif tile[:-1] == 'qu':
                letter = tile[:-1]
                gem = tile[-1]
            Tiles.append([letter, bonus(gem, treasures)])
        elif tile == '-':
            break
        elif tile == 'del':
            del Tiles[-1]
        else:
            print 'Try again.'
    
    Letters = []
    for tile in Tiles:
        Letters.append(tile[0])

    for word in dictionary:
        if all(Letters.count(a) >= word.count(a) for a in alphabet) \
        and len(word) <= numLetters:     
                Words[word] = [value(listify(word),Tiles,treasures), len(word)]
    
    if 'astropop' in Words:
        print 'Astropop!'
    
    return sorted(Words.iteritems(),key=operator.itemgetter(1),reverse=True)\
    [:numWords]

def quarterRound(x):
    return round(x*4)/4
    
def listify(word):
    List = list(word)
    if 'q' in List:
        while 'q' in List:
            List[List.index('q'):List.index('q') + 2] = \
            [''.join(List[List.index('q'):List.index('q') + 2])]
    return List
            
def wordify(List):
    word = ''
    for letter in List:
        word += letter
    return word
    
def bonus(gem, treasures):
    values = [0.15,0.2,0.25,0.3,0.35,0.5,1]
    if 'scimitar of justice' in treasures:
        for value in values:
            value += 0.1
    if gem == 'n':
        value = 0
    elif gem == 'v':
        value = values[0]
    elif gem == 'g':
        value = values[1]
    elif gem == 'b':
        value = values[2]
    elif gem == 'o':
        value = values[3]
    elif gem == 'r':
        value = values[4]
    elif gem == 'p':
        value = values[5]
    elif gem == 'w':
        value = values[6]
    return value
    
def value(word, Tiles, treasures):
    value = 0
    multiplier = 1
    elements = {}
    for letter in alphabet:
        elements[letter] = []
    values = [1,1.25,1.25,1,1,1.25,1,1.25,1,1.75,1.75,1,1.25,\
    1,1,1.25,2.75,1,1,1,1,1.5,1.5,2,1.5,2]
    
    if 'bow of zyx' in treasures:
        values[alphabet.index('x')] = 2.5
        values[alphabet.index('y')] = 2.5
        values[alphabet.index('z')] = 2.5
    if 'arch of xyzzy' in treasures:
        values[alphabet.index('x')] = 3
        values[alphabet.index('y')] = 3
        values[alphabet.index('z')] = 3
    if 'wooden parrot' in treasures:
        values[alphabet.index('r')] = 2
    
    for tile in Tiles:
        elements[tile[0]].append(tile[1])
    for letter in word:
        value += values[alphabet.index(letter)]
        multiplier += elements[letter].pop(elements[letter]\
        .index(max(elements[letter])))
    
    if 'hand of hercules' in treasures and word in metals:
        multiplier *= 1.5
    if 'tome of accidents' in treasures and word in colors:
        multiplier *= 2
    elif 'tablet of the ages' in treasures and word in colors:
        multiplier *= 2.5
    if 'wolfbane necklace' in treasures and word in mammals:
        multiplier *= 1.5
    elif 'slayer talisman' in treasures and word in mammals:
        multiplier *= 1.75
    if 'quadrumvir signet' in treasures and 'qua' in wordify(word):
        multiplier *= 1.5
    
    return quarterRound(math.ceil(value) * multiplier)
                    
def delete(Lists, words):
    '''List of words.'''
    Dictionary = dictionary
    if Lists == 'words':
        i = "/Users/Angel/Documents/Python/Lists/words2.txt"
    elif Lists == 'colors':
        i = "/Users/Angel/Documents/Python/Lists/colors.txt"
    elif Lists == 'metals':
        i = "/Users/Angel/Documents/Python/Lists/metals.txt"
    elif Lists == 'mammals':
        i = "/Users/Angel/Documents/Python/Lists/mammals.txt"
    for word in words:
        if word in Dictionary:
            Dictionary.remove(word)    
    f = open(i,"r+")
    for word in Dictionary:
        f.write("%s\n" % word.lower())
            
def merge(List):
    dic = dictionary
    for word in List:
        if word not in dic:
            dic.append(word)
    dic.sort()
    f = open("/Users/Angel/Documents/Python/Lists/words2.txt","r+")
    for word in dic:
        f.write("%s\n" % word.lower())