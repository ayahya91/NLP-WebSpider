# Bigram Chunker 
# Written by A.M. Yahya
# Accuracy: 
#	IOB Accuracy:  93.3%
#   Precision:     82.3%
#   Recall:        86.8%
#   F-Measure:     84.5%


import nltk
from nltk.corpus import conll2000
from Helper_Lib import serialize_object

class BigramChunker(nltk.ChunkParserI):
	def __init__(self, training_sents):
		training_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
						for sent in training_sents]
		self.tagger = nltk.BigramTagger(training_data)

	def parse(self, sentence):
		pos_tags = [pos for (word, pos) in sentence]
		tagged_pos_tags = self.tagger.tag(pos_tags)
		chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
		conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
					in zip(sentence,chunktags)]
		return nltk.chunk.conlltags2tree(conlltags)

def main():
	test_sents = conll2000.chunked_sents('test.txt', chunk_types = ['NP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types = ['NP'])
	bigram_chunker = BigramChunker(train_sents)
	print(bigram_chunker.evaluate(test_sents))
	print("Saving Bigram Chunker...")
	serialize_object(bigram_chunker, 'saved_objects/chunker/bigram_chunker.pkl')
	print("Bigram chunker successfully saved")

main()