# NLTK Practice file
# Written by A.M. Yahya
# Accuracy: 78 %

from nltk.corpus import names
from pickle import dump
import nltk
import random
import os

def gender_features(word):
	return {'last letter': word[-1]}

def get_names():
	ns = ([(str(name), 'male') for name in names.words('male.txt')] +
		  [(str(name), 'female') for name in names.words('female.txt')])
	random.shuffle(ns)
	return ns

def create_feature_set(names_list):
	return [(gender_features(n), g) for (n,g) in names_list]

def test_classifier(classifier, name_to_test):
	return classifier.classify(gender_features(name_to_test))

def Main():
	names_gender_list = get_names()
	feature_set = create_feature_set(names_gender_list)
	training_set, testing_set = feature_set[500:], feature_set[:500]
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	print "This classifiers accuracy is: ", nltk.classify.accuracy(classifier, testing_set)

	print classifier.show_most_informative_features(10)
	i = 0
	while i < 3:
		name_test =  raw_input("Enter a name to get gender: ")
		print test_classifier(classifier, name_test)
		i += 1

	print  "Serializing Classifier for later use..."
	output = open(os.path.join('./gender_classifier.pkl'), 'wb')
	dump(classifier, output, -1)
	output.close()

	print "Serialization completed"

Main()