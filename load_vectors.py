from indexer.indexer import Indexer
import sys

# python load_vectors.py ./datasets/ CISI.ALL.json CISI
if __name__ == '__main__':
    base_path = sys.argv[1]
    ext = sys.argv[2]
    name = sys.argv[3]
    idx = Indexer(base_path, ext, name)
    print(idx.vectorsPath)
    print(idx.keywordsPath)