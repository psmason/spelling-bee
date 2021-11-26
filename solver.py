#!/usr/bin/env python3

import argparse
from collections import defaultdict
from itertools import chain, combinations

parser = argparse.ArgumentParser(description='NYT spelling bee solver')
parser.add_argument('--word_list', help='dictionary txt file of valid words')
parser.add_argument('--required_character', help='character required for all scored words')
parser.add_argument('--optional_characters', help='optional character for scored words')

args = parser.parse_args()

if len(args.required_character) != 1:
    raise Exception("required_character must be a single character")

if len(args.optional_characters) != 6:
    raise Exception("optional_characters must be six characters")

valid_words = []
with open(args.word_list) as word_list:
    valid_words = word_list.readlines()

print("number of valid words:", len(valid_words))

characters_to_words = defaultdict(list)
for word in valid_words:
    word = word.strip().lower()
    if len(word) < 4:
        # skipping words which are too short
        continue
    characters = "".join(sorted(set(word)))
    characters_to_words[characters].append(word)

# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset  
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

scored_words = []
permutations = powerset(set(args.optional_characters))
for optional_characters_permutation in permutations:
    if len(optional_characters_permutation) == 0:
        # skip empty set
        continue
    # combine required character with the optional permutation
    potential_character_set = "".join(sorted(list(args.required_character) + list(optional_characters_permutation)))
    if potential_character_set in characters_to_words:
        for valid_word in characters_to_words[potential_character_set]:
            scored_words.append(valid_word)

for scored_word in sorted(scored_words):
    print(scored_word)

