# Helper Library
# Written by A.M. Yahya
#import _pickle as pickle
from _pickle import dump, load
import os, math

def serialize_object(object_to_save, obj_type = 'tag', pkl_filepath = 'serializedObject.pkl'):
	if obj_type == 'tag':
		output = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/taggers/' + pkl_filepath, 'wb')
	elif obj_type == 'chunk':
		output = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/chunker/' + pkl_filepath, 'wb')
	elif obj_type == 'diag_id':
		output = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/dialog_identifiers/' + pkl_filepath, 'wb')
	elif obj_type == 'sent_seg':
		output = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/sentence_segmenter/' + pkl_filepath, 'wb')
	else:
		output = open( '/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/other/' + pkl_filepath, 'wb')
	dump(object_to_save, output, -1)
	output.close()

def load_serialized_object(pkl_filepath, obj_type = 'tag'):
	if obj_type == 'tag':
		input_file = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/taggers/' + pkl_filepath, 'rb')
	elif obj_type == 'chunk':
		input_file = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/chunker/' + pkl_filepath, 'rb')
	elif obj_type == 'diag_id':
		input_file = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/dialog_identifiers/' + pkl_filepath, 'rb')
	elif obj_type == 'sent_seg':
		input_file = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/sentence_segmenter/' + pkl_filepath, 'rb')
	else:
		input_file = open('/home/ahmed/Desktop/Oracle/Oracle Language Processing System/saved_objects/other/' + pkl_filepath, 'rb')
	loaded_object = load(input_file)
	input_file.close()
	return loaded_object

def entropy(labels):
	freqdist = nltk.FreqDist(labels)
	probs = [freqdist.freq(l) for l in nltk.FreqDist(labels)]
	return -sum([p * math.log(p,2) for p in probs])
