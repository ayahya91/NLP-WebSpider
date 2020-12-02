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

class Named_Entity_Recognition_Classifier:					# Extract Named Entities
	temporal_strings = ["today", "tomorrow", "yesterday", "now", "week", "month", "year", "decade", "century"]
	# Add Libraries Here
	def __init__(self, tagged_sents, options="NERC"):
		if options == "NERC":
			start = time.time()
			self.regex_ne_chunker(tagged_sents)
			self.baseline_ne_chunker(tagged_sents)
			exec_time = time.time() - start
			print("\nNERC Execution Time: " + str(exec_time) + " seconds.")
		elif options == "REL":
			start = time.time()
			self.rel_extract_baseline_ne(tagged_sents)
			self.rel_extract_regex_ne(tagged_sents)
			exec_time = time.time() - start
			print("\nRelational Extractor Execution Time: " + str(exec_time) + " seconds.")
		else:
			print("INVALID OPTION.")
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

	def rm_duplicate(self, subtree, chunks):
		subtree = ['/'.join(i) for i in subtree.leaves() if True]
		index = 0
		for chunk in chunks:
			str_chunk = ['/'.join(i) for i in chunk.leaves() if True]
			if len(set(subtree).intersection(str_chunk)) != 0:
				return False, index
			else:
				index += 1
				continue
		return True, 0		

	''' A LITTLE EXTRA '''
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
				if subtree.label() == 'NP' or subtree.label() == 'NP_JJ_NP' or subtree.label() == 'NN_NP' or subtree.label() == 'D_P_JJ_NP':
					if subtree not in self.regex_chunks:
						self.regex_chunks.append(subtree)		
		'''
					result = self.rm_duplicate(subtree, self.regex_chunks)
					if result[0]:
						self.regex_chunks.append(subtree)
					else:
						if len(self.regex_chunks[result[1]]) >= len(subtree):
							continue
						else:
							 self.regex_chunks[result[1]] = subtree			
		'''		
	############################## RELATION EXTRACTOR #########################################

	def rel_extract_baseline_ne(self, tagged_sents):
		self.baseline_chunk_sents = nltk.chunk.ne_chunk_sents(tagged_sents, binary=True)
		self.extracted_rel_baseline = []
		for gen in self.baseline_chunk_sents:
			last_ne = None
			relation = []
			for token in gen:
				if hasattr(token,'label') and token.label() == 'NE':
					if last_ne is not None:
						relation.append(token)
						self.extracted_rel_baseline.append(relation)
						relation = [token]
						last_ne = token
					else:
						last_ne = token
						relation.append(token)
				elif last_ne is not None:
					relation.append(token)
				else:
					continue

	''' A LITTLE EXTRA '''
	def rel_extract_regex_ne(self, tagged_sents):
		chunk_grammar = r"""
				D_P_JJ_NP: 	{<DT|PP\$>?<JJ.*>*<NP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
						 	{<DT|PP\$>?<JJ.*>*<NNP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
				NN_NP:		{<NN.*>+<NNP>+}					# Might remove this one
				NP_JJ_NP:	{<NNP.*>+<JJ.*>?<NP.*>+}		# Might remove this one
				NP: 		{<NP>+}							# chunk prepositions followed by NP
							{<NNP>+}
			"""	
		self.regex_parser = nltk.RegexpParser(chunk_grammar, loop=2)
		self.extracted_rel_regex = []
		for sent in tagged_sents:
			tree = self.regex_parser.parse(sent)
			last_ne = None
			relation = []
			for subtree in tree: 
				if subtree in tree.subtrees():
					if last_ne is not None:	
						relation += [subtree]
						self.extracted_rel_regex += [relation]
						relation = [subtree]
						last_ne = subtree
					else:
						last_ne = subtree
						relation += [subtree]
				else:
					if last_ne is not None:
						relation += [subtree]
					else:
						continue
