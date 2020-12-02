# Tagger 
# Written by A.M. Yahya
# Accuracy: 92.1810558152 - 92.247309704 %

from nltk.corpus import brown
from Helper_Lib import serialize_object
import nltk, random

def build_tagger(training_sents):
	dt = nltk.DefaultTagger('NN')
	ut = nltk.UnigramTagger(training_sents, cutoff = 0, backoff = dt)	#7
	bt = nltk.BigramTagger(training_sents, cutoff = 0, backoff = ut)	#5
	tt = nltk.TrigramTagger(training_sents, cutoff = 0, backoff = bt)	#3
	qt = nltk.NgramTagger(4, training_sents, cutoff = 0, backoff = tt)	#2
	qt2 = nltk.NgramTagger(5, training_sents, cutoff = 0, backoff = qt)	#1
	return qt2, qt, tt, bt, ut, dt

def build_train_test_sets():
	print "Building training and testing sets..."
	train_set, test_set = [], []
	for i in brown.categories():
		tagged_sents = list(brown.tagged_sents(categories = i))
		random.shuffle(tagged_sents)
		test_size = int(len(tagged_sents)*0.1)
		train_set.extend(tagged_sents[test_size:])
		test_set.extend(tagged_sents[:test_size])
	random.shuffle(train_set)
	random.shuffle(test_set)
	print "Training and testing sets successfully built"
	return train_set, test_set

def train_tagger():
	train_sents, test_sents = build_train_test_sets()
	print "Building and training taggers, please wait..."
	taggers = build_tagger(train_sents)
	print "Tagger trained, testing..."
	print "Accuracy on test data is: ", taggers[0].evaluate(test_sents)
	return taggers	


def test_tagger(tagger, unseen_sent):
	return tagger.tag(unseen_sent)

def Main():
	taggers = train_tagger()
	
	i = 0
	while i < 2:
		sent = raw_input("Please enter a sentence to tag: ")
		sent = sent.split()
		print test_tagger(taggers[0], sent)
		i += 1
	
	print "Serializing tagger for later use, please wait..."
	serialize_object(taggers[5], 'saved_objects/taggers/default_tagger.pkl')
	serialize_object(taggers[4], 'saved_objects/taggers/unigram_tagger.pkl')
	serialize_object(taggers[3], 'saved_objects/taggers/bigram_tagger.pkl')
	serialize_object(taggers[2], 'saved_objects/taggers/trigram_tagger.pkl')
	serialize_object(taggers[1], 'saved_objects/taggers/quadrigram_tagger.pkl')
	serialize_object(taggers[0], 'saved_objects/taggers/quintigram_tagger.pkl')
	print "Serialization complete"

Main()