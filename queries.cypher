MATCH (c:Candidate {id:$candidate_id})-[:HAS_SKILL]->(owned:Skill)
MATCH path=(owned)-[:RELATED_TO*0..1]-(matched:Skill)<-[:REQUIRES]-(p:Project)
RETURN p.name,collect(DISTINCT matched.name) AS explanation,count(path) AS score ORDER BY score DESC;

MATCH (c:Candidate {id:$candidate_id})-[r:HAS_SKILL]->(s:Skill)
RETURN c.name,s.name,r.level,r.years;