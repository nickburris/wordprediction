from nltk import ngrams
import pygtrie
import re

t = pygtrie.CharTrie()
n = None

# Assume one word per line, like linux words
def gen_trie(filename):
	global t
	with open(filename) as f:
		for word in f:
			t[word] = True
				
# In progress
def gen_ngrams(filename, num):
	global n
	reg = re.compile('[^a-zA-Z]')
	words = []
	with open(filename) as f:
		for sentence in f:
			for w in sentence.split(" "):
				word = reg.sub('', w)
				words.append(word)
	n = ngrams(words, num)

def get_suffixes(query):
	return t.iterkeys(query)

gen_trie("words")
gen_ngrams("tomsawyer.txt", 3)

trigrams = {}

for trigram in n:
	try:
		# Count the trigram
		trigrams[trigram[0]][trigram[1]][trigram[2]]["_count"] += 1
	except KeyError, err:
		trigrams[trigram[0]][trigram[1]][trigram[2]]["_count"] = 1
	
	try:
		# Also count the bigram
		trigrams[trigram[0]][trigram[1]]["_count"] += 1
	except KeyError, err:
		trigrams[trigram[0]][trigram[1]]["_count"] = 1

print(trigrams)

#for word in get_suffixes('comp'):
	#print(word)
