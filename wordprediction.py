import pygtrie
import re

t = pygtrie.CharTrie()

def gen_data_structures(filename):
    reg = re.compile('[^a-zA-Z]')
    with open(filename) as f:
        for sentence in f:
            for word in sentence.split(" "):
                t[reg.sub('', word)] = True

def get_suffixes(query):
    return t.iterkeys(query)

gen_data_structures("tomsawyer.txt")

for word in get_suffixes('r'):
    print(word)
