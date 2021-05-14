from model.vectorial import VectorialModel
from indexer.indexer import get_vector
from indexer.aho_corasick import aho_corasick
import sys, json

def medida_f(P, R, B):
    return (1 + B * B) * P * R / (B * B * P + R)

# python3 eval.py ./docs/CISI.vectors.json ./docs/CISI.keywords.json ./datasets/CISI.QRY.json ./datasets/CISI.REL.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    with open(keywords_path, 'r') as kp:
        keywords = json.load(kp)
        ac = aho_corasick(keywords)

    with open(vectors_path, 'r') as vp:
        vectors_dict = json.load(vp)
        N = len(vectors_dict)
        vectors_dict.pop("name")
    
    vectors = []
    id_titles = []

    for idx, dic in vectors_dict.items():
        vectors.append(dic["vector"])
        id_titles.append((idx, dic["title"]))

    vm = VectorialModel(len(keywords), vectors)
    del vectors_dict

    queries_path = sys.argv[3]
    rels_path = sys.argv[4]

    with open(queries_path, 'r') as qp:
        queries = json.load(qp)

    with open(rels_path, 'r') as rp:
        rels = json.load(rp)

    top = int(input('Truncar el top en el indice: '))
    alpha = float(input('Valor alpha de suavizado: '))
    beta = float(input('Valor beta para la medida F: '))
    
    presiciones, recobrados, fallos = [], [], 0
    for id, query in enumerate(queries.values(), start=1):
        # id = int(query['id'])
        text = query['text']
        
        print(f'\n(ID: {id}) Consulta: {text}\nResultados:')
        if str(id) in rels:
            expecteds = rels[str(id)]

            qvector = get_vector(text, ac)
            ans = vm.query(qvector, alpha=alpha)[:top]

            rr = sum(1 for (_, doc) in ans if id_titles[doc][0] in expecteds) # recuperados relevantes
            R_precision = rr/len(ans)
            presiciones.append(R_precision)
            print(f'{top}-Presicion: {R_precision}')
            
            R_recobrado = rr/len(expecteds)
            recobrados.append(R_recobrado)
            print(f'{top}-Recobrado: {R_recobrado}')
            
            if rr > 0:
                R_medidaf = medida_f(R_precision, R_recobrado, beta)
                print(f'{top}-F (Beta= {beta}): {R_medidaf}')
                
                R_medidaf1 = medida_f(R_precision, R_recobrado, 1)
                print(f'{top}-F1: {R_medidaf1}')
            else:
                print('No se recupero ningun documento relevante!!!')
                print('  - Recuperados: ' + ', '.join(id_titles[doc][0] for (_, doc) in ans))
                print('  - Esperados: ' + ', '.join(doc for doc in expecteds))
                fallos += 1
            
            fallout = (len(ans) - rr)/(N - len(expecteds))
            print(f'{top}-Fallout: {fallout}')
        else:
            print('Id de consula no encontrado en el archivo de relevancias >:(')

    print(f'\nResultados finales:')
    print(f'Precision media: {sum(presiciones)/len(presiciones)}')
    print(f'Recobrado medio: {sum(recobrados)/len(recobrados)}')
    print(f'Fallos: {fallos} ({100 * fallos / len(presiciones)}%)')

    