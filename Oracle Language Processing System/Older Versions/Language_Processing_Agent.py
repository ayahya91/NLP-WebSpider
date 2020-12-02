
'''
	Oracle Language Processing Agent v1
	Status: Functional
	Written By Ahmed Mused Yahya

	Language Processing Agent:
		mem_vars = [word_contractions]
		mem_fun = [load_tagger_chunker, read_source, normalize_text, sentence_segmenter, tokenizer, context_chunk_text, main]

	Model:
	Speech Analysis -> Morphological and Lexical Analysis -> Parsing ->
	Contextual Reasoning -> Application Reasoning and Execution ->
	Utterance Planning -> Syntactic Realization -> Morpholoical Realization ->
	Speech Synthesis

	Improvements: 
	Possibly Add Preproposition Lookup Table

	Alternatives:
		Chose this or context_chunker
			chunk_grammar = r"""
				NP: {<DT|PP\$>?<JJ.*>*<NN.*>+}		# chunk determiner/possessive adjective and nouns
				NP:	{<DT|JJ|NN.*>+}					# chunk determiner/possessive adjective and nouns
				PP: {<IN><NP>}						# chunk prepositions followed by NP
				VP: {<VB.*><NP|PP|CLAUSE>+$}		# chunk verbs and their arguments
				CLAUSE: {<NP><VP>}					# chunk NP, VP
			"""
			chunk_parser = nltk.RegexpParser(chunk_grammar, loop=2)
			chunk_results = [chunk_parser.parse(tagged_sent) for tagged_sent in tagged_sents]

		Named Entity Weeder
			named_entities_dict = dict()
			false_ne = []
			for i in named_entities:
				ne = str(i[1:-1])
				ne_components = ne.split(" ")
				ne_type = ne_components[0]
				ne = ' '.join(ne_components[1:])
				if ne not in false_ne:
					if ne in named_entities_dict:
						if named_entities_dict[ne] != ne_type:
							del named_entities_dict[ne]
							false_ne.append(ne)
						else:
							continue
					else:
						named_entities_dict[ne] = ne_type
				else:
					continue
			print("\nFalse Positives: ", len(false_ne), false_ne)
'''
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!! INCORPORATE META DATA!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


import nltk, re, itertools, sys, os, datetime
from bs4 import BeautifulSoup
from Helper_Lib import *
from NERC import *
from generate_context_chunker import *
from urllib.request import urlopen  
from urllib.parse import urlparse
######################################

class Language_Processing_Agent:
	word_contractions = {"aren't" : "are not", "ain't" : "am not", "can't" : "cannot", "couldn't" : "could not", 
						 "didn't" : "did not", "doesn't" : "does not", "don't" : "do not", "hadn't" : "had not",
						 "hasn't" : "has not", "haven't" : "have not", "he'd" : ["he had","he would"], "he'll" : "he will",
						 "he's" : ["he is","he has"], "i'd" : ["i had","i would"], "i'll" : "i will", "i'm" : "i am",
						 "i've" : "i have", "isn't" : "is not", "it's" : "it is", "let's" : "let us", "mightn't" : "might not",
						 "mustn't" : "must not", "shan't" : "shall not", "she'd" : ["she had","she would"], "she'll" : "she will",
						 "she's" : ["she is","she has"], "shouldn't" : "should not", "that's" : ["that is","that has"],
						 "there's" : ["there is","there has"], "they'd" : "they would", "they'll" : "they will",
						 "they're" : "they are", "they've" : "they have", "we'd" : ["we had","we would"], "we're" : "we are",
						 "we've" : "we have", "weren't" : "were not", "what'll" : "what will", "what're" : "what are",
						 "what's" : "what is", "what've" : "what have", "where's" : "where is", "who'd" : "who would",
						 "who'll" : "who will", "who're" : "who are", "who's" : "who is", "who've" : "who have",
						 "won't" : "will not", "wouldn't" : "would not", "you'd" : "you had", "you'll" : "you will",
						 "you're" : "you are", "you've" : "you have"}

	def __init__(self, source, options=None):
		self.LPA_log = open(os.getcwd() + "/LPA Logs/lpa_log_" + str(datetime.datetime.today()) + ".txt", "w")
		self.load_tagger_chunker()
		self.keep_alive = 'y'
		while self.keep_alive != 'q':
			ret_code = self.main(source)
			if ret_code != 0:
				print("Good Bye.")
				break
			self.keep_alive = input("Would you like to continue using the Oracle Language Processing Agent\n('q' to quit, anything else to continue): ")
			if self.keep_alive != 'q':
				source = input("Please input another text source: ")
			else:
				print("Good Bye.")

	def load_tagger_chunker(self):
		self.LPA_log.write("Loading Internal Tagger...\n")														# Load Tagger/Chunker
		print("\nLoading Internal Tagger...")
		dt = load_serialized_object('default_tagger.pkl', 'tag')
		ut = load_serialized_object('unigram_tagger.pkl', 'tag')
		bt = load_serialized_object('bigram_tagger.pkl', 'tag')
		tt = load_serialized_object('trigram_tagger.pkl', 'tag')
		qt = load_serialized_object('quadrigram_tagger.pkl', 'tag')
		qt2 = load_serialized_object('quintigram_tagger.pkl', 'tag')
		self.tagger = [qt2, qt, tt, bt, ut, dt]

		self.LPA_log.write("Loading Internal Chunker...\n")
		print("\nLoading Internal Chunker...")
		self.context_chunker = load_serialized_object('context_chunker.pkl', 'chunk')

	def read_source(self, source):															# Read URL's or File Path
		try:
			response = urlopen(source)
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("utf-8")
			parsed_html = BeautifulSoup(htmlString, 'html.parser')
			for script in parsed_html(["script", "style"]):
				script.extract()
			raw_text = str(parsed_html.get_text())
			self.LPA_log.write("\nVisiting: " + source + "\n")
		except ValueError:  # invalid URL
			try:
				with open(source, 'r') as content_file:
					content = content_file.read()
				raw_text = content
				self.LPA_log.write("\nVisiting: " + source + "\n")
			except:
				return "Invalid source"
		return raw_text

	def normalize_text(self, raw_text):												# Resolve Word Contractions, normalize
		print("\nNormalizing Text...")
		lines = (line.strip() for line in raw_text.splitlines())							# break into lines and remove leading and trailing space on each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))			# break multi-headlines into a line each
		raw_text = '\n'.join(chunk for chunk in chunks if chunk)							# drop blank lines

		print("\nResolving Word Contractions...")
		for i in list(Language_Processing_Agent.word_contractions):
			current_word_contraction = re.compile(re.escape(i), re.IGNORECASE)
			if type(Language_Processing_Agent.word_contractions[i]) is list:
				# Do Something Here !!!!!!!!!!! 
				normalized_text = current_word_contraction.sub(Language_Processing_Agent.word_contractions[i][0], raw_text)
			else:
				normalized_text = current_word_contraction.sub(Language_Processing_Agent.word_contractions[i], raw_text)
		return normalized_text

	def sentence_segmenter(self, string):													# Sentence Segmenter
		print("\nSegmenting Sentences...")
		sentences = nltk.sent_tokenize(string)
		return sentences

	def tokenizer(self, string):															# Tokenization
		print("\nTokenizing Sentences...")
		tokenized_sents = [nltk.word_tokenize(sent) for sent in string]					#tokenized_text = nltk.Text(tokens)		# This line is not necessary
		return tokenized_sents

	def pos_tag_text(self, tokenized_text):														# Tagging
		print("\nTagging Sentences...")
		tagged_sents = [self.tagger[0].tag(tokens) for tokens in tokenized_text]
		return tagged_sents

	def context_chunk_text(self, tagged_sents):													# Chunking
		print("\nChunking Text...")
		context_chunker_result = [self.context_chunker.parse(tagged_sent) for tagged_sent in tagged_sents]
		return context_chunker_result

	# Should probably be own class
	def named_entity_recognition_classification(self, tagged_sents):					# Extract Named Entities
		nerc = Named_Entity_Classifier(tagged_sents)
		self.LPA_log.write('*'*60 + '\n')
		self.LPA_log.write("Named Entity Classifier Results \n")
		self.LPA_log.write('*'*60 + '\n')
		self.LPA_log.write("\nBaseline NE:\n" + str(nerc.named_entities) + "\n")
		self.LPA_log.write("\nRegex NE:\n" + str(nerc.regex_chunks) + "\n")
		self.LPA_log.write('*'*60 + '\n')

	def main(self, source):
		raw_text = self.read_source(source)
		if raw_text == "Invalid source":
			return 1
		normalized_text = self.normalize_text(raw_text)
		sentences = self.sentence_segmenter(normalized_text)
		tokenized_sents = self.tokenizer(sentences)
		tagged_sent = self.pos_tag_text(tokenized_sents)
		chunks = self.context_chunk_text(tagged_sent)
		self.named_entity_recognition_classification(tagged_sent)
		return 0
		#[print("\nNamed Entity: ", i, " Type: ", named_entities[i]) for i in named_entities if True]

		'''
		# Relation Dict
		relation_dict = find_min_substring(tagged_sents, list(set(named_entities)))

		print("\nRelational Dict")
		[print("\n", ne, sent) for (ne,sent) in relation_dict if True]
		
		# Relation Extraction
		print("\nExtracting Named Entity Relations...")
		'''


	def find_min_substring(strings, words):
		if type(strings) != list:
			return("Invalid type strings. String must be list.")
		elif type(words) != list:
			return("Invalid type words. Word must be list.")

		relation_dict = []
		for sent in strings:
			if sent == []:
				continue
			sent = [(w.lower(),t) for (w,t) in sent]
			ne_relation_overlap = list(set(sent) & set(words))
			start = 0
			end = len(sent) - 1
			if len(ne_relation_overlap) > 1:
				min_list = []
				max_list = []
				ne_occurence = []
				for (ne,tag) in ne_relation_overlap:
					indices = [i for i,val in enumerate(sent) if val==(ne,tag)]
					if indices != []:
						min_list.append(min(indices))
						max_list.append(max(indices))
						ne_occurence.append(ne)
				start = min(min_list)
				end = max(max_list)
			#elif len(ne_relation_overlap) == 1:
			#	pass
			else:
				continue
			if sent[start:end] != []:
				try:
					relation_dict.append((ne_relation_overlap, sent[start:end]))
				except (TypeError) as e:
					print("Error: ", e, " ne_relation_overlap: ", ne_relation_overlap, " sent: ", sent[start:end])
		return relation_dict

#agent = Language_Processing_Agent(sys.argv[1])