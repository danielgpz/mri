from model.vectorial import VectorialModel
from indexer.indexer import get_vector
from indexer.aho_corasick import aho_corasick
import sys, json

# python3 main.py ./docs/CISI.vectors.json ./docs/CISI.keywords.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    with open(keywords_path, 'r') as kp:
        keywords = json.load(kp)
        ac = aho_corasick(keywords)

    with open(vectors_path, 'r') as vp:
        vectors_dict = json.load(vp)
        N = len(vectors_dict)
        vectors = []
        id_titles = []

        for idx, dic in vectors_dict.items():
            vectors.append(dic["vector"])
            id_titles.append((idx, dic["title"]))

        vm = VectorialModel(len(keywords), vectors)
        del vectors_dict


    while True:
        query = input('\nQuery: ')
        qvector = get_vector(query, ac)
        results = vm.query(qvector)
        print('Results:')
        print('\n'.join(f'{j + 1}: \"{id_titles[result[1]][1]}\" (ID: {id_titles[result[1]][0]} - Rel: {result[0]})' for j, result in enumerate(results[:10])))