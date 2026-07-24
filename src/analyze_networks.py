# -*- coding: utf-8 -*-
"""Build 5 networks from the dataset, run SNA algorithms, export PNG + interactive HTML."""
import csv, os, json, math
from collections import defaultdict
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pyvis.network import Network

DS="dataset"; OUT="networks"
os.makedirs(OUT, exist_ok=True)

def read(f):
    with open(f"{DS}/{f}", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))

persons  = {r["person"]: r for r in read("persons.csv")}
docs     = {r["doc_id"]: r for r in read("documents.csv")}
apps     = read("appearances.csv")
rels     = read("relations.csv")
coapp    = read("edges_coappearance.csv")

SECT_COLOR = {
 "Karaite":"#1f77b4", "Karaite (presumed)":"#7fb3d8", "Karaite (probable)":"#4a90c4",
 "Rabbanite":"#d62728", "Rabbanite (probable)":"#e88a8a", "unknown":"#999999",
}
def sect_of(p): return persons.get(p,{}).get("sect","unknown")
def color_of(p): return SECT_COLOR.get(sect_of(p), "#999999")

def top(d, n=12):
    return sorted(d.items(), key=lambda x:-x[1])[:n]

def analyze(G, name, weighted=True):
    """Run standard algorithms; return dict of dataframes-like dicts."""
    res = {}
    wkw = {"weight":"weight"} if weighted else {}
    res["degree"] = dict(G.degree())
    res["wdegree"] = dict(G.degree(weight="weight")) if weighted else res["degree"]
    # distance-based measures: use inverse weight as distance
    for u,v,d in G.edges(data=True):
        d["dist"] = 1.0/d.get("weight",1)
    res["betweenness"] = nx.betweenness_centrality(G, weight="dist", normalized=True)
    try:
        res["eigenvector"] = nx.eigenvector_centrality(G, max_iter=2000, weight="weight")
    except Exception:
        res["eigenvector"] = {}
    res["pagerank"] = nx.pagerank(G, weight="weight")
    comms = nx.community.louvain_communities(G, weight="weight", seed=42)
    res["communities"] = comms
    res["modularity"] = nx.community.modularity(G, comms, weight="weight")
    res["n_nodes"]=G.number_of_nodes(); res["n_edges"]=G.number_of_edges()
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    res["n_components"]=len(comps); res["giant"]=len(comps[0]) if comps else 0
    res["density"]=nx.density(G)
    return res

def write_metrics(G, res, name):
    node2comm = {}
    for i,c in enumerate(res["communities"]):
        for n in c: node2comm[n]=i
    with open(f"{OUT}/{name}_metrics.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f)
        w.writerow(["node","sect","degree","weighted_degree","betweenness","eigenvector","pagerank","community"])
        for n in G.nodes():
            w.writerow([n, sect_of(n), res["degree"].get(n,0), res["wdegree"].get(n,0),
                        round(res["betweenness"].get(n,0),5), round(res["eigenvector"].get(n,0),5),
                        round(res["pagerank"].get(n,0),5), node2comm.get(n,"")])
    return node2comm

def draw_png(G, name, title, node2comm=None, res=None, color_by="sect", figsize=(22,18), labels_top=40):
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, weight="weight", seed=7, k=1.6/math.sqrt(max(G.number_of_nodes(),2)))
    if color_by=="community" and node2comm is not None:
        cmap = plt.cm.tab20
        colors=[cmap(node2comm.get(n,0)%20) for n in G.nodes()]
    else:
        colors=[color_of(n) for n in G.nodes()]
    if res:
        pr = res["pagerank"]; sizes=[300+30000*pr.get(n,0) for n in G.nodes()]
    else:
        deg = dict(G.degree()); sizes=[120+90*deg[n] for n in G.nodes()]
    weights=[G[u][v].get("weight",1) for u,v in G.edges()]
    nx.draw_networkx_edges(G,pos,alpha=0.25,width=[0.5+0.9*w for w in weights],edge_color="#777777")
    nx.draw_networkx_nodes(G,pos,node_color=colors,node_size=sizes,alpha=0.92,linewidths=0.6,edgecolors="#333333")
    if res:
        keyn = set(n for n,_ in top(res["pagerank"], labels_top)) | set(n for n,_ in top(res["betweenness"], 15))
    else:
        keyn = set(sorted(G.nodes(), key=lambda n:-G.degree(n))[:labels_top])
    nx.draw_networkx_labels(G,pos,labels={n:n for n in G.nodes() if n in keyn},font_size=8)
    plt.title(title, fontsize=17)
    plt.axis("off"); plt.tight_layout()
    plt.savefig(f"{OUT}/{name}.png", dpi=150, facecolor="white"); plt.close()

def draw_html(G, name, title, res=None, node2comm=None, extra_node_info=None, height="900px"):
    net = Network(height=height, width="100%", bgcolor="#ffffff", font_color="#222222",
                  select_menu=True, filter_menu=False, notebook=False, cdn_resources="remote")
    net.force_atlas_2based(gravity=-60, central_gravity=0.008, spring_length=110, damping=0.55)
    pr = (res or {}).get("pagerank", {})
    bt = (res or {}).get("betweenness", {})
    for n in G.nodes(data=True):
        node, d = n
        s = sect_of(node)
        size = 12 + (2500*pr.get(node,0) if pr else 2*G.degree(node))
        info = [f"<b>{node}</b>", f"Sect: {s}"]
        p = persons.get(node)
        if p:
            if p["roles"]: info.append("Roles: "+p["roles"])
            if p["docs"]: info.append("Documents: "+p["docs"])
            if p["year_min"]: info.append(f"Years: {p['year_min']}-{p['year_max']}")
            if p["places"]: info.append("Places: "+p["places"])
            if p["sect_evidence"]: info.append("Sect evidence: "+p["sect_evidence"])
        if pr: info.append(f"PageRank: {pr.get(node,0):.4f} | Betweenness: {bt.get(node,0):.4f}")
        if node2comm is not None: info.append(f"Community: {node2comm.get(node,'-')}")
        if extra_node_info and node in extra_node_info: info.append(extra_node_info[node])
        net.add_node(node, label=node, color=d.get("color", color_of(node)), size=size,
                     title="\n".join(x.replace("<b>","").replace("</b>","") for x in info))
    for u,v,d in G.edges(data=True):
        t = d.get("label","")
        w = d.get("weight",1)
        ttl = (f"{t} | " if t else "") + f"weight {w}" + (f" | docs: {d['docs']}" if d.get("docs") else "")
        net.add_edge(u,v,value=w,title=ttl,color=d.get("color","#9a9a9a"))
    net.heading = title
    net.write_html(f"{OUT}/{name}.html", notebook=False)

report = {}

# =====================================================================
# N1: Full person-person co-appearance network (weighted)
G1 = nx.Graph()
for r in coapp:
    G1.add_edge(r["source"], r["target"], weight=int(r["weight"]), docs=r["docs"])
res1 = analyze(G1,"N1")
n2c1 = write_metrics(G1,res1,"N1_coappearance")
draw_png(G1,"N1_coappearance_sect","N1. Co-appearance network of all persons (node color = sect, size = PageRank)",res=res1)
draw_png(G1,"N1_coappearance_communities","N1. Co-appearance network - Louvain communities",node2comm=n2c1,res=res1,color_by="community")
draw_html(G1,"N1_coappearance","N1. Co-appearance network (all persons, weighted)",res=res1,node2comm=n2c1)
report["N1"]={"nodes":res1["n_nodes"],"edges":res1["n_edges"],"components":res1["n_components"],
 "giant":res1["giant"],"density":round(res1["density"],4),"modularity":round(res1["modularity"],3),
 "n_communities":len(res1["communities"]),
 "top_degree":top(res1["degree"]),"top_wdegree":top(res1["wdegree"]),
 "top_betweenness":top(res1["betweenness"]),"top_eigen":top(res1["eigenvector"]),"top_pagerank":top(res1["pagerank"])}

# =====================================================================
# N2: Bipartite person-document network
G2 = nx.Graph()
for a in apps:
    if a["role"]=="Mentioned" or a["certainty"]=="contextual": continue
    d = a["doc_id"]
    G2.add_node(d, kind="doc", color="#2ca02c")
    G2.add_node(a["person"], kind="person", color=color_of(a["person"]))
    if G2.has_edge(a["person"], d):
        G2[a["person"]][d]["weight"] += 1
        G2[a["person"]][d]["label"] += ", "+a["role"]
    else:
        G2.add_edge(a["person"], d, weight=1, label=a["role"])
deg_docs = {n:G2.degree(n) for n,dd in G2.nodes(data=True) if dd.get("kind")=="doc"}
deg_pers = {n:G2.degree(n) for n,dd in G2.nodes(data=True) if dd.get("kind")=="person"}
res2 = analyze(G2,"N2")
n2c2 = write_metrics(G2,res2,"N2_bipartite")
extra = {d:"DOCUMENT: "+docs[d]["shelfmark"]+" | "+docs[d]["doc_type"]+" | "+docs[d]["date_text"]+" | "+docs[d]["place"] for d in docs if d in G2}
draw_png(G2,"N2_bipartite","N2. Bipartite person-document network (green = documents)",res=res2)
draw_html(G2,"N2_bipartite","N2. Bipartite person-document network",res=res2,node2comm=n2c2,extra_node_info=extra)
report["N2"]={"nodes":res2["n_nodes"],"edges":res2["n_edges"],"components":res2["n_components"],"giant":res2["giant"],
 "top_docs_by_people":top(deg_docs),"top_people_by_docs":top(deg_pers),
 "top_betweenness":top(res2["betweenness"])}

# =====================================================================
# N3: Kinship, marriage and agency network (typed edges)
REL_COLOR={"married":"#d62728","betrothed":"#ff7f0e","divorced":"#8c564b","father_of":"#1f77b4",
 "mother_of":"#17becf","sibling_of":"#2ca02c","first_cousin_of":"#98df8a","uncle_of":"#9467bd",
 "agent_for":"#e377c2","gave_gift_to":"#bcbd22","first_husband_of":"#7f7f7f","groom_agent_for":"#e377c2"}
G3 = nx.Graph()
for r in rels:
    s,t,rel = r["source"], r["target"], r["relation"]
    G3.add_edge(s,t,weight=2 if rel in("married","betrothed") else 1,
                label=rel,color=REL_COLOR.get(rel,"#aaaaaa"),docs=r["evidence"])
res3 = analyze(G3,"N3")
n2c3 = write_metrics(G3,res3,"N3_kinship")
draw_png(G3,"N3_kinship","N3. Kinship, marriage and agency network (color = sect)",res=res3,figsize=(24,20),labels_top=70)
draw_html(G3,"N3_kinship","N3. Kinship, marriage and agency network (edge colors = relation type)",res=res3,node2comm=n2c3)
comp3 = sorted(nx.connected_components(G3), key=len, reverse=True)
report["N3"]={"nodes":res3["n_nodes"],"edges":res3["n_edges"],"components":res3["n_components"],
 "largest_families":[sorted(c)[:8] for c in comp3[:6]],"largest_sizes":[len(c) for c in comp3[:8]],
 "top_betweenness":top(res3["betweenness"]),"top_degree":top(res3["degree"])}

# =====================================================================
# N4: Cross-sect (Karaite-Rabbanite) contact network
# co-appearance edges where the two endpoints have different sect groups (K vs R),
# plus, for context, all edges incident to Rabbanite nodes.
def sect_group(p):
    s = sect_of(p)
    if s.startswith("Karaite"): return "K"
    if s.startswith("Rabbanite"): return "R"
    return "U"
G4 = nx.Graph()
rabb = {p for p in persons if sect_group(p)=="R"}
for r in coapp:
    a,b=r["source"],r["target"]
    ga,gb=sect_group(a),sect_group(b)
    if "R" in (ga,gb):
        G4.add_edge(a,b,weight=int(r["weight"]),docs=r["docs"])
# also mixed marriages / relations edges involving R
for r in rels:
    if sect_group(r["source"])=="R" or sect_group(r["target"])=="R":
        if not G4.has_edge(r["source"],r["target"]):
            G4.add_edge(r["source"],r["target"],weight=1,docs=r["evidence"],label=r["relation"])
res4 = analyze(G4,"N4")
n2c4 = write_metrics(G4,res4,"N4_cross_sect")
draw_png(G4,"N4_cross_sect","N4. Karaite-Rabbanite contact network (red = Rabbanite, blue = Karaite)",res=res4,figsize=(20,16),labels_top=60)
draw_html(G4,"N4_cross_sect","N4. Karaite-Rabbanite contact network",res=res4,node2comm=n2c4)
kr_edges = [(u,v) for u,v in G4.edges() if {sect_group(u),sect_group(v)}=={"K","R"}]
docs_with_R = sorted({d for a in apps if sect_group(a["person"])=="R" for d in [a["doc_id"]]})
report["N4"]={"nodes":res4["n_nodes"],"edges":res4["n_edges"],
 "direct_KR_edges":len(kr_edges),"docs_with_rabbanites":docs_with_R,
 "rabbanite_nodes":sorted(rabb),
 "top_betweenness":top(res4["betweenness"]),"top_pagerank":top(res4["pagerank"])}

# =====================================================================
# N5: Witness / scribe co-signature network
WROLES={"Witness","WitnessOfAgency","Scribe"}
doc_w = defaultdict(set)
for a in apps:
    if a["role"] in WROLES and a["certainty"]!="contextual":
        doc_w[a["doc_id"]].add(a["person"])
G5 = nx.Graph()
pair=defaultdict(set)
for d,people in doc_w.items():
    pp=sorted(people)
    for i in range(len(pp)):
        for j in range(i+1,len(pp)):
            pair[(pp[i],pp[j])].add(d)
for (a,b),ds in pair.items():
    G5.add_edge(a,b,weight=len(ds),docs=", ".join(sorted(ds)))
res5 = analyze(G5,"N5")
n2c5 = write_metrics(G5,res5,"N5_witnesses")
draw_png(G5,"N5_witnesses","N5. Witness & scribe co-signature network (color = sect)",res=res5,figsize=(20,16),labels_top=50)
draw_html(G5,"N5_witnesses","N5. Witness & scribe co-signature network",res=res5,node2comm=n2c5)
report["N5"]={"nodes":res5["n_nodes"],"edges":res5["n_edges"],"components":res5["n_components"],
 "giant":res5["giant"],"n_communities":len(res5["communities"]),"modularity":round(res5["modularity"],3),
 "top_betweenness":top(res5["betweenness"]),"top_degree":top(res5["degree"]),"top_pagerank":top(res5["pagerank"])}

with open(f"{OUT}/analysis_summary.json","w",encoding="utf-8") as f:
    json.dump(report,f,indent=1,ensure_ascii=False)
print(json.dumps(report,indent=1,ensure_ascii=False)[:6000])
