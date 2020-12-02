# Dialog Identifier
# Written by A.M. Yahya
# Accuracy: 66 - 67 %

from nltk.corpus import nps_chat
from Helper_Lib import serialize_object
import nltk

def dialog_feature_extractor(post):
  	features = {}
  	for word in nltk.word_tokenize(post):
  		features["contains(%s)" % word.lower()] = True
  	return features

def build_dialog_identifier(posts):
	featuresets = [(dialog_feature_extractor(post.text), post.get("class")) for post in posts]
  	size = int(len(featuresets) * 0.1)
  	train_set, test_set = featuresets[size:], featuresets[:size]
  	identifier = nltk.NaiveBayesClassifier.train(train_set)
  	print "Accuracy for dialog identifier is: ", nltk.classify.accuracy(identifier, test_set)
  	return identifier

posts = nltk.corpus.nps_chat.xml_posts()
dialog_identifier = build_dialog_identifier(posts)
print "Serializing dialog classifier for later use."
serialize_object(dialog_identifier, 'saved_objects/dialog_identifiers/dialog_identifier.pkl')
print "Serialization complete."
