from db import GraphDB
def main():
 db=GraphDB()
 with db.driver.session() as s:
  for q in ["CREATE CONSTRAINT candidate_id IF NOT EXISTS FOR (n:Candidate) REQUIRE n.id IS UNIQUE","CREATE CONSTRAINT project_id IF NOT EXISTS FOR (n:Project) REQUIRE n.id IS UNIQUE","CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (n:Skill) REQUIRE n.name IS UNIQUE"]: s.run(q)
  people=[('c1','Aisha Khan','Frontend Engineer','React','expert',5),('c1','Aisha Khan','Frontend Engineer','TypeScript','advanced',4),('c1','Aisha Khan','Frontend Engineer','GraphQL','intermediate',2),('c2','Marco Silva','Platform Engineer','Python','expert',6),('c2','Marco Silva','Platform Engineer','Neo4j','advanced',3),('c3','Shashi Kiran','Software Engineer','Python','expert',4),('c3','Shashi Kiran','Software Engineer','Java','advanced',6)]
  s.run("UNWIND $rows AS r MERGE(c:Candidate{id:r.id}) SET c.name=r.name,c.title=r.title MERGE(x:Skill{name:r.skill}) MERGE(c)-[h:HAS_SKILL]->(x) SET h.level=r.level,h.years=r.years",rows=[dict(zip(['id','name','title','skill','level','years'],r)) for r in people])
  projects=[('p1','Customer Graph Explorer','Interactive relationship discovery for customer teams.','React','high'),('p1','Customer Graph Explorer','Interactive relationship discovery for customer teams.','GraphQL','high'),('p2','Developer Learning Map','Maps adjacent skills and personalized learning paths.','TypeScript','medium'),('p2','Developer Learning Map','Maps adjacent skills and personalized learning paths.','React','medium'),('p3','Graph Data API','A reliable API for connected operational data.','Python','high'),('p3','Graph Data API','A reliable API for connected operational data.','Neo4j','high')]
  s.run("UNWIND $rows AS r MERGE(p:Project{id:r.id}) SET p.name=r.name,p.description=r.description MERGE(x:Skill{name:r.skill}) MERGE(p)-[:REQUIRES{priority:r.priority}]->(x)",rows=[dict(zip(['id','name','description','skill','priority'],r)) for r in projects])
  rel=[('React','TypeScript',.9),('GraphQL','Neo4j',.7),('Python','GraphQL',.5)]
  s.run("UNWIND $rows AS r MERGE(a:Skill{name:r.a}) MERGE(b:Skill{name:r.b}) MERGE(a)-[x:RELATED_TO]-(b) SET x.strength=r.strength",rows=[dict(zip(['a','b','strength'],r)) for r in rel])
 db.close()
if __name__=='__main__':main()
