# %%
import rdflib as rdf
from rdflib import Graph
import pandas as pd
from pathlib import Path

# %%
PATH = Path.cwd().parent / "owl2vec" / "helis_v1.00.train.projection.ttl"
TARGET_PATH = Path.cwd()
# %% [markdown]
# # Parse train dataset

# %%
graph  = Graph()
graph.parse(PATH, format='ttl')

# %%

triples = [triple for triple in graph]
df = pd.DataFrame(triples, columns=['subject', 'predicate', 'object'])


# %%
df = df.applymap(lambda x: x.n3().replace("<", '').replace(">", "") if type(x) == rdf.term.URIRef else x.value)

df.to_csv(TARGET_PATH / "train_dataset.tsv", index=False, header=False)


# %% [markdown]
# ## Col2id file

# %%
def col2id_file(cols, file_name):
    col_index = set(df[cols].values.flatten())
    print(f'cols: {len(col_index)}')
    col2index_df = pd.DataFrame(col_index, columns=['col'])
    col2index_df['index'] = col2index_df.index
    col2index_df.to_csv(TARGET_PATH / file_name, index=False, header=False, sep='\t')
    col_mapping = col2index_df.set_index('col').to_dict()['index']
    return col_mapping

# %%
entity2id = col2id_file(['subject', 'object'], 'entity2id.csv')
relation2id = col2id_file('predicate', 'relation2id.csv')

# %% [markdown]
# ## train2id

# %%
entity_mapping = lambda x: entity2id[x]
relation_mapping = lambda x: relation2id[x]

df_id = df.copy()
df_id.loc[:, 'subject'] = df_id['subject'].map(entity_mapping)
df_id.loc[:, 'predicate'] = df_id['predicate'].map(relation_mapping)
df_id.loc[:, 'object'] = df_id['object'].map(entity_mapping)

# %%
df_id.to_csv(TARGET_PATH / "train2id.csv", index=False, header=False, sep='\t')
# %%
