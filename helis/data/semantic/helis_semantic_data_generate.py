# %%
import itertools
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import owlready2
from owlready2 import *

# [IMPORTANCE] Add the java path to the owlready2 library
owlready2.JAVA_EXE = r"C:\Users\Toon\AppData\Local\Programs\Eclipse Adoptium\jdk-17.0.9.9-hotspot\bin\java.exe"
ONTOLOGY_PATH = "helis_v1.00.train.owl"
CLASS_FILE = Path.cwd().parent / "owl2vec" / "classes.txt"
OUTPUT_PATH = "helis_filtered_subsumption_dataset.pkl"
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

filtered_dataset = list(filter(lambda x: 15 >= len(x) >= 5, dataset))
print(f"{len(filtered_dataset) = }")


# %%

classes = [line.strip() for line in open(CLASS_FILE).readlines()]
classes_dict = {cls: i for i, cls in enumerate(classes)}
class_list = set(classes_dict.keys())

flatten_dataset = set(itertools.chain.from_iterable(filtered_dataset))
print(f"{len(flatten_dataset & class_list)=}")


# %%

testable_class = flatten_dataset & class_list
testable_dataset = []

for data in filtered_dataset:
    for class_i in data:
        if class_i not in testable_class:
            break
    else:
        testable_dataset.append(data)
print(f"{len(testable_dataset)=}")


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
