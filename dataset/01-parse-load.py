"Parse the CLINC150 dataset and load (slowly) into Neo4j running via docker"

import json
import pandas as pd
import spacy 
from spacy import cli
from py2neo import Graph, Node, Relationship

# get the medium for simple vectors as a poc
cli.download("en_core_web_md")
nlp = spacy.load('en_core_web_md')

# read the file
with open("dataset/data_full.json", "r") as f:
    clinc = json.load(f)

df = pd.DataFrame()
for key in clinc.keys():
    tmp = clinc.get(key)
    tmp = pd.DataFrame(tmp, columns=['text', 'intent'])
    tmp['fold'] = key
    df = pd.concat([df, tmp])

docs = list(nlp.pipe(df['text']))
dvs = [d.vector.tolist() for d in docs]
df['vector'] = dvs

graph = Graph("bolt://neo4j:7687", auth=('neo4j', 'neo'))

data = df.to_dict(orient='records')

# not even remotely effecient but straight forward way to retain array
for row in range(len(data)):
    rec = data[row]
    c = Node("Command", text=rec['text'])
    e = Node("Embedding", vector=rec['vector'])
    i = Node("Intent", intent=rec['intent'])
    r1 = Relationship(c, "HAS_INTENT", i)
    r2 = Relationship(c, "HAS_VECTOR", e)
    graph.create(c)
    graph.create(e)
    graph.create(i)
    graph.create(r1)
    graph.create(r2)
    del rec, c, e, i, r1, r2
    if row % 100 == 0:
        print(f"finished row: {row}")

