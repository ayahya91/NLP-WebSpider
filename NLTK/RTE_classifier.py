# Recognizing Textual Entailment
# Written by A.M. Yahya
# Accuracy:
# Not completed: Insufficient documentation

from nltk.corpus import rte 
import nltk

def rte_feature_extractor(rtepair):
	return nltk.RTEFeatureExtractor(rtepair) 
	#add .similar() words to hyp_extra('word' and 'ne')

def rte_features(rtepair):
	extractor = rte_feature_extractor(rtepair)
	features = {}
	features['word_overlap'] = len(extractor.overlap('word'))
	features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
	features['ne_overlap'] = len(extractor.overlap('ne'))
	features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
	return features

def Main(rtepair):
	features = rte_features(rtepair)
	trainer = nltk.MaxentClassifier.train
	#trainer = nltk.MaxentClassifier.train
	classifier = nltk.rte_classifier(trainer, features)
	#size = int(len(rte_features)*0.1)
	#train_set, test_set = rte_features[size:], rte_features[:size]
	#classifier = nltk.rte_classifier([], train_set) #nltk.NaiveBayesClassifier(train_set)
	#print "Accuracy is: ", nltk.classify.rte_classify(classifier)

rtepair = nltk.corpus.rte.pairs(['rte3_dev.xml'])[33]
Main(rtepair)