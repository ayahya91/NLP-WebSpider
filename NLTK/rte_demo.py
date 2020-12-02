# DEMO 

from nltk.corpus import rte
import nltk
from nltk.classify.util import accuracy

def ne(token):
    """
    This just assumes that words in all caps or titles are
    named entities.

    :type token: str
    """
    if token.istitle() or token.isupper():
        return True
    return False

def lemmatize(word):
    """
    Use morphy from WordNet to find the base form of verbs.
    """
    lemma = nltk.corpus.wordnet.morphy(word, pos='verb')
    if lemma is not None:
        return lemma
    return word

class RTEFeatureExtractor(object):
    """
    This builds a bag of words for both the text and the hypothesis after
    throwing away some stopwords, then calculates overlap and difference.
    """
    def __init__(self, rtepair, stop=True, lemmatize=False):
        """
        :param rtepair: a ``RTEPair`` from which features should be extracted
        :param stop: if ``True``, stopwords are thrown away.
        :type stop: bool
        """
        self.stop = stop
        self.stopwords = set(['a', 'the', 'it', 'they', 'of', 'in', 'to', 'is',
                              'have', 'are', 'were', 'and', 'very', '.', ','])

        self.negwords = set(['no', 'not', 'never', 'failed', 'rejected',
                             'denied'])
        # Try to tokenize so that abbreviations like U.S.and monetary amounts
        # like "$23.00" are kept as tokens.
        from nltk.tokenize import RegexpTokenizer
        tokenizer = RegexpTokenizer('([A-Z]\.)+|\w+|\$[\d\.]+')

        #Get the set of word types for text and hypothesis
        self.text_tokens = tokenizer.tokenize(rtepair.text)
        self.hyp_tokens = tokenizer.tokenize(rtepair.hyp)
        self.text_words = set(self.text_tokens)
        self.hyp_words = set(self.hyp_tokens)

        if lemmatize:
            self.text_words = set(lemmatize(token) for token in self.text_tokens)
            self.hyp_words = set(lemmatize(token) for token in self.hyp_tokens)

        if self.stop:
            self.text_words = self.text_words - self.stopwords
            self.hyp_words = self.hyp_words - self.stopwords

        self._overlap = self.hyp_words & self.text_words
        self._hyp_extra = self.hyp_words - self.text_words
        self._txt_extra = self.text_words - self.hyp_words


    def overlap(self, toktype, debug=False):
        """
        Compute the overlap between text and hypothesis.

        :param toktype: distinguish Named Entities from ordinary words
        :type toktype: 'ne' or 'word'
        """
        ne_overlap = set(token for token in self._overlap if ne(token))
        if toktype == 'ne':
            if debug:
                print("ne overlap", ne_overlap)
            return ne_overlap
        elif toktype == 'word':
            if debug:
                print("word overlap", self._overlap - ne_overlap)
            return self._overlap - ne_overlap
        else:
            raise ValueError("Type not recognized:'%s'" % toktype)

    def hyp_extra(self, toktype, debug=True):
        """
        Compute the extraneous material in the hypothesis.

        :param toktype: distinguish Named Entities from ordinary words
        :type toktype: 'ne' or 'word'
        """
        ne_extra = set(token for token in self._hyp_extra if ne(token))
        if toktype == 'ne':
            return ne_extra
        elif toktype == 'word':
            return self._hyp_extra - ne_extra
        else:
            raise ValueError("Type not recognized: '%s'" % toktype)


def rte_features(rtepair):
    extractor = RTEFeatureExtractor(rtepair)
    features = {}
    features['alwayson'] = True
    features['word_overlap'] = len(extractor.overlap('word'))
    features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
    features['ne_overlap'] = len(extractor.overlap('ne'))
    features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
    features['neg_txt'] = len(extractor.negwords & extractor.text_words)
    features['neg_hyp'] = len(extractor.negwords & extractor.hyp_words)
    return features

def demo_features():
    pairs = nltk.corpus.rte.pairs(['rte1_dev.xml'])[:6]
    for pair in pairs:
        print()
        for key in sorted(rte_features(pair)):
            print("%-15s => %s" % (key, rte_features(pair)[key]))


def demo_feature_extractor():
    rtepair = nltk.corpus.rte.pairs(['rte3_dev.xml'])[33]
    extractor = RTEFeatureExtractor(rtepair)
    print(extractor.hyp_words)
    print(extractor.overlap('word'))
    print(extractor.overlap('ne'))
    print(extractor.hyp_extra('word'))


def demo():
#    try:
#        nltk.config_megam('/usr/local/bin/megam')
#        trainer = lambda x: nltk.MaxentClassifier.train(x, 'megam')
#    except ValueError:
#        try:
#            trainer = lambda x: nltk.MaxentClassifier.train(x, 'BFGS')
#        except ValueError:
#            trainer = nltk.MaxentClassifier.train
    trainer = nltk.MaxentClassifier.train
    nltk.classify.rte_classifier(trainer)


demo_features()
demo_feature_extractor()
demo()