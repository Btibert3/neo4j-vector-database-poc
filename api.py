from fastapi import FastAPI
from pydantic import BaseModel
import spacy 
from py2neo import Graph 

nlp = spacy.load("en_core_web_md")
graph = Graph("bolt://neo4j:7687", auth=('neo4j', 'neo'))

class Command(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def home():
    return {'hello':'world'}

@app.post("/model")
def reco(command: Command):
    doc = nlp(command.text)
    vec = doc.vector.tolist()
    cypher = f"""
    WITH {vec} as vector
    MATCH (i:Intent)<--(c:Command)-[:HAS_VECTOR]->(e:Embedding)
    WITH vector, c, i, gds.similarity.cosine(vector, e.vector) as sim
    where sim > 0
    RETURN c.text, i.intent, sim
    ORDER BY sim desc
    LIMIT 5
    """
    results = graph.run(cypher).to_data_frame()

    return results.to_dict(orient='records')