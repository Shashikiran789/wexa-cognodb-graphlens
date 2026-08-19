import os
from neo4j import GraphDatabase
class GraphDB:
 def __init__(self):
  uri=os.getenv('COGNODB_URI'); password=os.getenv('COGNODB_PASSWORD')
  if not uri or not password: raise RuntimeError('Set COGNODB_URI and COGNODB_PASSWORD')
  self.driver=GraphDatabase.driver(uri,auth=(os.getenv('COGNODB_USER','cognodb'),password))
 def close(self): self.driver.close()
 def candidates(self):
  with self.driver.session() as s:return s.run("MATCH (c:Candidate) RETURN c.id AS id,c.name AS name,c.title AS title ORDER BY c.name").data()
 def explore(self,candidate_id):
  q="""MATCH (c:Candidate {id:$candidate_id}) OPTIONAL MATCH (c)-[h:HAS_SKILL]->(s:Skill)
  WITH c,collect({name:s.name,level:h.level,years:h.years}) AS skills
  OPTIONAL MATCH (c)-[:HAS_SKILL]->(owned:Skill)
  OPTIONAL MATCH path=(owned)-[:RELATED_TO*0..1]-(matched:Skill)<-[:REQUIRES]-(p:Project)
  WITH c,skills,p,collect(DISTINCT matched.name) AS matched WHERE p IS NOT NULL
  RETURN c.name AS candidate,skills,p.name AS project,p.description AS description,matched,size(matched) AS score
  ORDER BY score DESC,project"""
  with self.driver.session() as s:return s.run(q,candidate_id=candidate_id).data()
