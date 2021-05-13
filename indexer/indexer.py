#!/usr/bin/env python3

import yake
from pathlib import Path
import os
import json
import nltk
import math
import sys
from indexer.aho_corasick import aho_corasick

'''
	self.name: given name to the collection of documents
	self.keywords: extracted keywords
	self.keywordsPath: path to json containing self.keywords
	self.vectorsPath: path to json containing generated vectors for all documents
'''
class Indexer:
	'''
		path: path of all documents that must be indexed
		ext: regular expression to filter which documents must be indexed
		name: given name to this collection
	'''
	def __init__(self, path: str, ext: str, name: str):
		self.name = name
		all = {}

		for file in list(Path(path).rglob(ext)):		
			f = open(file, 'r')
			json_obj = json.load(f)
			f.close()

			for i in json_obj:
				content = ''
				for j in json_obj[i]:
					if j != 'id' and j != 'keywords':
						content += json_obj[i][j] + '\n'

				content = ' '.join(nltk.word_tokenize(content))
				kw_extractor = yake.KeywordExtractor(top=max(1, math.ceil(math.log2(len(content)))), n=1)
				keywords = kw_extractor.extract_keywords(content)
				json_obj[i]['keywords'] = keywords
				for k in keywords:
					all[k[0].lower()] = 0

			f = open(file, 'w')
			json.dump(json_obj, f, indent=4, sort_keys=False)
			f.close()

		idx = 0
		for i in all:
			all[i] = idx
			idx += 1

		vectors = {}
		ac = aho_corasick(all)
		for file in list(Path(path).rglob(ext)):
			f = open(file, 'r')
			json_obj = json.load(f)
			f.close()

			for i in json_obj:
				vector = [0] * idx
				content = ''
				for j in json_obj[i]:
					if j != 'id' and j != 'keywords':
						content += json_obj[i][j] + '\n'

				vector = ac.match(content.lower())
				vectors[json_obj[i]['id']] = {}
				vectors[json_obj[i]['id']]['title'] = json_obj[i]['title']
				vectors[json_obj[i]['id']]['vector'] = vector

		self.keywords = all
		self.keywordsPath = os.path.join(os.getcwd(), 'datasets', self.name + '.keywords.json')
		f = open(self.keywordsPath, 'w')
		json.dump(all, f, indent=4, sort_keys=False)
		f.close()

		self.vectorsPath = os.path.join(os.getcwd(), 'datasets', self.name + '.vectors.json')
		f = open(self.vectorsPath, 'w')
		json.dump(vectors, f, indent=4, sort_keys=False)
		f.close()

		for i in json_obj:
			id = json_obj[i]['id']
			f = open(os.path.join(os.getcwd(), 'docs', id + '.json'), 'w')
			json.dump(json_obj[i], f, indent=4, sort_keys=False)
			f.close()

		cnt = [0] * idx
		for key in vectors:
			for i in range(idx):
				cnt[i] += vectors[key]['vector'][i]
		
		for i in range(idx):
			if not cnt[i]:
				for key in all:
					if all[key] == i:
						raise Exception(f'keyword ({all[key]}) {key} has frequency 0 in all vectors')
						# print(f'keyword ({all[key]}) {key} has frequency 0 in all vectors')

'''
	return frequency vector of all words in `text`
'''
def get_vector(text: str, keywords: dict):
	ac = aho_corasick(keywords)
	return ac.match(text.lower())

# python3 indexer.py ./datasets/ CISI.ALL.json CISI
if __name__ == '__main__':
	base_path = sys.argv[1]
	ext = sys.argv[2]
	name = sys.argv[3]
	Indexer(base_path, ext, name)
