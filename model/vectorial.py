from math import log


def rankf(doc: list, qry: list):
    # assert len(doc) == len(qry), 'Deben tener el mismo tamanho'
    return sum(wj * wq for wj, wq in zip(doc, qry))/(sum(wj * wj for wj in doc)*sum(wq * wq for wq in qry))**.5

class VectorialModel:
    def __init__(self, n: int, freq_vectors: list, rank_function=rankf):
        self.rank_function = rank_function
        self.N, self.n = len(freq_vectors), n
        
        idf = [log(self.N/sum(v[i] > 0 for v in freq_vectors)) for i in range(n)]
        mfq = [max(v) for v in freq_vectors]

        self.vectors = [[idf[i] * v[i] / mfq[j] for i in range(n)] for j, v in enumerate(freq_vectors)]
        self.idf = idf

    def query(self, freq_query: list, alpha=0.4):
        # assert len(freq_query) == n, f'El vector de la query debe ser de tamanho {self.n}'
        mfq = max(freq_query)
        if mfq == 0: return []
        qvector = [self.idf[i] * (alpha + (1 - alpha) * freq_query[i] / mfq) for i in range(self.n)]
        ranks = ((self.rank_function(vector, qvector), j) for j, vector in enumerate(self.vectors))
        return sorted(ranks, reverse=True)

if __name__ == "__main__":
    docs = [
        "lion lion lion",
        "lion lion lion fox",
        "lion fox dog",
        "lion lion lion fox fox fox",
        "dog"
    ]
    terms = ["lion", "fox", "dog"]

    docss = [doc.split() for doc in docs]

    freq_vecs = [[doc.count(term) for term in terms] for doc in docss]
    print(terms, freq_vecs, sep='\n')

    mri = VectorialModel(len(terms), freq_vecs)
    print(mri.idf, mri.vectors, sep='\n')

    query = "blue dog".split()
    freq_query = [query.count(term) for term in terms]

    print(mri.query(freq_query))

