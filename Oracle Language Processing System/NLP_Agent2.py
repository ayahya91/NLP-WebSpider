'''
	NLP Agent v2  !!!!!!!!!!!!!!Edit this!!!!!!!!!!!!!!!!
	Status: Functional
	Written By Ahmed Mused Yahya

	NLP Agent:
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
'''
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!! INCORPORATE META DATA!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


import nltk, re, itertools, sys, os, datetime, time
from bs4 import BeautifulSoup
from Helper_Lib import *
from NERC2 import *
from ContextChunker import *
from urllib.request import urlopen  
from urllib.parse import urlparse
######################################

class NLP_Agent:
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
	# source_format options are "TEXT", "URL", "TEXT_FILE", "URL_FILE"
	def __init__(self, source, source_format="URL_FILE", options=None):
		self.NLP_log = open(os.getcwd() + "/LPA Logs/NLP_log_" + str(datetime.datetime.today()) + ".txt", "w")
		self.load_tagger_chunker()
		self.url_list = []
		if source_format in ["TEXT", "URL", "TEXT_FILE", "URL_FILE"]:
			start = time.time()
			ret_code = self.main(source, source_format)
			exec_time = time.time() - start
			self.NLP_log.close()
			print("\nExecution Time: " + str(exec_time) + " seconds.")
			print("Good Bye.")
		else:
			print("Invalid source format parameter passed. Options are: \"TEXT\", \"URL\", \"TEXT_FILE\", \"URL_FILE\"")

	def load_tagger_chunker(self):
		self.NLP_log.write("Loading Internal Chunker...\n")
		print("\nLoading Internal Chunker...")
		self.context_chunker = load_serialized_object('context_chunker.pkl', 'chunk')
		## Alternative Chunker
		grammar = r"""
			NP:
				{<.*>+}						# Chunk everything
				}<VBD|IN>+{					# Chink sequences of VBD and IN
			"""
		self.chinker = nltk.RegexpParser(grammar, loop=2)

	def read_source(self, source, source_format="URL_FILE"):															# Read URL's or File Path
		print("\nVisiting: " + source + "\n")
		self.NLP_log.write("\nVisiting: " + source)
		if source_format == "TEXT_FILE":
			try:
				with open(source, 'r') as content_file:
					content = content_file.read()
				raw_text = content
			except:
				return "Invalid source"
		elif source_format == "TEXT":
			raw_text = source
		elif source_format == "URL_FILE":
			try:
				self.url_list = [line.rstrip('\n') for line in open(source)]
				print("\nVisiting: " + self.url_list[0] + "\n")
				response = urlopen(self.url_list[0])
				htmlBytes = response.read()
				htmlString = htmlBytes.decode("utf-8")
				parsed_html = BeautifulSoup(htmlString, 'html.parser')
				for script in parsed_html(["script", "style"]):
					script.extract()
				raw_text = str(parsed_html.get_text())
				self.url_list = self.url_list[1:]
			except:
				return "Invalid source"
		elif source_format == "URL":
			try:
				response = urlopen(source)
				htmlBytes = response.read()
				htmlString = htmlBytes.decode("utf-8")
				parsed_html = BeautifulSoup(htmlString, 'html.parser')
				for script in parsed_html(["script", "style"]):
					script.extract()
				raw_text = str(parsed_html.get_text())
			except:
				return "Invalid source"
		return raw_text

	def normalize_text(self, raw_text):												# Resolve Word Contractions, normalize
		print("\nNormalizing Text...")
		lines = (line.strip() for line in raw_text.splitlines())							# break into lines and remove leading and trailing space on each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))			# break multi-headlines into a line each
		raw_text = '\n'.join(chunk for chunk in chunks if chunk)							# drop blank lines

		print("\nResolving Word Contractions...")
		for i in list(NLP_Agent.word_contractions):
			current_word_contraction = re.compile(re.escape(i), re.IGNORECASE)
			if type(NLP_Agent.word_contractions[i]) is list:
				# Do Something Here !!!!!!!!!!! 
				normalized_text = current_word_contraction.sub(NLP_Agent.word_contractions[i][0], raw_text)
			else:
				normalized_text = current_word_contraction.sub(NLP_Agent.word_contractions[i], raw_text)
		self.NLP_log.write("\n\nNormalized Text:\n\n" + normalized_text)
		return normalized_text

	def sentence_segmenter(self, string):													# Sentence Segmenter
		print("\nSegmenting Sentences...")
		sentences = nltk.sent_tokenize(string)
		sentences = [sent for sent in sentences if len(sent) > 1]
		self.NLP_log.write("\n\nSentences:\n\n")
		for sent in sentences:
			self.NLP_log.write("\n" + sent + "\n")
		return sentences

	def tokenizer(self, string):															# Tokenization
		print("\nTokenizing Sentences...")
		tokenized_sents = [nltk.word_tokenize(sent) for sent in string]					#tokenized_text = nltk.Text(tokens)		# This line is not necessary
		self.NLP_log.write("\n\nTokenized Sentences:\n\n")
		for sent in tokenized_sents:
			self.NLP_log.write("\n" + str(sent) + "\n")
		return tokenized_sents

	def pos_tag_text(self, tokenized_text):														# Tagging
		print("\nTagging Sentences...")
		tagged_sents = [nltk.pos_tag(tokens) for tokens in tokenized_text]
		self.NLP_log.write("\n\nTagged Sentences:\n\n")
		for sent in tagged_sents:
			self.NLP_log.write("\n" + str(sent) + "\n")
		return tagged_sents

	def context_chunk_text(self, tagged_sents):													# Chunking
		print("\nChunking Text...")
		context_chunker_result = [self.context_chunker.parse(tagged_sent) for tagged_sent in tagged_sents]
		context_chunker_result = [chunk for chunk in context_chunker_result if chunk is not None]
		self.NLP_log.write("\n\nContext Chunker Results:\n\n")
		for chunks in context_chunker_result:
			self.NLP_log.write(str(chunks))
			self.NLP_log.write("\n")
		return context_chunker_result

	def chink_text(self, tagged_sents):
		print("\nChinking Text...")
		chinker_results = [self.chinker.parse(tagged_sent) for tagged_sent in tagged_sents]
		chinker_results = [chink for chink in chinker_results if chink is not None]
		self.NLP_log.write("\n\nChinker Results:\n\n")
		for chunks in chinker_results:
			self.NLP_log.write(str(chunks))
			self.NLP_log.write("\n")
		return chinker_results

	def nltk_chunker_text(self, tagged_sents):
		print("\nNLTK Chunking Text...")
		nltk_chunker_result = [nltk.chunk.ne_chunk(tagged_sent) for tagged_sent in tagged_sents]
		ntlk_chunker_result = [chunk for chunk in nltk_chunker_result if chunk is not None]
		self.NLP_log.write("\n\nNLTK Chunker Results:\n\n" + str(ntlk_chunker_result) + "\n\n")
		for chunks in ntlk_chunker_result:
			self.NLP_log.write("Tree('S',\n" + self.stringify_tree(str(chunks)) + '\n')
		return nltk_chunker_result

	def named_entity_recognition_classification(self, tagged_sents):					# Extract Named Entities
		print("\nRecognizing Named Entities...")
		nerc = Named_Entity_Recognition_Classifier(tagged_sents)
		self.NLP_log.write('*'*60 + '\n')
		self.NLP_log.write('*'*60 + '\n')
		self.NLP_log.write("Named Entity Classifier Results \n")
		self.NLP_log.write('*'*60 + '\n')
		count = 1
		self.NLP_log.write("\nBaseline NE:\n")
		for i in nerc.named_entities:
			self.NLP_log.write(str(count) + ".\t" + str(i) + "\n")
			count += 1
		self.NLP_log.write('\n' + '-'*60 + '\n')
		count = 1
		self.NLP_log.write("\nRegex NE:\n")
		for i in nerc.regex_chunks:
			self.NLP_log.write(str(count) + ".\t" + str(i) + "\n")
			count += 1
		self.NLP_log.write('*'*60 + '\n')
		return nerc.named_entities, nerc.regex_chunks

	def relation_extractor(self,tagged_sents):
		print("\nExtracting Named Entity Relations")
		rel_ext =  Named_Entity_Recognition_Classifier(tagged_sents, options="REL")
		self.NLP_log.write('*'*60 + '\n')
		self.NLP_log.write("Relation Extractor Results \n")
		self.NLP_log.write('*'*60 + '\n')
		self.NLP_log.write("\nBaseline Relation Extractor:\n")
		for i in rel_ext.extracted_rel_baseline:
			self.NLP_log.write("Named Entities: \n" + str(i[0]) + " ---> " + str(i[-1]) + "\n")
			self.NLP_log.write("Relation: \n" + str(i[1:-1]) + "\n\n")
		self.NLP_log.write('-'*60 + '\n')
		self.NLP_log.write("\nRegex Relation Extractor:\n")
		for i in rel_ext.extracted_rel_regex:
			self.NLP_log.write("Named Entities: \n" + str(i[0]) + " ---> " + str(i[-1]) + "\n")
			self.NLP_log.write("Relation: \n" + str(i[1:-1]) + "\n\n")
			#print("Named Entities: " + str(i[0]) + " ---> " + str(i[-1]) + "\n")
			#print("Relation: " + str(i[1:-1]) + "\n\n")
		self.NLP_log.write('*'*60 + '\n')
		return rel_ext.extracted_rel_baseline, rel_ext.extracted_rel_regex

	def main(self, source, source_format="URL_FILE"):
		while True:
			self.raw_text = self.read_source(source, source_format)
			if self.raw_text == "Invalid source":
				return 1
			self.NLP_log.write('-'*70 + "\n")
			self.normalized_text = self.normalize_text(self.raw_text)
			self.sentences = self.sentence_segmenter(self.normalized_text)
			self.tokenized_sents = self.tokenizer(self.sentences)
			self.tagged_sent = self.pos_tag_text(self.tokenized_sents)
			self.chunks = self.context_chunk_text(self.tagged_sent)
			self.chinks = self.chink_text(self.tagged_sent)
			#self.nltk_chunks = self.nltk_chunker_text(self.tagged_sent)
			self.ne = self.named_entity_recognition_classification(self.tagged_sent)
			self.rel_extractor = self.relation_extractor(self.tagged_sent)
			self.NLP_log.write('-'*70 + "\n")
			if self.url_list == []:
				break
			else:
				source = self.url_list[0]
				source_format = "URL"
				self.url_list = self.url_list[1:]
		return 0

	def stringify_tree(self, stringified_tree):
		# Parse tree into string
		return str(stringified_tree.split("Tree('S',"))

	def token_validator(self, chunk):
		if type(chunk) == list:
			chunk = [tup for tup in chunk if tup[0].isalpha()]
			return chunk
		elif type(chunk) == tuple:
			return chunk[0].isalpha()
		else:
			print("Not a Tuple: ", chunk)
			return True


agent = NLP_Agent(sys.argv[1], source_format=sys.argv[2])
'''
print("Chunker Results: \n")
for chunk in agent.chunks:
	#if agent.stringify_tree(chunk) is not None:
	print(chunk)

print("\nChinker Results: \n")
for chunk in agent.chinks:
	#if agent.stringify_tree(chunk) is not None:
	print(chunk)

print("\nNLTK Chunker Results: \n")
for chunk in agent.nltk_chunks:
	print("Tree('S',\n" + agent.stringify_tree(str(chunk)) + '\n\n')
'''