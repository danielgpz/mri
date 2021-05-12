#!/usr/bin/env python3

import yake
from pathlib import Path
import os
import json
import nltk
import math

def get_vectors(path: str, ext: str):
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
			# print(content)
			kw_extractor = yake.KeywordExtractor(top=max(1, math.ceil(math.log2(len(content)))), n=1)
			keywords = kw_extractor.extract_keywords(content)
			# print(json_obj[i]['title'], keywords)
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

	vectors = { 'keywords': [i for i in all] }
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
			# print(content)
			for k in nltk.word_tokenize(content):
				if k.lower() in all:
					vector[all[k.lower()]] += 1

			vectors[json_obj[i]['title']] = vector

	return vectors

if __name__ == '__main__':
	base_path = "./datasets/"
	ext = "*.ALL.json"

	v = get_vectors(base_path, ext)

	f = open('vectors.json', 'w')
	json.dump(v, f, indent=4, sort_keys=False)
	f.close()
