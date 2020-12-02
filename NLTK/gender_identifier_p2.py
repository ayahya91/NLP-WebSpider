# NLTK Practice file
# Written by A.M. Yahya
# Accuracy: 78 % (same as gender_indentifier.py)

from nltk.corpus import names
from pickle import load
import nltk
import random
import os

def gender_features(word):
	return {'last letter': word[-1]}

def test_classifier(classifier, name_to_test):
	return classifier.classify(gender_features(name_to_test))

def Main():
	print "Loading Classifier"

	input_file = open(os.path.join('./gender_classifier.pkl'), 'rb')
	classifier = load(input_file)
	input_file.close()

	while True:
		name_test =  raw_input("Enter a name to get gender: ")
		print test_classifier(classifier, name_test)

Main()