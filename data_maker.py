#!/bin/python3

# This python script uses nltk corpus and wordnet to generate dictionary files in json format
# It takes the words from words.txt file and finds definitions for them
# Then it generates json files for each Alphabet in data folder

# This script has been taken from https://github.com/tusharlock10/Dictionary and has been modified

from nltk.corpus import wordnet2021 as wn
from nltk import download
import json
download('wordnet2021')
download("wordnet")

TEXT_FILE_TO_USE = "words.txt"

L = []
f = open(TEXT_FILE_TO_USE)
data = f.read()
f.close()
L = data.split('\n')


D = {}

empty_words = []


for word in L:
    word = word.upper()
    # {WORD:{'MEANINGS':{...}, 'ANTONYMS':[...], 'SYNONYMS:[...]'}}
    D_word = {}

    # help(S[0])
    # 1/0

    ALL_TYPES = {'n': 'Noun', 'v': 'Verb',
                 'a': 'Adjective', 's': 'Adjective', 'r': 'Adverb'}

    # 'MEANINGS':{SENSE_NUM_1:[TYPE_1, MEANING, CONTEXT, EXAMPLE], SENSE_NUM_2:[TYPE_2, MEANING, CONTEXT, EXAMPLE]}'
    MEANINGS = {}
    SYNONYMS = set()
    ANTONYMS = set()
    sense = []
    S = wn.synsets(word)

    def get_context(syn):
        HYPERNYMS = syn.hypernyms()
        result = []
        for i in HYPERNYMS:
            temp = i.lemma_names()
            temp = [' '.join(i.capitalize().split('_')) for i in temp]
            result += temp

        return result

    for syn in S:
        t = ALL_TYPES[syn.pos()]  # type
        m = syn.definition()  # meaning
        c = get_context(syn)  # context
        e = syn.examples()  # examples

        for l in syn.lemmas():
            temp = ' '.join(l.name().capitalize().split('_'))
            SYNONYMS.add(temp)
            if l.antonyms():
                ANTONYMS.add(l.antonyms()[0].name())

        # Skips words which are not matching
        # syn_name = syn.name().split('.')[0].upper()
        # if syn_name != word:
        #     continue

        sense_num = int(syn.name().split('.')[-1])
        if sense_num in sense:
            continue

        temp = {sense_num: [t, m, c, e]}
        MEANINGS.update(temp)

    try:
        SYNONYMS.remove(word)
    except:
        pass
    try:
        ANTONYMS.remove(word)
    except:
        pass
    SYNONYMS, ANTONYMS = list(SYNONYMS)[:5], list(ANTONYMS)[:5]
    if MEANINGS != {} or SYNONYMS != []:
        D_word = {word: {'MEANINGS': MEANINGS,
                         'ANTONYMS': ANTONYMS, 'SYNONYMS': SYNONYMS}}
        D.update(D_word)
    else:
        empty_words += [word]


L = [chr(ord('A')+i) for i in range(26)]

L = L
for i in L:
    D2 = {}
    print(i)
    for word in D:
        if word[0].upper() == i:
            D2.update({word: D[word]})

    f = open(f'data/D{i}.json', 'w')
    data = json.dumps(D2)
    f.write(data)
    f.close()

f = open('data/empty_words.txt', 'w')
f.write('\n'.join(empty_words))
f.close()
