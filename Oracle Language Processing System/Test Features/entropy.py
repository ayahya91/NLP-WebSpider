
import math
import nltk

def calculate_entropy(labels):
	freqDist = nltk.FreqDist(labels)
	probs = [freqDist.freq(l) for l in freqDist]
	return -sum([p * math.log(p,2) for p in probs])