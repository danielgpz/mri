# MRI using Vectorial Model.
Final proyect of SI subject. Model and build an MRI.

## Dependencies  
- `pip install yake`  
- `pip install nltk`
```
$ python
$ import nltk  
$ nltk.download('punkt')  
```

## How to use:
- To create the necesary information to use de each example dataset:
    
    ```
    make build_CRAN
    make build_CISI
    ```

- To run a server in localhost using each dataset:
    
    ```
    make serve_CRAN
    make serve_CISI
    ```

- To run the console app version using each dataset:
    
    ```
    make console_CRAN
    make console_CISI
    ```

- To obtain evaluation metrics for each dataset:
    
    ```
    make test_CRAN
    make test_CISI
    ```

