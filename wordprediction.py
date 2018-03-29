from ngram import NGram
import pygtrie
import re

t = pygtrie.CharTrie()
n = NGram()

# Assume one word per line, like linux words
def gen_trie(filename):
    with open(filename) as f:
        for word in f:
			t[word] = True
				
# In progress
def gen_ngrams(filename):
	reg = re.compile('[^a-zA-Z]')
	with open(filename) as f:
		for sentence in f:
			for w in sentence.split(" "):
				word = reg.sub('', w)

def get_suffixes(query):
    return t.iterkeys(query)

gen_trie("words")
gen_ngrams("tomsawyer.txt")

for word in get_suffixes('comp'):
    print(word)
