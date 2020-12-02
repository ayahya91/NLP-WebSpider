
'''
	Oracle Language Processing System Web
	Written By Ahmed Mused Yahya	

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

import nltk, re, itertools, numpy, sys, webspider_v4
from bs4 import BeautifulSoup
from Helper_Lib import *
from generate_context_chunker import *
from urllib.request import urlopen  
from urllib.parse import urlparse
######################################

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
						
def LPS(raw_text_path):
	# Read URL's or File Path
	try:
		response = urlopen(raw_text_path)
		htmlBytes = response.read()
		htmlString = htmlBytes.decode("utf-8")
		parsed_html = BeautifulSoup(htmlString, 'html.parser')
		for script in parsed_html(["script", "style"]):
			script.extract()
		raw_text = str(parsed_html.get_text())

	except ValueError:  # invalid URL
		with open(raw_text_path, 'r') as content_file:
			content = content_file.read()
		raw_text = content

	lines = (line.strip() for line in raw_text.splitlines())							# break into lines and remove leading and trailing space on each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))			# break multi-headlines into a line each
	raw_text = '\n'.join(chunk for chunk in chunks if chunk)							# drop blank lines

	# Resolve Word Contractions 
	print("\nResolving Word Contractions...")
	for i in list(word_contractions):
		current_word_contraction = re.compile(re.escape(i), re.IGNORECASE)
		if type(word_contractions[i]) is list:
			# Do Something Here !!!!!!!!!!! 
			raw_text = current_word_contraction.sub(word_contractions[i][0], raw_text)
		else:
			raw_text = current_word_contraction.sub(word_contractions[i], raw_text)

	# Sentence Segmenter
	print("\nSegmenting Sentences...")
	sentences = nltk.sent_tokenize(raw_text)
	#for sent in sentences:
	#	print(sent)

	# Tokenization
	print("\nTokenizing Sentences...")
	tokenized_sents = [nltk.word_tokenize(sent) for sent in sentences]
	#tokenized_text = nltk.Text(tokens)		# This line is not necessary

	# Load Tagger
	print("\nLoading Internal Tagger...")
	dt = load_serialized_object('default_tagger.pkl', 'tag')
	ut = load_serialized_object('unigram_tagger.pkl', 'tag')
	bt = load_serialized_object('bigram_tagger.pkl', 'tag')
	tt = load_serialized_object('trigram_tagger.pkl', 'tag')
	qt = load_serialized_object('quadrigram_tagger.pkl', 'tag')
	qt2 = load_serialized_object('quintigram_tagger.pkl', 'tag')
	tagger = [qt2, qt, tt, bt, ut, dt]

	# Tagging
	print("\nTagging Sentences...")
	tagged_sents = [tagger[0].tag(tokens) for tokens in tokenized_sents]
	#print("\n First 3 tagged sents: ", tagged_sents[:3])

	# Chunking
	print("\nChunking Text...")
	context_chunker = load_serialized_object('context_chunker.pkl', 'chunk')
	context_chunker_result = [context_chunker.parse(tagged_sent) for tagged_sent in tagged_sents]
	#print("\n First 3 chunked sents: ", context_chunker_result[:3])

	# Extract Named Entities
	print("\nExtracting Named Entities")
	chunk_sents = nltk.chunk.ne_chunk_sents(tagged_sents)	#, binary=True
	named_entities = []
	for gen in chunk_sents:
		for token in gen:			
			ne = re.match(r'\([A-Z].*\\*\)',str(token))
			if ne != None:
				named_entities.append(ne.group())
	print("\nWeeding Out False Positives...")
	start_len = len(named_entities)
	named_entities = [i for i in named_entities if i[i.rfind('/') + 1] == 'N']
	print("False NE's: ", start_len - len(named_entities))
	
	named_entities_dict = dict()
	for i in named_entities:
		ne = str(i[1:-1])
		ne_components = ne.split(" ")
		ne_type = ne_components[0]
		ne = ' '.join(ne_components[1:])
		if ne in named_entities_dict:
			if named_entities_dict[ne] != ne_type:
				named_entities_dict[ne].append(ne_type)
			else:
				continue
		else:
			named_entities_dict[ne] = [ne_type]

	[print("\nNamed Entity: ", i, " Type: ", named_entities_dict[i]) for i in named_entities_dict if True]

	# Relation Dict
	relation_dict = find_min_substring(tagged_sents, list(set(named_entities)))

	print("\nRelational Dict")
	[print("\n", ne, sent) for (ne,sent) in relation_dict if True]
	
	# Relation Extraction
	print("\nExtracting Named Entity Relations...")



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

LPS(sys.argv[1])