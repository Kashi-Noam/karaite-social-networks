# -*- coding: utf-8 -*-
"""
SNA on the v2 database: five networks, centrality + community algorithms,
publication figures (PNG) and interactive views (HTML).

cd src && python3 analyze_v2.py
"""
import csv, os, json, math
from collections import defaultdict, Counter
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyBboxPatch
from pyvis.network import Network

DS, OUT = "../dataset", "../networks"
os.makedirs(OUT, exist_ok=True)

def read(f): return list(csv.DictReader(open(f"{DS}/{f}", encoding="utf-8-sig")))
persons = {p["canonical_name"]: p for p in read("persons.csv")}
docs    = {d["shelfmark"]: d for d in read("documents.csv")}
apps    = read("appearances.csv")
rels    = read("relations.csv")
coapp   = read("edges_coappearance.csv")

def sect(p):  return persons.get(p, {}).get("sect", "unknown")
def group(p):
    s = sect(p)
    return "K" if s.startswith("Karaite") else ("R" if s.startswith("Rabbanite") else "U")
COL = {"Karaite":"#3d6b8e","Karaite (probable)":"#6d94b0","Karaite (presumed)":"#b6cbdb",
       "Rabbanite":"#a8555a","Rabbanite (probable)":"#cf9a9d","unknown":"#b8b3ad"}
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,
                     "axes.edgecolor":"none","savefig.facecolor":"white"})
def col(p): return COL.get(sect(p), "#9e9e9e")
def pid(p):  return persons.get(p, {}).get("person_id", "")
def short(p):
    """short display label"""
    p = p.replace(" ha-Kohen","").replace(" ha-Levi","").replace(" (nasi)"," [N]").replace(" (he-haver)","")
    return p if len(p) <= 30 else p[:29]+"…"

def top(d, n=10): return sorted(d.items(), key=lambda x: -x[1])[:n]

def analyze(G):
    for u, v, d in G.edges(data=True):
        d["dist"] = 1.0/max(d.get("weight",1), 1)
    r = {"degree":dict(G.degree()), "wdegree":dict(G.degree(weight="weight")),
         "betweenness":nx.betweenness_centrality(G, weight="dist", normalized=True),
         "closeness":nx.closeness_centrality(G, distance="dist"),
         "pagerank":nx.pagerank(G, weight="weight")}
    try: r["eigenvector"] = nx.eigenvector_centrality(G, max_iter=3000, weight="weight")
    except Exception: r["eigenvector"] = {n:0 for n in G}
    c = nx.community.louvain_communities(G, weight="weight", seed=42)
    r["communities"] = c
    r["modularity"] = nx.community.modularity(G, c, weight="weight")
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    r.update(n_nodes=G.number_of_nodes(), n_edges=G.number_of_edges(),
             n_components=len(comps), giant=len(comps[0]) if comps else 0,
             density=nx.density(G), avg_degree=2*G.number_of_edges()/max(G.number_of_nodes(),1))
    return r

def write_metrics(G, r, name):
    n2c = {n:i for i,c in enumerate(r["communities"]) for n in c}
    with open(f"{OUT}/{name}_metrics.csv","w",newline="",encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["person_id","node","sect","degree","weighted_degree","betweenness","closeness","eigenvector","pagerank","community"])
        for n in sorted(G, key=lambda x: -r["pagerank"].get(x,0)):
            w.writerow([pid(n), n, sect(n), r["degree"].get(n,0), r["wdegree"].get(n,0),
                        round(r["betweenness"].get(n,0),5), round(r["closeness"].get(n,0),5),
                        round(r["eigenvector"].get(n,0),5),
                        round(r["pagerank"].get(n,0),5), n2c.get(n,"")])
    return n2c


def _relax(pos, radius, size, iters=150, pad=1.35, groups=None, fixed_scale=False):
    """Push apart nodes whose drawn circles would overlap on the page.
    radius is in points; the layout is rescaled through the figure size so that
    the separation test is done in the units the reader actually sees.

    By default the data-units-per-point scale is recomputed every iteration
    from the current spread, which lets the canvas grow as crowded nodes push
    apart. For a dense graph that recompute can runs away: pushing one pair
    apart grows the span, which shrinks everyone else's point-distance under
    the recompute, triggering a wider wave of pushes, growing the span again.
    fixed_scale=True freezes the scale at the starting layout instead, so a
    push only ever resolves the pair it was computed for.
    """
    nodes = list(pos)
    blocks = [list(g) for g in groups] if groups else [nodes]
    fixed_upx = fixed_upy = None
    if fixed_scale:
        xs = [pos[n][0] for n in nodes]; ys = [pos[n][1] for n in nodes]
        spanx = (max(xs)-min(xs)) or 1.0; spany = (max(ys)-min(ys)) or 1.0
        fixed_upx = spanx/(0.92*size[0]*72.0); fixed_upy = spany/(0.92*size[1]*72.0)
    for _ in range(iters):
        if fixed_scale:
            upx, upy = fixed_upx, fixed_upy
        else:
            xs = [pos[n][0] for n in nodes]; ys = [pos[n][1] for n in nodes]
            spanx = (max(xs)-min(xs)) or 1.0; spany = (max(ys)-min(ys)) or 1.0
            upx = spanx/(0.92*size[0]*72.0); upy = spany/(0.92*size[1]*72.0)
        moved = 0.0
        for blk in blocks:
         for i in range(len(blk)):
            a = blk[i]
            for j in range(i+1, len(blk)):
                b = blk[j]
                dx = (pos[b][0]-pos[a][0])/upx; dy = (pos[b][1]-pos[a][1])/upy
                d = math.hypot(dx, dy) or 1e-6
                need = pad*(radius[a]+radius[b])
                if d < need:
                    push = (need-d)/2.0; ux, uy = dx/d, dy/d
                    pos[a] = (pos[a][0]-ux*push*upx, pos[a][1]-uy*push*upy)
                    pos[b] = (pos[b][0]+ux*push*upx, pos[b][1]+uy*push*upy)
                    moved += push
        if moved < 0.4: break
    return pos

def fig(G, name, title, r=None, n2c=None, color_by="sect", size=(16,12), label_n=28, legend=True, layout="spring", kfac=1.5, min_gap=0.019, fsize=12, must=(), nmin=40, nspan=780, outdir=None, relax=True):
    plt.figure(figsize=size)
    if layout=="grid":
        # One cell per component, but the cell grows with the component, so a
        # crowded twenty node cluster is not squeezed into the same box as a
        # thirteen node star. Cells are packed onto shelves left to right.
        comps = sorted(nx.connected_components(G), key=len, reverse=True)
        pos = {}
        WIDTH = 4.2
        x_cursor, y_cursor, shelf_h = 0.0, 0.0, 0.0
        solo = len(comps) > 1 and len(comps[0]) >= 1.4*len(comps[1])
        for idx, comp in enumerate(comps):
            sub = G.subgraph(comp)
            sp = nx.kamada_kawai_layout(sub, weight="dist") if len(comp) > 2 else \
                 nx.circular_layout(sub)
            xs = [p[0] for p in sp.values()] or [0]; ys = [p[1] for p in sp.values()] or [0]
            w = (max(xs)-min(xs)) or 1; h = (max(ys)-min(ys)) or 1
            rad = 0.12*math.sqrt(len(comp)) + 0.07
            if idx == 0 and solo:
                rad = 1.05                      # the densest component gets a row of its own
            if x_cursor > 0 and x_cursor + 2*rad > WIDTH:
                x_cursor = 0.0; y_cursor -= shelf_h + 0.35; shelf_h = 0.0
            cx, cy = x_cursor + rad, y_cursor - rad
            for n,(x,y) in sp.items():
                pos[n] = (cx + rad*(x-(max(xs)+min(xs))/2)/(w/2 or 1),
                          cy + rad*(y-(max(ys)+min(ys))/2)/(h/2 or 1))
            x_cursor += 2*rad + 0.35
            shelf_h = max(shelf_h, 2*rad)
            if idx == 0 and solo:
                x_cursor = WIDTH               # force the next component onto a new shelf
    elif layout=="kk" and G.number_of_nodes() < 200:
        pos = nx.kamada_kawai_layout(G, dist=None, weight="dist")
    else:
        pos = nx.spring_layout(G, weight="weight", seed=11, k=kfac/math.sqrt(max(G.number_of_nodes(),2)), iterations=300)
    if color_by == "community" and n2c:
        cm = plt.cm.tab20; colors=[cm(n2c.get(n,0)%20) for n in G]
    else:
        colors=[col(n) for n in G]
    pr = (r or {}).get("pagerank", {})
    mx = max(pr.values()) if pr else 1
    sizes = [nmin+nspan*pr.get(n,0)/mx for n in G] if pr else [nmin+14*G.degree(n) for n in G]
    if relax:
        pos = _relax(pos, {n: math.sqrt(a/math.pi) for n, a in zip(list(G), sizes)}, size,
                     groups=(sorted(nx.connected_components(G), key=len, reverse=True)
                             if layout=="grid" else None))
    ws = [G[u][v].get("weight",1) for u,v in G.edges()]
    nx.draw_networkx_edges(G,pos,alpha=0.20,width=[0.4+0.7*w for w in ws],edge_color="#8d8d8d")
    nx.draw_networkx_nodes(G,pos,node_color=colors,node_size=sizes,alpha=0.95,linewidths=0.6,edgecolors="#54514d")
    keys = set(n for n,_ in top(pr, label_n)) | set(n for n,_ in top((r or {}).get("betweenness",{}), 12))
    # Drop labels whose boxes would overlap one already placed. The box is estimated
    # from the character count and the figure size, so long names claim more room.
    xs_ = [p[0] for p in pos.values()] or [0]; ys_ = [p[1] for p in pos.values()] or [0]
    spanx = (max(xs_)-min(xs_)) or 1; spany = (max(ys_)-min(ys_)) or 1
    cw = 0.62*fsize/72.0 * spanx/(0.92*size[0])      # data units per character
    ch = 1.85*fsize/72.0 * spany/(0.92*size[1])      # data units per label height
    # the label sits just under its node, so the circle itself stays visible
    upy = spany/(0.92*size[1]*72.0)
    lpos = {n: (pos[n][0], pos[n][1] - (math.sqrt(a/math.pi)*upy) - 0.62*ch)
            for n, a in zip(list(G), sizes)}
    placed=[]
    lab={}
    order = [n for n in must if n in G] + [n for n,_ in sorted(((n,pr.get(n,0)) for n in G if n in keys),
                                                                key=lambda x:-x[1]) if n not in must]
    for n in order:
        x,y=lpos[n]; s=short(n)
        w=max(len(s)*cw, 3*cw)/2 + 1.7*cw; h=ch/2
        if all(abs(x-px) > w+pw or abs(y-py) > h+ph for px,py,pw,ph in placed):
            placed.append((x,y,w,h)); lab[n]=s
    nx.draw_networkx_labels(G,lpos,labels=lab,font_size=fsize,font_color="#26241f",
        bbox=dict(boxstyle="round,pad=0.3",fc="#fffdf8",ec="#cfc9c0",lw=0.6,alpha=0.94))
    # the axes must contain the label boxes too, not only the nodes
    _lx0 = min([px-pw for px,py,pw,ph in placed] + [min(xs_)])
    _lx1 = max([px+pw for px,py,pw,ph in placed] + [max(xs_)])
    _ly0 = min([py-ph for px,py,pw,ph in placed] + [min(ys_)])
    _ly1 = max([py+ph for px,py,pw,ph in placed] + [max(ys_)])
    plt.xlim(_lx0-1.5*cw, _lx1+1.5*cw); plt.ylim(_ly0-0.8*ch, _ly1+0.8*ch)
    if legend and color_by=="sect":
        plt.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=9,label=s)
                            for s,c in COL.items()], loc="upper center", bbox_to_anchor=(0.5,-0.005),
                   ncol=6, fontsize=10, frameon=False, handletextpad=0.3, columnspacing=1.4)
    if os.environ.get("FIGTITLES","1")=="1":
        plt.title(title, fontsize=14)
    plt.axis("off"); plt.tight_layout()
    plt.savefig(f"{outdir or OUT}/{name}.png", dpi=200, facecolor="white"); plt.close()


# =============================================================== full-page plain graphs
# These are ordinary node-link drawings, same as fig() -- circles, edges, every
# person labelled -- but sized to fill one dedicated page rather than sharing a
# page with body text, and laid out directly in points (1 data unit = 1pt) so
# a push never has to be re-scaled mid-relaxation. The earlier version rescaled
# the data-units-per-point conversion every iteration (matching what fig()
# does), which for a dense 66-node graph fed back on itself -- pushing one
# pair apart grew the span, which under the recompute shrank everyone else's
# point-distance, triggering a wider wave of pushes, growing the span again --
# and ran away to overflow. Working in points from the start removes that
# feedback loop entirely.
#
# Each node's footprint is an axis-aligned box (circle on top, label below),
# not a circle padded out to cover the label -- a box lets two nodes sit
# closer when their labels don't actually occupy the same direction, which
# matters because label text, not the circle, is what has to fit 40-60
# people onto one page. Overlap is resolved on whichever axis needs the
# smaller push, standard rectangle-separation.
def _relax_boxes(pos, boxes, iters=1500, pad=1.05):
    """pos, boxes already in points. boxes[n] = (halfw, top, bot): the box
    spans x in [-halfw,+halfw] and y in [-bot,+top] relative to the node."""
    nodes = list(pos)
    for _ in range(iters):
        moved = 0.0
        for i in range(len(nodes)):
            a = nodes[i]; hwa, topa, bota = boxes[a]
            ax, ay = pos[a]
            for j in range(i+1, len(nodes)):
                b = nodes[j]; hwb, topb, botb = boxes[b]
                bx, by = pos[b]
                ddx = bx-ax; ddy = by-ay
                ox = (hwa+hwb)*pad - abs(ddx)
                oy = (min(topa, ddy+topb) - max(-bota, ddy-botb))*pad
                if ox > 0 and oy > 0:
                    moved += min(ox, oy)
                    if ox < oy:
                        s = 1.0 if ddx >= 0 else -1.0
                        push = s*ox/2.0
                        ax -= push; bx += push
                    else:
                        s = 1.0 if ddy >= 0 else -1.0
                        push = s*oy/2.0
                        ay -= push; by += push
                    pos[a] = (ax, ay); pos[b] = (bx, by)
        if moved < 0.5: break
    return pos

def _extent_area(pos, boxes):
    x0 = min(pos[n][0]-boxes[n][0] for n in pos); x1 = max(pos[n][0]+boxes[n][0] for n in pos)
    y0 = min(pos[n][1]-boxes[n][2] for n in pos); y1 = max(pos[n][1]+boxes[n][1] for n in pos)
    return (x1-x0)*(y1-y0)

def _compact_pack(pos, boxes, iters=600, pad=1.05, rounds=16, shrink=0.93):
    """Plain relaxation only ever pushes apart -- nothing pulls the layout
    back together once early pushes have spread it out, so it tends to settle
    into a loose, elongated packing with a lot of dead space. This alternates
    a global shrink toward the centroid with a re-relax, keeping the result
    only when it actually got smaller, which is what pushes packing density
    up from ~20% toward something a page-budget estimate can rely on."""
    pos = _relax_boxes(pos, boxes, iters=iters, pad=pad)
    best_area = _extent_area(pos, boxes)
    for _ in range(rounds):
        cx = sum(p[0] for p in pos.values())/len(pos)
        cy = sum(p[1] for p in pos.values())/len(pos)
        trial = {n: (cx+(x-cx)*shrink, cy+(y-cy)*shrink) for n, (x, y) in pos.items()}
        trial = _relax_boxes(trial, boxes, iters=iters, pad=pad)
        area = _extent_area(trial, boxes)
        if area < best_area*0.995:
            pos, best_area = trial, area
        else:
            break
    return pos

def _fold_to_aspect(pos, boxes, target_ratio):
    """Box relaxation only ever pushes apart, never pulls together, and for a
    scatter of short-and-wide boxes the cheapest push to resolve any given
    overlap is almost always vertical (the short axis needs less absolute
    displacement to clear), so many independent pairwise pushes add up to one
    emergent bias: the whole layout stacks into a tall thin column (or, less
    often, a wide thin row) instead of filling a page in two dimensions. This
    slices that strip into `K` bands and lays them side by side or stacked,
    the way a printed sheet gets folded into columns -- a plain rearrangement
    (each band keeps its internal relative positions, so no overlap it didn't
    already have) rather than a physics step, and is what actually fixes the
    aspect ratio."""
    x0 = min(pos[n][0]-boxes[n][0] for n in pos); x1 = max(pos[n][0]+boxes[n][0] for n in pos)
    y0 = min(pos[n][1]-boxes[n][2] for n in pos); y1 = max(pos[n][1]+boxes[n][1] for n in pos)
    w, h = x1-x0, y1-y0
    cur = w/h if h else 1.0
    if 0.85*target_ratio <= cur <= target_ratio/0.85:
        return pos
    new_pos = dict(pos)
    if cur < target_ratio:
        K = max(1, round(math.sqrt(target_ratio*(h/w))))
        if K <= 1: return pos
        order = sorted(pos, key=lambda n: pos[n][1])
        seg = math.ceil(len(order)/K)
        col_w = w*1.15
        for ci in range(K):
            chunk = order[ci*seg:(ci+1)*seg]
            if not chunk: continue
            base_y = min(pos[n][1] for n in chunk)
            for n in chunk:
                new_pos[n] = (pos[n][0] + ci*col_w, pos[n][1] - base_y)
    else:
        K = max(1, round(math.sqrt((w/h)/target_ratio)))
        if K <= 1: return pos
        order = sorted(pos, key=lambda n: pos[n][0])
        seg = math.ceil(len(order)/K)
        row_h = h*1.15
        for ri in range(K):
            chunk = order[ri*seg:(ri+1)*seg]
            if not chunk: continue
            base_x = min(pos[n][0] for n in chunk)
            for n in chunk:
                new_pos[n] = (pos[n][0] - base_x, pos[n][1] + ri*row_h)
    return new_pos

def _node_boxes(G, r, fsize):
    pr = (r or {}).get("pagerank", {}); mx = max(pr.values()) if pr else 1
    radius, boxes = {}, {}
    for nd in G:
        area = 45 + 620*pr.get(nd, 0)/mx
        rad = math.sqrt(area/math.pi); radius[nd] = rad
        lw = len(short(nd))*0.585*fsize + 9
        lh = fsize*1.28 + 5
        boxes[nd] = (max(rad, lw/2), rad, rad + 3 + lh)
    return radius, boxes

def fig_page(G, name, title, r, fsize=11, outdir=None, seed=11,
             portrait_wh=(7.6, 9.1), landscape_wh=(10.1, 6.6), legend=True,
             min_fsize=6.5):
    n = G.number_of_nodes()
    k = 2.4/math.sqrt(max(n, 2))
    pos0 = nx.spring_layout(G, weight="weight", seed=seed, k=k, iterations=500)
    xs0 = [p[0] for p in pos0.values()]; ys0 = [p[1] for p in pos0.values()]
    spanx0 = (max(xs0)-min(xs0)) or 1; spany0 = (max(ys0)-min(ys0)) or 1
    cx = sum(xs0)/n; cy = sum(ys0)/n
    # orientation is decided once, from the graph's own raw spring shape --
    # not from whatever shape the box-packing settles into, since that can be
    # distorted by the vertical-stacking bias _fold_to_aspect corrects for
    landscape = (spanx0/spany0) > 1.15
    budget_w, budget_h = (landscape_wh if landscape else portrait_wh)
    budget_w, budget_h = budget_w*72*0.92, budget_h*72*0.92
    target_ratio = budget_w/budget_h

    fs = fsize
    while True:
        radius, boxes = _node_boxes(G, r, fs)
        # seed the point-space scale from the average box footprint, so relax
        # starts near its target size instead of needing to expand by orders
        # of magnitude (which is what made the naive version unstable).
        # The search over fsize only needs an approximate fit estimate, so it
        # runs a cheap, short pack; the expensive high-quality pack (more
        # iterations, more compaction rounds) only runs once, after the
        # right fsize is already known -- doing it on every trial fsize is
        # what made this loop slow enough to time out.
        avg_w = sum(2*hw for hw, _, _ in boxes.values())/n
        scale = avg_w*1.35*math.sqrt(n) / max(spanx0, spany0)
        pos = {nd: ((pos0[nd][0]-cx)*scale, (pos0[nd][1]-cy)*scale) for nd in G}
        pos = _compact_pack(pos, boxes, iters=180, pad=1.05, rounds=4)
        pos = _fold_to_aspect(pos, boxes, target_ratio)
        pos = _compact_pack(pos, boxes, iters=150, pad=1.05, rounds=3)

        x0 = min(pos[nd][0]-boxes[nd][0] for nd in G); x1 = max(pos[nd][0]+boxes[nd][0] for nd in G)
        y0 = min(pos[nd][1]-boxes[nd][2] for nd in G); y1 = max(pos[nd][1]+boxes[nd][1] for nd in G)
        need_w, need_h = (x1-x0), (y1-y0)
        fit = max(need_w/budget_w, need_h/budget_h)
        if fit <= 1.0 or fs <= min_fsize:
            break
        fs = max(min_fsize, fs*max(0.85, math.sqrt(1/fit)))

    # the fsize search above used a short/cheap pack to estimate fit quickly;
    # redo the final chosen fsize once with the full iteration budget so the
    # shipped layout is fully converged, not just approximately so
    pos = {nd: ((pos0[nd][0]-cx)*scale, (pos0[nd][1]-cy)*scale) for nd in G}
    pos = _compact_pack(pos, boxes, iters=600, pad=1.05, rounds=14)
    pos = _fold_to_aspect(pos, boxes, target_ratio)
    pos = _compact_pack(pos, boxes, iters=500, pad=1.05, rounds=8)
    x0 = min(pos[nd][0]-boxes[nd][0] for nd in G); x1 = max(pos[nd][0]+boxes[nd][0] for nd in G)
    y0 = min(pos[nd][1]-boxes[nd][2] for nd in G); y1 = max(pos[nd][1]+boxes[nd][1] for nd in G)
    need_w, need_h = (x1-x0), (y1-y0)
    fit = max(need_w/budget_w, need_h/budget_h)

    # numeric self-check against the *drawn* rectangles, not a proxy circle
    nodes = list(pos); viol = 0; worst = 0.0
    for i in range(len(nodes)):
        a = nodes[i]; hwa, topa, bota = boxes[a]; ax, ay = pos[a]
        for j in range(i+1, len(nodes)):
            b = nodes[j]; hwb, topb, botb = boxes[b]; bx, by = pos[b]
            ddx = bx-ax; ddy = by-ay
            ox = (hwa+hwb) - abs(ddx)
            oy = (min(topa, ddy+topb) - max(-bota, ddy-botb))
            if ox > 0 and oy > 0:
                viol += 1; worst = max(worst, min(ox, oy))
    print(f"[fig_page] {name}: landscape={landscape} fsize={fs:.1f} "
          f"needed={need_w:.0f}x{need_h:.0f}pt fit={fit:.2f} "
          f"violations={viol}/{len(nodes)*(len(nodes)-1)//2} worst_overlap={worst:.1f}pt")

    size = (need_w/72/0.92, need_h/72/0.92)
    plt.figure(figsize=size)
    ws = [G[u][v].get("weight", 1) for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, alpha=0.22, width=[0.4+0.6*w for w in ws], edge_color="#8d8d8d")
    nx.draw_networkx_nodes(G, pos, node_color=[col(nd) for nd in G],
                            node_size=[math.pi*radius[nd]**2 for nd in G],
                            alpha=0.95, linewidths=0.6, edgecolors="#54514d")
    lpos = {nd: (pos[nd][0], pos[nd][1] - radius[nd] - 0.5*fs - 4) for nd in G}
    nx.draw_networkx_labels(G, lpos, labels={nd: short(nd) for nd in G}, font_size=fs,
        font_color="#26241f",
        bbox=dict(boxstyle="round,pad=0.22", fc="#fffdf8", ec="#cfc9c0", lw=0.6, alpha=0.95))
    plt.xlim(x0, x1); plt.ylim(y0, y1)
    if legend:
        plt.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=9,label=s)
                            for s, c in COL.items()], loc="upper center", bbox_to_anchor=(0.5, -0.01),
                   ncol=3 if landscape else 2, fontsize=10, frameon=False, handletextpad=0.3, columnspacing=1.4)
    if os.environ.get("FIGTITLES", "1") == "1":
        title_fs = 13 if size[0] >= 7.5 else max(9, 13*size[0]/7.5)
        plt.title(title, fontsize=title_fs, wrap=True)
    plt.axis("off"); plt.tight_layout()
    plt.savefig(f"{outdir or OUT}/{name}.png", dpi=220, facecolor="white"); plt.close()
    return landscape, size


def html(G, name, title, r=None, n2c=None, extra=None):
    net = Network(height="900px", width="100%", bgcolor="#ffffff", font_color="#222",
                  select_menu=True, cdn_resources="remote")
    net.force_atlas_2based(gravity=-60, central_gravity=0.008, spring_length=110, damping=0.55)
    pr = (r or {}).get("pagerank", {}); bt = (r or {}).get("betweenness", {})
    for n, d in G.nodes(data=True):
        info = [n, f"id: {pid(n)}", f"sect: {sect(n)}"]
        p = persons.get(n)
        if p:
            for k, lab in [("roles","roles"),("actions","actions"),("docs","documents"),
                           ("origin_or_nisba_place","origin"),("princeton_name","Princeton match"),
                           ("sect_evidence","sect evidence")]:
                if p.get(k): info.append(f"{lab}: {p[k]}")
            if p.get("year_min"): info.append(f"years: {p['year_min']}-{p['year_max']}")
        if pr: info.append(f"PageRank {pr.get(n,0):.4f} | betweenness {bt.get(n,0):.4f}")
        if n2c: info.append(f"community {n2c.get(n,'-')}")
        if extra and n in extra: info.append(extra[n])
        net.add_node(n, label=short(n), title="\n".join(info),
                     color=d.get("color", col(n)), size=12+(2200*pr.get(n,0) if pr else 2*G.degree(n)))
    for u,v,d in G.edges(data=True):
        t = " | ".join(x for x in [d.get("label",""), f"weight {d.get('weight',1)}", d.get("docs","")] if x)
        net.add_edge(u,v,value=d.get("weight",1),title=t,color=d.get("color","#9a9a9a"))
    net.heading = title
    net.write_html(f"{OUT}/{name}.html", notebook=False)

REPORT = {}

# =============================================================== N1 co-appearance
G1 = nx.Graph()
for e in coapp:
    G1.add_edge(e["source"], e["target"], weight=int(e["weight"]), docs=e["docs"])
r1 = analyze(G1); n1 = write_metrics(G1, r1, "N1_coappearance")
giant1 = G1.subgraph(max(nx.connected_components(G1), key=len)).copy()
rg = analyze(giant1); ng = write_metrics(giant1, rg, "N1_giant")
fig(G1,"fig1_coappearance_full","Figure 1. Co-appearance network, all components\n(node colour = sect, node size = PageRank)",r1,label_n=14)
fig_page(giant1,"fig1_coappearance","Figure 1. Giant component of the co-appearance network (66 persons)\n(node colour = sect, node size = PageRank)",rg,fsize=9.5,min_fsize=5.5)
fig(giant1,"fig1b_communities","Figure 1b. Louvain communities within the giant component",rg,ng,color_by="community",legend=False,label_n=22)
REPORT["N1_giant"] = {k:rg[k] for k in ["n_nodes","n_edges","density","modularity"]}
REPORT["N1_giant"].update(n_communities=len(rg["communities"]), top_betweenness=top(rg["betweenness"]), top_pagerank=top(rg["pagerank"]), top_closeness=top(rg["closeness"]), top_degree=top(rg["degree"]), top_eigen=top(rg["eigenvector"]))
html(G1,"N1_coappearance","N1. Co-appearance network (weighted)",r1,n1)
REPORT["N1"] = {k:r1[k] for k in ["n_nodes","n_edges","n_components","giant","density","modularity","avg_degree"]}
REPORT["N1"].update(n_communities=len(r1["communities"]),
    top_pagerank=top(r1["pagerank"]), top_betweenness=top(r1["betweenness"]),
    top_wdegree=top(r1["wdegree"]), top_eigen=top(r1["eigenvector"]), top_closeness=top(r1["closeness"]))

# =============================================================== N2 bipartite
G2 = nx.Graph()
for a in apps:
    if a["action_en"] in ("DocumentMention","ScholarlyMention","FamilyMention"): continue
    d = a["shelfmark"]
    G2.add_node(d, kind="doc", color="#2e8b57")
    G2.add_node(a["person"], kind="person", color=col(a["person"]))
    if G2.has_edge(a["person"], d):
        G2[a["person"]][d]["weight"] += 1
        G2[a["person"]][d]["label"] += ", " + a["action_en"]
    else:
        G2.add_edge(a["person"], d, weight=1, label=a["action_en"])
r2 = analyze(G2); n2 = write_metrics(G2, r2, "N2_bipartite")
docdeg = {n:G2.degree(n) for n,d in G2.nodes(data=True) if d.get("kind")=="doc"}
perdeg = {n:G2.degree(n) for n,d in G2.nodes(data=True) if d.get("kind")=="person"}
fig(G2,"fig2_bipartite","Figure 2. Bipartite person–document network (green = documents)",r2,legend=False)
html(G2,"N2_bipartite","N2. Bipartite person–document network",r2,n2,
     extra={d:f"DOCUMENT — {docs[d]['doc_type']}, {docs[d]['date_text']}, {docs[d]['place']}" for d in docs if d in G2})
REPORT["N2"] = {k:r2[k] for k in ["n_nodes","n_edges","n_components","giant"]}
REPORT["N2"].update(top_documents=top(docdeg), top_persons=top(perdeg), top_betweenness=top(r2["betweenness"]))

# =============================================================== N3 kinship / agency
RC = {"married":"#c0392b","betrothed":"#e67e22","divorced":"#7f5539","father_of":"#2471a3",
      "mother_of":"#17a2b8","sibling_of":"#27ae60","first_cousin_of":"#7dcea0","uncle_of":"#8e44ad",
      "agent_for":"#c2408f","ancestor_of":"#5d6d7e","son_in_law_of":"#d35400"}
KIN = {"married","betrothed","divorced","first_husband_of","father_of","mother_of","sibling_of",
       "first_cousin_of","uncle_of","ancestor_of","son_in_law_of","agent_for","gave_gift_to"}
G3 = nx.Graph()
for r in rels:
    if r["relation"] not in KIN: continue
    G3.add_edge(r["source"], r["target"], weight=2 if r["relation"] in ("married","betrothed") else 1,
                label=r["relation"], color=RC.get(r["relation"],"#aaa"), docs=r["evidence"])
r3 = analyze(G3); n3 = write_metrics(G3, r3, "N3_kinship")
fig(G3,"fig3_kinship","Figure 3. Kinship, marriage and agency network",r3,size=(18,13),label_n=18)
html(G3,"N3_kinship","N3. Kinship, marriage and agency (edge colour = relation type)",r3,n3)
comp3 = sorted(nx.connected_components(G3), key=len, reverse=True)
REPORT["N3"] = {k:r3[k] for k in ["n_nodes","n_edges","n_components","giant"]}
REPORT["N3"].update(component_sizes=[len(c) for c in comp3[:8]],
    largest_component=sorted(comp3[0])[:12] if comp3 else [],
    top_betweenness=top(r3["betweenness"]), top_degree=top(r3["degree"]))

# =============================================================== N4 cross-sect
G4 = nx.Graph()
for e in coapp:
    a,b = e["source"], e["target"]
    if "R" in (group(a), group(b)):
        G4.add_edge(a,b,weight=int(e["weight"]),docs=e["docs"])
for r in rels:
    if group(r["source"])=="R" or group(r["target"])=="R":
        if not G4.has_edge(r["source"], r["target"]):
            G4.add_edge(r["source"], r["target"], weight=1, label=r["relation"], docs=r["evidence"])
r4 = analyze(G4); n4 = write_metrics(G4, r4, "N4_cross_sect")
fig(G4,"fig4_cross_sect","Figure 4. Karaite–Rabbanite contact network\n(red = Rabbanite, blue = Karaite, grey = unknown)",r4,size=(18,12.5),label_n=18)
html(G4,"N4_cross_sect","N4. Karaite–Rabbanite contact network",r4,n4)
kr = [(u,v) for u,v in G4.edges() if {group(u),group(v)} == {"K","R"}]
docs_R = sorted({a["shelfmark"] for a in apps if group(a["person"])=="R"})
REPORT["N4"] = {k:r4[k] for k in ["n_nodes","n_edges","n_components"]}
REPORT["N4"].update(direct_KR_edges=len(kr), docs_with_rabbanites=docs_R,
    n_docs_with_rabbanites=len(docs_R), rabbanites=sorted({p for p in persons if group(p)=="R"}),
    top_betweenness=top(r4["betweenness"]), top_pagerank=top(r4["pagerank"]), top_closeness=top(r4["closeness"]))

# =============================================================== N5 attestation professionals
ATT = {"Witness","WitnessOfAgency","Scribe","Declarant"}
dw = defaultdict(set)
for a in apps:
    if a["action_en"] in ATT and a["certainty"] != "contextual":
        dw[a["shelfmark"]].add(a["person"])
pair = defaultdict(set)
for d, pp in dw.items():
    pp = sorted(pp)
    for i in range(len(pp)):
        for j in range(i+1, len(pp)): pair[(pp[i],pp[j])].add(d)
G5 = nx.Graph()
for (a,b), ds in pair.items(): G5.add_edge(a,b,weight=len(ds),docs="; ".join(sorted(ds)))
r5 = analyze(G5); n5 = write_metrics(G5, r5, "N5_attestation")
fig(G5,"fig5_attestation","Figure 5. Witness, scribe and declarant co-signature network",r5,size=(18,12.5),label_n=14)
html(G5,"N5_attestation","N5. Attestation network (witnesses, witnesses of agency, scribes)",r5,n5)
REPORT["N5"] = {k:r5[k] for k in ["n_nodes","n_edges","n_components","giant","modularity"]}
REPORT["N5"].update(n_communities=len(r5["communities"]), top_betweenness=top(r5["betweenness"]),
                    top_pagerank=top(r5["pagerank"]), top_wdegree=top(r5["wdegree"]), top_closeness=top(r5["closeness"]))


# =============================================================== N6 ketubbot only
KET = {d for d,v in docs.items() if "ketubba" in v["doc_type"] and "formular" not in v["doc_type"]
       and "book of" not in v["doc_type"]}
BET = {d for d,v in docs.items() if "betrothal" in v["doc_type"] and "formular" not in v["doc_type"]
       and "book of" not in v["doc_type"]}
def subnet(doclist, name):
    dp = defaultdict(set)
    for a in apps:
        if a["shelfmark"] in doclist and a["action_en"] not in ("DocumentMention","ScholarlyMention"):
            dp[a["shelfmark"]].add(a["person"])
    pr_ = defaultdict(set)
    for d, pp in dp.items():
        pp = sorted(pp)
        for i in range(len(pp)):
            for j in range(i+1, len(pp)): pr_[(pp[i],pp[j])].add(d)
    G = nx.Graph()
    for (a,b), ds in pr_.items(): G.add_edge(a,b,weight=len(ds),docs="; ".join(sorted(ds)))
    return G, len(dp)

G6, n6docs = subnet(KET, "ketubbot")
r6 = analyze(G6); c6 = write_metrics(G6, r6, "N6_ketubbot")
fig(G6,"fig6_ketubbot","Ketubbot only",r6,size=(18,12.5),label_n=14)
html(G6,"N6_ketubbot","N6. Ketubbot only (Karaite marriage contracts)",r6,c6)
G6b, n6bdocs = subnet(BET, "betrothals")
r6b = analyze(G6b)
REPORT["N6_ketubbot"] = {k:r6[k] for k in ["n_nodes","n_edges","n_components","giant","density","modularity"]}
REPORT["N6_ketubbot"].update(n_documents=n6docs, n_communities=len(r6["communities"]),
    top_pagerank=top(r6["pagerank"]), top_betweenness=top(r6["betweenness"]),
    top_closeness=top(r6["closeness"]), top_degree=top(r6["degree"]))
REPORT["N6_betrothals"] = {k:r6b[k] for k in ["n_nodes","n_edges","n_components","giant","density"]}
REPORT["N6_betrothals"].update(n_documents=n6bdocs, top_betweenness=top(r6b["betweenness"]))

# per-document participant profile for ketubbot vs betrothals
def profile(doclist):
    c = Counter()
    for a in apps:
        if a["shelfmark"] in doclist: c[a["action_en"]] += 1
    return dict(c.most_common())
REPORT["profile_ketubbot"] = profile(KET)
REPORT["profile_betrothal"] = profile(BET)

# =============================================================== courts and adjudication
COURT_ACT = {"Judge","Trustee","Declarant","NamedNasi"}
court_docs = sorted({a["shelfmark"] for a in apps if a["action_en"] in COURT_ACT})
court_people = defaultdict(set)
for a in apps:
    if a["action_en"] in COURT_ACT: court_people[a["action_en"]].add(a["person"])
# documents that record a court act in their type or notes
court_type_docs = sorted({d for d,v in docs.items()
    if "court" in v["doc_type"].lower() or "attorney" in v["doc_type"].lower()
    or "court" in v["notes"].lower() or "certif" in v["notes"].lower()})
REPORT["courts"] = {
  "docs_with_court_actions": court_docs,
  "n_docs_with_court_actions": len(court_docs),
  "docs_of_court_type_or_note": court_type_docs,
  "n_docs_court_type_or_note": len(court_type_docs),
  "judges": sorted(court_people["Judge"]),
  "nesiim_named": sorted(court_people["NamedNasi"]),
  "trustees": sorted(court_people["Trustee"]),
  "declarants": sorted(court_people["Declarant"]),
}
# how central are court-act persons in N1?
court_persons = set().union(*court_people.values()) if court_people else set()
in_n1 = [p for p in court_persons if p in G1]
if in_n1:
    import statistics as st
    others = [n for n in G1 if n not in court_persons]
    REPORT["courts"]["mean_betweenness_court_persons"] = round(st.mean(r1["betweenness"][p] for p in in_n1),5)
    REPORT["courts"]["mean_betweenness_others"] = round(st.mean(r1["betweenness"][p] for p in others),5)
    REPORT["courts"]["mean_pagerank_court_persons"] = round(st.mean(r1["pagerank"][p] for p in in_n1),5)
    REPORT["courts"]["mean_pagerank_others"] = round(st.mean(r1["pagerank"][p] for p in others),5)


# =============================================================== alternative weighting schemes
# Scheme A (used throughout): weight = number of shared documents.
# Scheme B (Newman): a tie made inside a document with k participants is worth 1/(k-1),
#   so a signature in a crowded court copy counts for less than one in a small deed.
# Scheme C: binary, weight = 1 for any co-appearance.
doc_size = {d: len(pp) for d, pp in doc_people.items()} if "doc_people" in dir() else {}
dp2 = defaultdict(set)
for a in apps:
    if a["action_en"] not in ("DocumentMention","ScholarlyMention") and a["certainty"]!="contextual":
        dp2[a["shelfmark"]].add(a["person"])
GA, GB, GC = nx.Graph(), nx.Graph(), nx.Graph()
wB = defaultdict(float); wA = defaultdict(int)
for d, pp in dp2.items():
    pp = sorted(pp); k = len(pp)
    for i in range(k):
        for j in range(i+1, k):
            wA[(pp[i],pp[j])] += 1
            wB[(pp[i],pp[j])] += 1.0/max(k-1,1)
for (a,b),w in wA.items(): GA.add_edge(a,b,weight=w); GC.add_edge(a,b,weight=1)
for (a,b),w in wB.items(): GB.add_edge(a,b,weight=round(w,4))
rA, rB, rC = analyze(GA), analyze(GB), analyze(GC)
write_metrics(GB, rB, "N1_newman_weighting")
def rank(d, n=10): return [x for x,_ in top(d,n)]
REPORT["weighting"] = {
  "scheme_A_shared_documents": {"top_betweenness":top(rA["betweenness"],8), "top_pagerank":top(rA["pagerank"],8)},
  "scheme_B_newman_1_over_k": {"top_betweenness":top(rB["betweenness"],8), "top_pagerank":top(rB["pagerank"],8)},
  "scheme_C_binary": {"top_betweenness":top(rC["betweenness"],8), "top_pagerank":top(rC["pagerank"],8)},
  "overlap_top10_betweenness_A_vs_B": len(set(rank(rA["betweenness"])) & set(rank(rB["betweenness"]))),
  "overlap_top10_pagerank_A_vs_B": len(set(rank(rA["pagerank"])) & set(rank(rB["pagerank"]))),
  "overlap_top10_betweenness_A_vs_C": len(set(rank(rA["betweenness"])) & set(rank(rC["betweenness"]))),
}

# =============================================================== N7 document-document network
# two documents are linked if they share at least one person; weight = number of shared persons
person_docs = defaultdict(set)
for a in apps:
    if a["action_en"] not in ("DocumentMention","ScholarlyMention") and a["certainty"]!="contextual":
        person_docs[a["person"]].add(a["shelfmark"])
dd = defaultdict(set)
for p, ds in person_docs.items():
    ds = sorted(ds)
    for i in range(len(ds)):
        for j in range(i+1, len(ds)): dd[(ds[i],ds[j])].add(p)
G7 = nx.Graph()
for (a,b), ps in dd.items(): G7.add_edge(a,b,weight=len(ps),docs="; ".join(sorted(ps)))
if G7.number_of_nodes():
    r7 = analyze(G7)
    with open(f"{OUT}/N7_document_network.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["doc_a","doc_b","shared_persons","persons"])
        for (a,b),ps in sorted(dd.items(), key=lambda x:-len(x[1])):
            w.writerow([a,b,len(ps),"; ".join(sorted(ps))])
    html(G7,"N7_document_network","N7. Document network (documents linked by shared persons)",r7)
    REPORT["N7_documents"] = {k:r7[k] for k in ["n_nodes","n_edges","n_components","giant","density"]}
    REPORT["N7_documents"].update(
      top_betweenness=top(r7["betweenness"],8), top_degree=top(r7["degree"],8),
      strongest_links=[[a,b,len(ps)] for (a,b),ps in sorted(dd.items(), key=lambda x:-len(x[1]))[:6]])


# =============================================================== robustness: without the nasi clause
# The nasi is named in a fixed opening clause, not as a participant who acted.
# This test rebuilds the network without those appearances to see whether the
# judicial finding survives.
import statistics as _st
def _build(exclude=()):
    dp = defaultdict(set)
    for a in apps:
        if a["action_en"] in ("DocumentMention","ScholarlyMention","FamilyMention"): continue
        if a["action_en"] in exclude: continue
        if a["certainty"]=="contextual": continue
        dp[a["shelfmark"]].add(a["person"])
    pr_ = defaultdict(set)
    for d, pp in dp.items():
        pp = sorted(pp)
        for i in range(len(pp)):
            for j in range(i+1,len(pp)): pr_[(pp[i],pp[j])].add(d)
    G = nx.Graph()
    for (a,b),ds in pr_.items(): G.add_edge(a,b,weight=len(ds))
    return G
COURT_ALL = {a["person"] for a in apps if a["action_en"] in ("Judge","Trustee","Declarant","NamedNasi")}
COURT_ACTED = {a["person"] for a in apps if a["action_en"] in ("Judge","Trustee","Declarant")}
def _probe(G, label):
    for u,v,d in G.edges(data=True): d["dist"]=1/max(d["weight"],1)
    bt = nx.betweenness_centrality(G, weight="dist", normalized=True)
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    inA=[p for p in COURT_ALL if p in G]; others=[n for n in G if n not in COURT_ALL]
    out = {"nodes":G.number_of_nodes(), "giant":len(comps[0]), "components":len(comps),
           "top_betweenness":top(bt,6)}
    if inA: out["mean_betweenness_court_roles"]=round(_st.mean(bt[p] for p in inA),5)
    if others: out["mean_betweenness_others"]=round(_st.mean(bt[p] for p in others),5)
    if inA and others:
        out["ratio"]=round(out["mean_betweenness_court_roles"]/max(out["mean_betweenness_others"],1e-9),2)
    g = G.subgraph(comps[0]).copy()
    for u,v,d in g.edges(data=True): d["dist"]=1/max(d["weight"],1)
    out["giant_top_betweenness"]=top(nx.betweenness_centrality(g,weight="dist",normalized=True),5)
    return out
REPORT["robustness_nasi_clause"] = {
  "with_nasi_clause": _probe(_build(), "with"),
  "without_nasi_clause": _probe(_build(exclude=("NamedNasi",)), "without"),
}


# =============================================================== readable close-ups for the paper
# Figure 4 was unreadable because eleven separate clusters overlapped.
# Draw only the components that actually contain a Karaite-Rabbanite tie.
def _kr_components(G):
    keep = set()
    for comp in nx.connected_components(G):
        sub = G.subgraph(comp)
        if any({group(u),group(v)}=={"K","R"} for u,v in sub.edges()):
            keep |= comp
    return G.subgraph(keep).copy()
G4c = _kr_components(G4)
if G4c.number_of_nodes():
    r4c = analyze(G4c)
    fig(G4c,"fig4_cross_sect_closeup",
        "Figure 4. Karaite-Rabbanite contact, components containing a cross-sect tie",
        r4c, size=(10.8,7.6), label_n=22, layout="grid", fsize=11,
        must=["Eli b. Amram (he-haver)","Solomon b. Jehuda (Gaon)","Nathan b. Abraham (Gaon)","Josiah b. Solomon (nasi)"])
    REPORT["N4_closeup"] = {"n_nodes":G4c.number_of_nodes(), "n_edges":G4c.number_of_edges(),
                            "n_components":nx.number_connected_components(G4c)}

# Figure 5: close-up on the three components around the recurring signatories
KEY = ["Bishr b. Abraham ha-Levi", "Eli b. Mu'ammar", "David b. Isaac ha-Kohen (the scribe)"]
keep = set()
for k in KEY:
    if k in G5:
        keep |= nx.node_connected_component(G5, k)
G5c = G5.subgraph(keep).copy()
if G5c.number_of_nodes():
    r5c = analyze(G5c)
    fig_page(G5c,"fig5_attestation_closeup",
        "Figure 5. Close-up: the components around the three recurring signatories",
        r5c, fsize=10)
    REPORT["N5_closeup"] = {"n_nodes":G5c.number_of_nodes(), "n_edges":G5c.number_of_edges(),
                            "n_components":nx.number_connected_components(G5c),
                            "share_of_network":round(G5c.number_of_nodes()/G5.number_of_nodes(),2)}

# Figure 2 in the paper: the ketubbot network is too fragmented to draw whole,
# so the paper shows a close-up of its giant component with every person named.
_g6c = G6.subgraph(max(nx.connected_components(G6), key=len)).copy()
r6c = analyze(_g6c)
fig_page(_g6c,"fig6_ketubbot_closeup",
    "Figure 2. Close-up: the giant component of the ketubbot network",
    r6c, fsize=9.5)
REPORT["N6_closeup"] = {"n_nodes":_g6c.number_of_nodes(), "n_edges":_g6c.number_of_edges(),
                        "share_of_network":round(_g6c.number_of_nodes()/G6.number_of_nodes(),2),
                        "n_documents":len({d for _,_,dd in _g6c.edges(data=True) for d in dd["docs"].split("; ")})}

# Figure 3 in the paper: 45 family components cannot be read at page size,
# so the paper shows a close-up of the largest one, the nesi'im x Tustari merger.
_g3c = G3.subgraph(max(nx.connected_components(G3), key=len)).copy()
r3c = analyze(_g3c)
fig(_g3c,"fig3_kinship_closeup",
    "Figure 3. Close-up: the largest family component (nesi'im x Tustari)",
    r3c, size=(10.5,9.0), label_n=_g3c.number_of_nodes(), layout="kk", fsize=10,
    must=["Yefet b. Abraham al-Tustari","Ama al-Aziz bt. Hizkiyahu","Hizkiyahu b. Solomon (nasi)",
          "Sahl (Yashar) b. Israel al-Tustari","Anan b. David"])
REPORT["N3_closeup"] = {"n_nodes":_g3c.number_of_nodes(), "n_edges":_g3c.number_of_edges()}

# =============================================================== do communities follow document type?
_giant = G1.subgraph(max(nx.connected_components(G1), key=len)).copy()
_comms = nx.community.louvain_communities(_giant, weight="weight", seed=42)
_pdocs = defaultdict(set)
for a in apps:
    if a["certainty"]!="contextual": _pdocs[a["person"]].add(a["shelfmark"])
_out=[]
for i,c in enumerate(_comms):
    ds=set()
    for p in c: ds |= _pdocs[p]
    _out.append({"community":i,"people":len(c),"documents":len(ds),
                 "types":dict(Counter(docs[d]["doc_type"].split(" (")[0] for d in ds if d in docs)),
                 "places":dict(Counter(docs[d]["place"] for d in ds if d in docs))})
REPORT["communities_vs_document_type"] = _out

# =============================================================== formal role of the top brokers
_ROLES = defaultdict(set)
for a in apps: _ROLES[a["person"]].add(a["action_en"])
Gnn = _build(exclude=("NamedNasi",))
for u,v,d in Gnn.edges(data=True): d["dist"]=1/max(d["weight"],1)
_bt = nx.betweenness_centrality(Gnn, weight="dist", normalized=True)
REPORT["top_brokers_roles"] = [
  {"person":n, "betweenness":round(v,4), "roles":sorted(_ROLES[n])}
  for n,v in sorted(_bt.items(), key=lambda x:-x[1])[:6]]

# =============================================================== corpus descriptives
REPORT["corpus"] = {
 "documents": len(docs), "persons": len(persons), "appearances": len(apps), "relations": len(rels),
 "action_distribution": dict(Counter(a["action_en"] for a in apps).most_common()),
 "sect_distribution": dict(Counter(p["sect"] for p in persons.values())),
 "place_distribution": dict(Counter(d["place"] for d in docs.values()).most_common()),
 "gender": dict(Counter(p["gender"] for p in persons.values())),
 "doc_type_distribution": dict(Counter(d["doc_type"] for d in docs.values()).most_common()),
}

# =============================================================== full size plates
# The paper prints close-ups, because a page cannot carry a whole fragmented
# network legibly. The complete networks are written here at plate size, every
# node named, for readers who want to zoom in. See networks/full/README.md.
FULL = f"{OUT}/full"
os.makedirs(FULL, exist_ok=True)
_plates = [
    (G1,      "N1_coappearance_all", r1,  "grid", "Plate 1. Co-appearance network, all 275 persons, every component"),
    (giant1,  "N1_giant",            rg,  "kk",   "Plate 2. Giant component of the co-appearance network, 66 persons"),
    (G2,      "N2_person_document",  r2,  "grid", "Plate 3. Bipartite network of persons and documents"),
    (G3,      "N3_kinship",          r3,  "grid", "Plate 4. Kinship, marriage and agency, all 45 family components"),
    (G4,      "N4_cross_sect",       r4,  "grid", "Plate 5. Karaite-Rabbanite contact, all components"),
    (G5,      "N5_attestation",      r5,  "grid", "Plate 6. Witnesses and scribes, all components"),
    (G6,      "N6_ketubbot",         r6,  "grid", "Plate 7. Ketubbot only, all components"),
    (G6b,     "N6_betrothals",       r6b, "grid", "Plate 8. Deeds of betrothal only, all components"),
]
if G7.number_of_nodes():
    _plates.append((G7, "N7_document_network", r7, "kk", "Plate 9. Documents joined by shared persons"))
for _g, _nm, _rr, _lay, _ttl in _plates:
    fig(_g, _nm, _ttl, _rr, size=(30, 21), fsize=13, label_n=_g.number_of_nodes(),
        layout=_lay, outdir=FULL, nmin=70, nspan=1500)
print("plates written to", FULL)

json.dump(REPORT, open(f"{OUT}/analysis_v2.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

for k in ["N1","N1_giant","N2","N3","N4","N5","N6_ketubbot"]:
    print(k, {x:REPORT[k][x] for x in REPORT[k] if not isinstance(REPORT[k][x], list)})
print("corpus:", REPORT["corpus"]["action_distribution"])
