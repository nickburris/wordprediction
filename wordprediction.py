import nltk
import time
from collections import defaultdict
import pygtrie
import re
import os

# TODO set up flags
verbose = True

t = pygtrie.CharTrie() # trie
ngrams = {} # ngrams
c = defaultdict(int) # counts

# Assume one word per line, like linux words
def gen_trie(filename):
	with open(filename, encoding="utf8") as f:
		for word in f:
			w = word.rstrip().lower()
			if(w != ''):
				t[w] = True
				
# Generate bigrams and trigrams for the input text
# TODO shouldn't read entire files into memory
def gen_ngrams(dirname):
	reg = re.compile('[^a-zA-Z]')
	# Read in the words from the text
	words = []
	for filename in os.listdir(dirname):
		with open(dirname + "/" + filename, encoding="utf8") as f:
			for sentence in f:
				for w in sentence.split(" "):
					w = reg.sub('', w).lower()
					if(w != ''):
						# Add word if not in dictionary
						if not is_whole_word(w):
							# TODO look at the words it's adding, lots are weird and should be prevented
							#print("adding " + w)
							t[w] = True
						words.append(w)
						c[w] += 1
	
	# Count bigrams and trigrams
	n = nltk.ngrams(words, 3)
	for tu in n:
		if tu[0] not in ngrams:
			ngrams[tu[0]] = {}
		if tu[1] not in ngrams[tu[0]]:
			ngrams[tu[0]][tu[1]] = {}
			ngrams[tu[0]][tu[1]]["_count"] = 0
		if tu[2] not in ngrams[tu[0]][tu[1]]:
			ngrams[tu[0]][tu[1]][tu[2]] = {}
			ngrams[tu[0]][tu[1]][tu[2]]["_count"] = 0
			
		# Count the bigram and trigram
		ngrams[tu[0]][tu[1]][tu[2]]["_count"] += 1
		ngrams[tu[0]][tu[1]]["_count"] += 1

def get_suffixes(query):
	return t.iterkeys(query)

def is_whole_word(w):
	return t.has_key(w.lower())

# Get the top word completions
# If just partial is passed, return the most common completions
# If last and possibly second_last are passed, return completions ranked by ngrams
def get_completions(partial, last = '', second_last = ''):
	COUNT = 10
	completions = None
	if last == '' and second_last == '':
		# Just return the most common completions
		completions = sorted([(w, c[w]) for w in get_suffixes(partial) if w in c],
							key=lambda w: c[w[0]],
							reverse=True)[:COUNT]
							
	elif last != '' and second_last == '':
		# Return completions based on last word
		completions = sorted([(w, ngrams[last][w]["_count"]) for w in get_suffixes(partial) 
								if last in ngrams 
								and w in ngrams[last] 
								and "_count" in ngrams[last][w]],
							key=lambda w: ngrams[last][w[0]]["_count"],
							reverse=True)[:COUNT]
	elif last != '' and second_last != '':
		# Return completions based on last 2 words
		completions = sorted([(w, ngrams[second_last][last][w]["_count"]) for w in get_suffixes(partial)
								if second_last in ngrams 
								and last in ngrams[second_last] 
								and w in ngrams[second_last][last] 
								and "_count" in ngrams[second_last][last][w]],
							key=lambda w: ngrams[second_last][last][w[0]]["_count"],
							reverse=True)[:COUNT]
	
	# try weaker search if nothing was found
	if len(completions) == 0:
		if second_last != '':
			completions = get_completions(partial, last)
		elif last != '':
			completions = get_completions(partial)
	
	# completions is a sorted list of (word, ngram-count) tuples
	return completions

def time_millis():
	return int(round(time.time()*1000))
#--------------- Start demo ---------------

start_millis = time_millis()

gen_trie("words")
gen_ngrams("train_english")

if(verbose):
	print("Generating structures took " + str((time_millis() - start_millis)) + "ms");

while True:
	in_words = input('---------------------------\n' +
					 'Enter word or partial word: ').strip().lower().split(" ")
	
	last_w = ''
	second_last_w = ''
	third_last_w = ''
	if len(in_words) == 0:
		continue
	elif len(in_words) == 1:
		last_w = in_words[0]
	elif len(in_words) == 2:
		last_w = in_words[-1]
		second_last_w = in_words[-2]
	else:
		last_w = in_words[-1]
		second_last_w = in_words[-2]
		third_last_w = in_words[-3]
			  
	if is_whole_word(last_w): # If last_w was a whole word
		print("Whole word detected. Here are the top next word predictions:")
		if is_whole_word(second_last_w) and second_last_w in ngrams and last_w in ngrams[second_last_w]:
			print("Based on last 2 words (best prediction):")
			print(', '.join(sorted([k for k,_ in ngrams[second_last_w][last_w].items() 
										if k != "_count" and "_count" in ngrams[second_last_w][last_w][k]], 
									key=lambda k: ngrams[second_last_w][last_w][k]["_count"], 
									reverse=True)[:10]))	
		elif last_w in ngrams:
			print("Based on last word (weak prediction):")
			print(', '.join(sorted([k for k,_ in ngrams[last_w].items() if "_count" in ngrams[last_w][k]], 
									key=lambda k: ngrams[last_w][k]["_count"], 
									reverse=True)[:10]))
		else:
			print("No word predictions.")
		
		print()
	else:
		print("Partial word detected.\n")
	
	print("Here are the word completion predictions:")
	print(', '.join([c[0] for c in get_completions(partial=last_w, last=second_last_w, second_last=third_last_w)]))
	
	print()
