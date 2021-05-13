from model.vectorial import VectorialModel
from indexer.indexer import get_vector
import sys, json

# python main.py ./datasets/CISI.vectors.json ./datasets/CISI.keywords.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    with open(keywords_path, 'r') as kp:
        keywords = json.load(kp)

    with open(vectors_path, 'r') as vp:
        vectors_dict = json.load(vp)
        N = len(vectors_dict)
        vectors = [[]] * N
        titles = [""] * N

        for idx, dic in vectors_dict.items():
            i = int(idx) - 1
            vectors[i] = dic["vector"]
            titles[i] = dic["title"]

        vm = VectorialModel(len(keywords), vectors)
        del vectors_dict


    while True:
        query = input('\nQuery: ')
        qvector = get_vector(query, keywords)
        results = vm.query(qvector)
        print('Results:')
        print('\n'.join(f'{j + 1}: \"{titles[result[1]]}\" (ID: {result[1] + 1} - Rel: {result[0]})' for j, result in enumerate(results[:10])))


