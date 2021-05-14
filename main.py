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
            vectors_dict.pop('name')
            N = len(vectors_dict)
            vectors = [[]] * N
            self.titles = [""] * N

            for idx, dic in vectors_dict.items():
                i = int(idx) - 1
                vectors[i] = dic["vector"]
                self.titles[i] = dic["title"]

            self.vm = VectorialModel(len(keywords), vectors)
            del vectors_dict
    
    def query(self, text: str):
        qvector = get_vector(text, self.ac)
        results = self.vm.query(qvector)
        return [result[1] + 1 for j, result in results]

# python3 main.py ./datasets/CISI.vectors.json ./datasets/CISI.keywords.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    se = SearchEngine(vectors_path, keywords_path)

    while True:
        query = input('\nQuery: ')
        qvector = get_vector(query, se.ac)
        results = se.vm.query(qvector)
        print('Results:')
        print('\n'.join(f'{j + 1}: \"{se.titles[result[1]]}\" (ID: {result[1] + 1} - Rel: {result[0]})' for j, result in enumerate(results[:10])))