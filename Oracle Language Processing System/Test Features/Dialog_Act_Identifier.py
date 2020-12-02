
import nltk

posts = nltk.corpus.nps_chat.xml_posts()[:10000]

def dialog_act_features(post):
	features = {}
	for word in nltk.word_tokenize(post):
		features['contains(%s)' % word.lower()] = True
	return features

print("Creating Feature Set...")
featuresets = [(dialog_act_features(post.text), post.get('class')) for post in posts]
test_size = int(len(featuresets) * 0.1)
train_set, test_set =  featuresets[test_size:], featuresets[:test_size]
print("Training Classifier...")
classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Classifier Accuracy is: ", nltk.classify.accuracy(classifier, test_set))
