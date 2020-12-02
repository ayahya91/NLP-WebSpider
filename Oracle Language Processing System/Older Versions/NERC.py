'''
	Oracle Named Entity Classifier v1
	Status: Funtional, Development
	Written By Ahmed Yahya

	Named Entity Classifier:
		Regex Classifier is way better than Baseline

	Improvements:
		Add to baseline chunker:
			ne = re.match(r'\([A-Z].*\\*\)',str(token))
			if ne != None:
				ne_string = str(token[1:-1])
				ne_components = ne_string.split(" ")
				ne_type = ne_components[0]
				ne = ' '.join(ne_components[1:])
				if ne in self.named_entities:
					if self.named_entities[ne] != ne_type:
						self.named_entities[ne].append(ne_type)
					else:
						continue
				else:
					self.named_entities[ne] = [ne_type]

		Add to regex_chunker:											
			INEFFECTIVE:			DT_JJ_NN:	{<DT|JJ|NN.*>+}		chunk determiner/possessive adjective and nouns
			INEFFECTIVE:			D_P_JJ_NN:	{<DT|PP\$>?<JJ.*>*<NN.*>+}		# chunk determiner/possessive adjective and nouns | Not Good
			INEFFECTIVE:			DT_JJ_NP:	{<DT|JJ|NP.*>+}					# chunk determiner/possessive adjective and nouns
			SEMI-EFFECTIVE:			N-TL: 		{<N.*-TL>+}		
		
'''
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!! INCORPORATE META DATA!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


import nltk, re, itertools, time
from dateutil.parser import parse

class Named_Entity_Classifier:					# Extract Named Entities
	temporal_strings = ["today", "tomorrow", "yesterday", "now", "week", "month", "year", "decade", "century"]
	# Add Libraries Here
	def __init__(self, tagged_sents):
		start = time.time()
		self.regex_ne_chunker(tagged_sents)
		self.baseline_ne_chunker(tagged_sents)
		exec_time = time.time() - start
		print("\nNERC Execution Time: " + str(exec_time) + " seconds.")
		#self.extract_all_nouns(tagged_sents)					# 	self.all_nouns
		#self.extract_temporal_tokens(tagged_sents)				#   self.temporal_tokens

	def extract_all_nouns(self, tagged_sents):
		self.all_nouns = []
		for sent in tagged_sents:
			self.all_nouns.extend([(word, tag) for (word, tag) in sent if tag[0] == 'N'])

	def extract_temporal_tokens(self, tagged_sents):			# Not Good
		self.temporal_tokens = []
		for sent in tagged_sents:
			for (word,tag) in sent:
				try:
					parse(word)
					self.temporal_tokens.append((word, tag))
				except:
					if word in Named_Entity_Classifier.temporal_strings:
						self.temporal_tokens.append((word, tag))
					else:
						continue

	def baseline_ne_chunker(self, tagged_sents):
		self.baseline_chunk_sents = nltk.chunk.ne_chunk_sents(tagged_sents, binary=True)
		self.named_entities = []
		for gen in self.baseline_chunk_sents:
			for token in gen:
				if hasattr(token,'label') and token.label() == 'NE':
					if token not in self.named_entities:
						self.named_entities.append(token)

	def regex_ne_chunker(self, tagged_sents):
		chunk_grammar = r"""
				D_P_JJ_NP: 	{<DT|PP\$>?<JJ.*>*<NP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
						 	{<DT|PP\$>?<JJ.*>*<NNP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
				NN_NP:		{<NN.*>+<NNP>+}					# Might remove this one
				NP_JJ_NP:	{<NNP.*>+<JJ.*>?<NP.*>+}		# Might remove this one
				NP: 		{<NP>+}							# chunk prepositions followed by NP
							{<NNP>+}
			"""	
		self.regex_parser = nltk.RegexpParser(chunk_grammar)
		self.regex_chunks = []
		for sent in tagged_sents:
			tree = self.regex_parser.parse(sent)
			for subtree in tree.subtrees():
				if subtree.label() == 'NP' or subtree.label() == 'D_P_JJ_NP' or subtree.label() == 'NP_JJ_NN' or subtree.label() == 'NN_NP': 
					#NE = str(subtree)			#.replace(subtree.label(), 'NE')
					if subtree not in self.regex_chunks:
						self.regex_chunks.append(subtree)										

	#def merge_regex_ne_chunks(self):
