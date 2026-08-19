from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse
from db import GraphDB
app=FastAPI(title='GraphLens')
def page(x):return HTMLResponse(f"""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><style>body{{margin:auto;max-width:950px;padding:40px 20px;background:#08111f;color:#edf4ff;font:16px system-ui}}h1{{font-size:clamp(36px,7vw,68px);line-height:1;margin-bottom:12px}}p{{color:#9fb0c8;line-height:1.6}}select,button{{padding:13px;border-radius:10px;background:#101d31;color:white;border:1px solid #29405f;font-size:15px}}button{{background:#69e1c0;color:#06221b;font-weight:700}}form{{display:flex;gap:10px;margin:30px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:15px}}article{{padding:20px;background:#101d31;border:1px solid #29405f;border-radius:15px}}.tag{{display:inline-block;padding:5px 9px;background:#1a304d;border-radius:99px;margin:3px;color:#c8d7ea}}a{{color:#69e1c0}}.score{{float:right;color:#69e1c0}}</style><p>Graph<span style='color:#69e1c0'>Lens</span> · CognoDB powered</p>{x}""")
@app.get('/',response_class=HTMLResponse)
def home():
 try:
  d=GraphDB(); people=d.candidates(); d.close(); opts=''.join(f'<option value="{p["id"]}">{p["name"]} — {p["title"]}</option>' for p in people)
  return page(f'<h1>See the connections behind the work.</h1><p>Explore how skills connect people to projects through direct and adjacent capabilities.</p><form action=/explore><select name=candidate_id required><option value="">Choose a person...</option>{opts}</select><button>Explore graph →</button></form>')
 except Exception as e:return page(f'<article><h2>Database unavailable</h2><p>Check CognoDB environment variables and instance status.</p><small>{e}</small></article>')
@app.get('/explore',response_class=HTMLResponse)
def explore(candidate_id:str=Query(...)):
 try:
  d=GraphDB(); rows=d.explore(candidate_id); d.close()
  if not rows:return page('<h2>No connections found</h2><p>Try another profile.</p><a href="/">← Back</a>')
  skills=''.join(f'<span class=tag>{x["name"]} · {x["level"]}</span>' for x in rows[0]['skills']); cards=''.join(f'<article><span class=score>{r["score"]} paths</span><h2>{r["project"]}</h2><p>{r["description"]}</p><small>Matched through</small><div>'+''.join(f'<span class=tag>{m}</span>' for m in r['matched'] if m)+'</div></article>' for r in rows)
  return page(f'<a href="/">← Back</a><h1>{rows[0]["candidate"]}</h1><p>Known skills</p><div>{skills}</div><h2>Recommended projects</h2><p>Ranked and explained using graph paths.</p><div class=grid>{cards}</div>')
 except Exception as e:return page(f'<article><h2>Could not explore graph</h2><p>Please try again.</p><small>{e}</small></article>')
