from model.vectorial import VectorialModel
from indexer.indexer import get_vector
from indexer.aho_corasick import aho_corasick
import sys, json

class SearchEngine:
    def __init__(self, vectors_path: str, keywords_path: str):
        with open(keywords_path, 'r') as kp:
            keywords = json.load(kp)
            self.ac = aho_corasick(keywords)

        with open(vectors_path, 'r') as vp:
            vectors_dict = json.load(vp)
            self.name = vectors_dict['name']
            vectors_dict.pop("name")
        
        self.vectors = []
        self.id_titles = []
        self.idxs = {}

        for idx, dic in vectors_dict.items():
            self.idxs[idx] = len(self.vectors)
            self.vectors.append(dic["vector"])
            self.id_titles.append((idx, dic["title"]))

        self.vm = VectorialModel(len(keywords), self.vectors)
        del vectors_dict
    
    def query(self, text: str):
        qvector = get_vector(text, self.ac)
        results = self.vm.query(qvector)
        return [self.id_titles[result[1]][0] for j, result in enumerate(results[:100])]

    def feedback(self, relevant_ids: list, irrelevant_ids: list):
        results = self.vm.feedback(relevant_ids, irrelevant_ids)
        return [self.id_titles[result[1]][0] for j, result in enumerate(results[:100])]
    

# python3 main.py ./docs/CISI.vectors.json ./docs/CISI.keywords.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    se = SearchEngine(vectors_path, keywords_path)

    while True:
        query = input('\nQuery: ')
        qvector = get_vector(query, se.ac)
        results = se.vm.query(qvector)
        print('Results:')
        print('\n'.join(f'{j + 1}: \"{se.id_titles[result[1]][1]}\" (ID: {se.id_titles[result[1]][0]} - Rel: {result[0]})' for j, result in enumerate(results[:10])))
