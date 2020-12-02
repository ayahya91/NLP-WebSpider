# Sentence Segmentation
# Written by A.M. Yahya
# Accuracy: 93.602 % (pretty useless, should just split along '.?!'')

import nltk
from nltk.corpus import treebank_raw	# just data_set
from Helper_Lib import serialize_object

def tokenize_and_getBoundaries(sents, sentences = [], boundaries = set()):
	offset = 0
	for sent in sents:
		sentences.extend(sent)
		offset += len(sent)
		boundaries.add(offset-1)
	return sentences, boundaries

def punct_features(sentences, i):
	return {'next_word_capitialized': sentences[i + 1][0].isupper(),
			'prev_word': sentences[i - 1].lower(),
			'punct': sentences[i],
			'prev_word_is_one_char': len(sentences[i - 1]) == 1}

def feature_sets(sentences, boundaries):
	return [(punct_features(sentences, i), (i in boundaries))
	 for i in range(1, len(sentences) - 1) if sentences[i] in '.?!']

def build_sent_segmenter_classifer(train_set):
	return nltk.NaiveBayesClassifier.train(train_set)

# getting data
sents = nltk.corpus.treebank_raw.sents()

# Variable declaration
# sentences : Will hold every token in sents
# boundaries : this will hold the last letter of ever sentence
def Main():
	sentences, boundaries = tokenize_and_getBoundaries(sents)
	feature_set =  feature_sets(sentences, boundaries)

	size = int(len(feature_set)* 0.1)
	train_set, test_set = feature_set[size:], feature_set[:size]
	sent_segmenter_classifier = build_sent_segmenter_classifer(train_set)
	print("Accuracy is: ", nltk.classify.accuracy(sent_segmenter_classifier, test_set))
	print("Saving classifier...")
	serialize_object(sent_segmenter_classifier, 'saved_objects/sentence_segmenter/sent_segmenter.pkl')
	print("Classifier saved.")

Main()
