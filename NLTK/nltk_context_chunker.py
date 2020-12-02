# Context Chunker
# Written by A.M. Yahya
# Accuracy: TBD
### FAULT SCRIPT ###

import nltk, os, time
from nltk.corpus import conll2000
from nltk.classify.maxent import MaxentClassifier
from nltk import config_megam
from Helper_Lib import serialize_object

#nltk.config_megam('megam_i686.opt')

class ConsecutiveNPChunkTagger(nltk.TaggerI):
	def __init__(self, train_sents):
		train_set = []
		nltk.config_megam('/home/ahmed/nltk_data/MEGAM/megam-64.opt')
		for tagged_sent in train_sents:
			untagged_sent = nltk.tag.untag(tagged_sent)
			history = []
			for i, (word, tag) in enumerate(tagged_sent):
				featureset = self.npchunk_features(untagged_sent, i, history)
				train_set.append( (featureset, tag) )
				history.append(tag)
		self.classifier = nltk.MaxentClassifier.train(train_set, algorithm='megam', trace=0)

	def tag(self, sentence):
		history = []
		for i, word in enumerate(sentence):
			featureset = self.npchunk_features(sentence, i, history)
			tag = self.classifier.classify(featureset)
			history.append(tag)
		return zip(sentence, history)

	def npchunk_features(self, sentence, i, history):
		word, pos = sentence[i]
		if i == 0:
			prevword, prevpos = "<START>", "<START>"
		else:
			prevword, prevpos = sentence[i-1]
		if i == len(sentence)-1:
			nextword, nextpos = "<END>", "<END>"
		else:
			nextword, nextpos = sentence[i+1]
		return {"pos": pos,
			    "word": word,
			    "prevpos": prevpos,
			    "nextpos": nextpos,
				"prevpos+pos": "%s+%s" % (prevpos, pos),
				"pos+nextpos": "%s+%s" % (pos, nextpos), 
				"tags-since-dt": self.tags_since_dt(sentence, i)}

	def tags_since_dt(self, sentence, i):
		tags = set()
		for word, pos in sentence[:i]:
			if pos == 'DT':
				tags = set()
			else:
				tags.add(pos)
		return '+'.join(sorted(tags))

class ConsecutiveNPChunker(nltk.ChunkParserI):
	def __init__(self, train_sents):
		tagged_sents = [[((w,t),c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)]
						for sent in train_sents]
		self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

	def parse(self, sentence):
		tagged_sents = self.tagger.tag(sentence)
		conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
		return nltk.chunk.conlltags2tree(conlltags)

def main():
	print("Pulling Lexical Corpus...")
	test_sents = conll2000.chunked_sents('test.txt', chunk_types = ['NP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types = ['NP'])
	print("\nTraining Chunker...")
	start_time = time.time()
	context_chunker = ConsecutiveNPChunker(train_sents)
	print("\nTime elapsed for training: " + str(time.time() - start_time))
	print("\nTesting...")
	print("\nTesting Length: " + str(len(test_sents)))
	start_time = time.time()
	print(context_chunker.evaluate(test_sents))
	print("\nTime elapsed for testing: " + str(time.time() - start_time))
	print("\nSaving Trigram Chunker")
	serialize_object(context_chunker, 'saved_objects/chunker/context_chunker.pkl')
	print("\nTrigram chunker successfully saved")

main()
