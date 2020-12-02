# Helper Library
# Written by A.M. Yahya

from pickle import dump, load
import os, math

def serialize_object(object_to_save, pkl_filepath = 'serializedObject.pkl'):
	output = open(os.path.join('./' + pkl_filepath), 'wb')
	dump(object_to_save, output, -1)
	output.close()

def load_serialized_object(pkl_filepath):
	input_file = open(os.path.join('./' + pkl_filepath), 'rb')
	loaded_object = load(input_file)
	input_file.close()
	return loaded_object

def entropy(labels):
	freqdist = nltk.FreqDist(labels)
	probs = [freqdist.freq(l) for l in nltk.FreqDist(labels)]
	return -sum([p * math.log(p,2) for p in probs])