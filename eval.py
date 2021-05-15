from main import SearchEngine
import sys, json

def medida_f(P, R, B):
    return (1 + B * B) * P * R / (B * B * P + R)

# python3 eval.py ./docs/CISI.vectors.json ./docs/CISI.keywords.json ./datasets/CISI.QRY.json ./datasets/CISI.REL.json
if __name__ == "__main__":
    vectors_path = sys.argv[1]
    keywords_path = sys.argv[2]

    se = SearchEngine(vectors_path, keywords_path)

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
            ans = se.query(text)[:top]

            rr = sum(1 for doc in ans if doc in expecteds) # recuperados relevantes
            R_precision = rr/len(ans)
            presiciones.append(R_precision)
            print(f'{top}-Precision: {R_precision}')
            
            R_recobrado = rr/len(expecteds)
            recobrados.append(R_recobrado)
            print(f'{top}-Recobrado: {R_recobrado}')
            
            if rr > 0:
                R_medidaf = medida_f(R_precision, R_recobrado, beta)
                print(f'{top}-Medida F (Beta= {beta}): {R_medidaf}')
                
                R_medidaf1 = medida_f(R_precision, R_recobrado, 1)
                print(f'{top}-Medida F1: {R_medidaf1}')
            else:
                print('No se recupero ningun documento relevante!!!')
                print('  - Recuperados: ' + ', '.join(ans))
                print('  - Esperados: ' + ', '.join(doc for doc in expecteds))
                fallos += 1
            
            fallout = (len(ans) - rr)/(se.vm.N - len(expecteds))
            print(f'{top}-Fallout: {fallout}')
        else:
            print('Id de consula no encontrado en el archivo de relevancias >:(')

    print(f'\nResultados finales:')
    print(f'Total de consultas: {len(presiciones)}')
    print(f'Precision media: {round(sum(presiciones)/len(presiciones), 3)}')
    print(f'Recobrado medio: {round(sum(recobrados)/len(recobrados), 3)}')
    print(f'Fallos: {fallos}/{len(presiciones)} ({round(100 * fallos / len(presiciones), 3)}%)')

    