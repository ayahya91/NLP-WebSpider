# Sentence Segmenter Test
# Written by A.M. Yahya

import nltk
from Helper_Lib import load_serialized_object
from nltk_sentence_segmenter import *

def segment_sent_main(sents, classifier):
	#sents = sents.replace('. ', "%$")
	#sents = sents.replace('? ', "%$")
	#sents = sents.replace('! ', "%$")
	#sents = sents.split('%$')
	#sentences, boundaries = tokenize_getBoundaries(sents)
	#feature_set = feature_sets(sentences, boundaries)
	start = 0
	sentences = []
	for i, sent in enumerate(sents):
		if sent in '.?!' and classifier.classify(sents, i) == True:
			sentences.append(sent[start:i + 1])
			start = i + 1
	if start < len(sents):
		sentences.append(sents[start:])

	# Formatting
	sentences = str(sentences)
	sentences = sentences.replace(r'\n', "")
	sentences = sentences.replace(r'\t', "").split("', '")
	sentences = [i.strip() + '.' for i in sentences]
	sentences[0] = sentences[0][3:]
	sentences[-1] =  sentences[-1][:-4] + sentences[-1][-1]

	return sentences

print("Loading classifier")
sent_segmenter_classifer = load_serialized_object('saved_objects/sentence_segmenter/sent_segmenter.pkl')
print("Classifier load.")
words = """The two areas overlap in many ways: data mining uses many 
		machine learning methods, but often with a slightly different
		goal in mind. On the other hand, machine learning also employs
		data mining methods as "unsupervised learning" or as a 
		preprocessing step to improve learner accuracy. Much of the 
		confusion between these two research communities (which do 
		often have separate conferences and separate journals, ECML
		PKDD being a major exception) comes from the basic assumptions 
		they work with: in machine learning, performance is usually 
		evaluated with respect to the ability to reproduce known 
		knowledge, while in Knowledge Discovery and Data Mining (KDD) 
		the key task is the discovery of previously unknown knowledge. 
		Evaluated with respect to known knowledge, an uninformed 
		(unsupervised) method will easily be outperformed by supervised 
		methods, while in a typical KDD task, supervised methods cannot 
		be used due to the unavailability of training data. Machine 
		learning also has intimate ties to optimization: many learning 
		problems are formulated as minimization of some loss function on 
		a training set of examples. Loss functions express the discrepancy 
		between the predictions of the model being trained and the actual 
		problem instances (for example, in classification, one wants to 
		assign a label to instances, and models are trained to correctly 
		predict the pre-assigned labels of a set examples). The difference 
		between the two fields arises from the goal of generalization: while 
		optimization algorithms can minimize the loss on a training set, 
		machine learning is concerned with minimizing the loss on unseen 
		samples."""

sentences = segment_sent_main(words, sent_segmenter_classifer)
print("Sentences are: ")
for i in sentences:
	print(i, '\n') 





