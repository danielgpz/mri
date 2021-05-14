build_CRAN:
	python3 load_vectors.py ./datasets/ CRAN.ALL.json CRAN

build_CISI:
	python3 load_vectors.py ./datasets/ CISI.ALL.json CISI

serve_CRAN:
	python3 server.py localhost 8080 "./docs/CRAN.vectors.json" "./docs/CRAN.keywords.json"

serve_CISI:
	python3 server.py localhost 8080 "./docs/CISI.vectors.json" "./docs/CISI.keywords.json"

test_CRAN:
	python3 eval.py ./docs/CARN.vectors.json ./docs/CRAN.keywords.json ./datasets/CRAN.QRY.json ./datasets/CRAN.REL.json

test_CISI:
	python3 eval.py ./docs/CISI.vectors.json ./docs/CISI.keywords.json ./datasets/CISI.QRY.json ./datasets/CISI.REL.json