'''
	Oracle Relationship Extractor v1
	Status: Funtional, Development
	Written By Ahmed Yahya
'''

import nltk, time

class RelExtractor:
	def __init__(self, tagged_sents):
		start = time.time()
		self.rel_extract_baseline_ne(tagged_sents)
		self.rel_extract_regex_ne(tagged_sents)
		exec_time = time.time() - start
		print("\nRelational Extractor Execution Time: " + str(exec_time) + " seconds.")

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

	def rel_extract_regex_ne(self, tagged_sents):
		chunk_grammar = r"""
				D_P_JJ_NP: 	{<DT|PP\$>?<JJ.*>*<NP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
							{<DT|PP\$>?<JJ.*>*<NNP.*>+}		# chunk determiner/possessive adjective and nouns | Very Good
				NN_NP:		{<NN.*>+<NNP>+}					# Might remove this one
				NP_JJ_NN:	{<NNP.*>+<JJ.*>?<NP.*>+}		# Might remove this one
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
			'''
				elif subtree.label() == 'NP' or subtree.label() == 'D_P_JJ_NP': 
					if last_ne is not None:	
						relation += [subtree.leaves()]
						self.extracted_rel_regex += [relation]
						print("Relation")
						print(relation)
						relation = [subtree.leaves()]
						last_ne = subtree.leaves()
					else:
						last_ne = subtree.leaves()
						relation += [subtree.leaves()]
				'''