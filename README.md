# ontology-embedding-evaluation-set-perspectives-1

## setup
using Python 3.8.18 
```bash 
%pip install -r <path\to\requirements.txt>
```
## Features

| From                | Evaluation Metric                                |
| ------------------- | ------------------------------------------------ |
| concept2vec         | The Coherence Score                              |
|                     | Categorization metric                            |
|                     | Class-Entity visualization via t-SNE             |
| OWL2VEC             | Euclidean distance for positve and negative pair |
|                     | MRR/Hits@1/Hits@5/Hits@10                        |
| ontology-evaluation | SemMR and SemMMR                                 |

## Models

- OWL2VEC* from [KRR-Oxford/OWL2Vec-Star: Embedding OWL ontologies (github.com)](https://github.com/KRR-Oxford/OWL2Vec-Star/tree/master)
- Model from [pykeen/pykeen: 🤖 A Python library for learning and evaluating knowledge graph embeddings (github.com)](https://github.com/pykeen/pykeen)
## Dataset
- FoodOn \*except Categorization metric and The Coherence Score
- Helis
- OHD \*only evaluate using pykeen

## Files structure
- **foodon-helis**
	- **data:** for generate and save dataset
	- **workspace:** for train pykeen and owl2vec-evaluate
- **ohd**
	- **data:** for generate and save dataset
	- **workspace:** for train pykeen-evaluate

## Citations
- **Lamy JB**. [Owlready: Ontology-oriented programming in Python with automatic classification and high level constructs for biomedical ontologies.](http://www.lesfleursdunormal.fr/_downloads/article_owlready_aim_2017.pdf) **Artificial Intelligence In Medicine 2017**;80:11-28