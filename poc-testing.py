# imports
import pandas as pd 
from py2neo import Graph

# auth - references the service header, not the network name or localhost
graph = Graph("bolt://neo4j:7687", auth=('neo4j', 'neo'))

# how many nodes
CQL = "MATCH (n) return count(n);"
graph.run().to_data_frame()

# 


