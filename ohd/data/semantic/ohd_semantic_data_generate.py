# %%
import itertools
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import owlready2
from owlready2 import *

# [IMPORTANCE] Add the java path to the owlready2 library
owlready2.JAVA_EXE = r"C:\Users\Toon\AppData\Local\Programs\Eclipse Adoptium\jdk-17.0.9.9-hotspot\bin\java.exe"
ONTOLOGY_PATH = "ohd.owl"
OUTPUT_PATH = "ohd_filtered_subsumption_dataset.pkl"
# https://owlready2.readthedocs.io/en/latest/onto.html


# %%
list_map = lambda f, xs: list(map(f, xs))
is_most_specific = lambda x: len(x.descendants(include_self=False)) == 0


def get_ancestors(cls):
    all_ancestors = cls.is_a
    return (
        []
        if len(all_ancestors) == 0
        else [all_ancestors[0]] + get_ancestors(all_ancestors[0])
    )


# %%

onto = get_ontology(ONTOLOGY_PATH).load()
print("warning this will take a long time (30 mins) to run")
sync_reasoner()

# %%
all_classes = list(onto.classes())

dataset = []
for cls in filter(is_most_specific, all_classes):
    dataset.append([cls] + get_ancestors(cls))

# change name to something more descriptive
dataset = list_map(lambda row: list_map(lambda x: x.iri, row), dataset)

# if exclude owl:Thing
dataset = [data[:-1] for data in dataset]

testable_dataset = list(filter(lambda x: 15 >= len(x) >= 5, dataset))
print(f"{len(testable_dataset) = }")


# %%

longest_sequence = max(list_map(len, testable_dataset))
print(f"{longest_sequence = }")

# %%

plt.hist(list_map(len, testable_dataset), bins=20)
plt.show()


# %%

with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(testable_dataset, f)

# %%
