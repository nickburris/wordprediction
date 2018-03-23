# Word prediction and completion
A Perl implementation of word prediction and completion, created for CSCI 4152 Natural Language Processing. 

The initial program will take a word or partial word as input, and either provide a suggestion for completion or suggest the next word:
- If the input word is in the dictionary, predict the next word using an ngram model.
- If the input word is not in the dictionary, check the suffix tree for a list of possible completions, and apply a metric to choose the best one.
