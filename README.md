# Neo4j As a Vector Database

With embeddings at the center of modern machine learning, there is a need to consider how to properly query these vectors in production.  Pinecone and Milvus are two firms that are currently building out vector database solutions, but it occurred to me that Neo4j could be used to solve the same problem.  Neo4j as a vector datbase!

- The property graph supported by Neo4j already allows for us to store arrays on a node.
- Via the Graph Data Science plugin, Neo4j supports the ability to compute the [similarity](https://neo4j.com/docs/graph-data-science/current/algorithms/similarity-functions/) between arrays in the database.
- In the event your application captures [spatial data](https://neo4j.com/docs/cypher-manual/current/syntax/spatial/) (e.g. lat/long), your algorithm could easily leverage that data to enhance the recommendations.
- One of the strengths of Neo4j is the ability to leverage relationships across our data.  We can use the flexible data model in order to associate a number of vectors to a given Command, allowing us to test different models without the need to change our database via schema migrations.


## Proof of Concept

To frame this proof of concept, consider an application that needs to "predict" the intent of a `Command`.  In this example, an API exists that allows an app to post a user's command and returns the top 5 similiar messages based on the embedding of each utterance.  The API generates an embedding for the Command on the fly, and queries the Neo4j database to find the top 5 similar commands based on the document embeddings related to the command.  

Below is an example of this simple data model:

![](https://snipboard.io/RHx0qz.jpg)

Other applications include:

- Support cases.  For example a customer submits a Case, and you can use the submission's embedding to identify the most similar cases that have already been resolved.
- Identify similar images in order to identify dupicates or perhaps inappropriate content


## The App

- Run a stack via docker that includes Neo4j and a python environment that you can attach to via VS Code.  Effectively, this is the virutal environment, removing the need for conda environments or the like.
- A FastAPI app that highlights how a system could post data to an API that is backed by Neo4j in order to generated the top 5 similar records.
- spacy is used to generate the document embedding on the fly for the posted message.

> It's worth noting that I am leveraging the apoc and GDS plugins for neo4j, but these were manually downloaded and added to the plugins folder.  


## Technical Notes

Below is an example of using the app backed by Neo4j to find the top similar messages and the associated intent.  For example, the command posted to the API was `turn off the lights`.

![](https://snipboard.io/qU9VWE.jpg)

The cypher query used:

```    
WITH {vec} as vector
MATCH (i:Intent)<--(c:Command)-[:HAS_VECTOR]->(e:Embedding)
WITH vector, c, i, gds.similarity.cosine(vector, e.vector) as sim
where sim > 0
RETURN c.text, i.intent, sim
ORDER BY sim desc
LIMIT 5
```

> The query is built with an f-string in python, which passes the vector to Neo4j to evaluate.  

## Notes

- The python script inside the dataset folder can be used to parse the CLINC150 dataset and load it into Neo4j.  
- The docker compose file should start up the Neo4j database with the apoc and graph-data-science plugins, as well as python dev environment that you can attach inside VS Code.
- Run the FastAPI app with `uvicorn api:app --reload`


