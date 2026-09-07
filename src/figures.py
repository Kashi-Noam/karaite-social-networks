# -*- coding: utf-8 -*-
"""
figures.py — every figure printed in the paper, from dataset/ and paper_numbers.json.

    cd src && python3 backbone.py && python3 figures.py

One visual system throughout: a warm off-white surface, thin recessive marks,
a single categorical ramp, labels only where a name carries an argument, and
no chart furniture that does not earn its place. Captions live in the paper,
not in the image, so nothing here is set in Hebrew.
"""
import csv, json, math, os, itertools, random
from collections import defaultdict, Counter

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(HERE, "..", "dataset")
FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8f8d87"
GRID = "#e6e4de"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
VIOLET = "#4a3aa7"
GREY = "#b8b3ad"
EDGE = "#c9c6bf"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10.5,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#cfccc5", "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "axes.titlelocation": "left", "axes.titlecolor": INK,
    "axes.titlesize": 11.5, "axes.titlepad": 12,
})


def read(n):
    with open(os.path.join(DS, n), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


docs = {d["shelfmark"]: d for d in read("documents.csv")}
persons = {p["canonical_name"]: p for p in read("persons.csv")}
apps = read("appearances.csv")
rels = read("relations.csv")
actions = {a["action_en"]: a for a in read("actions.csv")}
NUM = json.load(open(os.path.join(HERE, "..", "networks", "paper_numbers.json"),
                     encoding="utf-8"))

PRESENCE = [a for a in apps if actions[a["action_en"]]["action_class"] != "Reference"]
PRESENCE_NASI = [a for a in apps
                 if actions[a["action_en"]]["action_class"] != "Reference"
                 or a["action_en"] == "NamedNasi"]
REGION = {"Fustat": "Egypt", "Cairo": "Egypt", "Egypt (region)": "Egypt",
          "Jerusalem": "Palestine", "Ramle": "Palestine", "Tyre": "Palestine",
          "Palestine (region)": "Palestine"}


def cast(rows):
    dp = defaultdict(set)
    for a in rows:
        dp[a["shelfmark"]].add(a["person"])
    return dp


def graph(rows):
    dp = cast(rows)
    G = nx.Graph()
    for doc, pp in dp.items():
        for u, v in itertools.combinations(sorted(pp), 2):
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
                G[u][v]["docs"].append(doc)
            else:
                G.add_edge(u, v, weight=1, docs=[doc])
    G.add_nodes_from({a["person"] for a in rows})
    return G, dp


G, DP = graph(PRESENCE)
GN, DPN = graph(PRESENCE_NASI)


def between(Gx):
    H = Gx.copy()
    for u, v, d in H.edges(data=True):
        d["dist"] = 1.0 / max(d.get("weight", 1), 1)
    return nx.betweenness_centrality(H, weight="dist", normalized=True)


def short(n):
    n = (n.replace(" ha-Kohen", "").replace(" ha-Levi", "")
          .replace(" (the scribe)", " (scribe)").replace(" (nasi)", " (nasi)")
          .replace(" b. ", " b. "))
    return n if len(n) <= 30 else n[:29] + "…"


def save(fig, name, pad=0.16):
    fig.savefig(os.path.join(FIG, name), dpi=260, bbox_inches="tight",
                pad_inches=pad, facecolor=SURFACE)
    plt.close(fig)
    print("  ", name)


def halo(txt):
    txt.set_path_effects([pe.withStroke(linewidth=2.6, foreground=SURFACE)])


def place_labels(ax, pos, names, fs=8.4, dy=0.0):
    """Draw labels, dropping any that would collide with one already drawn."""
    ax.figure.canvas.draw()
    placed = []
    out = []
    for n in names:
        x, y = pos[n]
        t = ax.text(x, y + dy, short(n), fontsize=fs, color=INK, ha="center",
                    va="center", zorder=6)
        halo(t)
        bb = t.get_window_extent(ax.figure.canvas.get_renderer()).expanded(1.06, 1.25)
        if any(bb.overlaps(b) for b in placed):
            t.remove()
        else:
            placed.append(bb)
            out.append(n)
    return out


# ============================================================ 1. the clique
def fig_clique():
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.5))
    cases = [(4, "TS 20.47r", "a ketubba with 4 named"),
             (8, "TS 12.644", "a deed of betrothal with 8"),
             (17, "Bodl. MS Heb. a.3.4v", "a court copy with 17")]
    for ax, (k, sm, lab) in zip(axes, cases):
        Gk = nx.complete_graph(k)
        pos = {i: (math.cos(2 * math.pi * i / k + math.pi / 2),
                   math.sin(2 * math.pi * i / k + math.pi / 2)) for i in range(k)}
        nx.draw_networkx_edges(Gk, pos, ax=ax, edge_color=BLUE, alpha=0.22, width=0.9)
        nx.draw_networkx_nodes(Gk, pos, ax=ax, node_size=78, node_color=BLUE,
                               edgecolors=SURFACE, linewidths=1.4)
        e = k * (k - 1) // 2
        ax.set_title(f"{lab}\n{e} ties", fontsize=10.5, color=INK, pad=8, loc="center")
        ax.text(0, -1.62, sm, ha="center", fontsize=8.2, color=MUTED)
        ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.8, 1.35)
        ax.axis("off")
    save(fig, "fig_clique.png")


# ======================================================= 2. the backbone
def fig_backbone():
    """An arc diagram: documents on a time axis, an arc where a person signs both.

    A force layout would waste the one variable that matters here, the date, so
    the documents sit on their own years, the labels alternate above the line,
    and every shared signatory hangs below it as an arc.
    """
    pdocs = defaultdict(set)
    for a in PRESENCE:
        pdocs[a["person"]].add(a["shelfmark"])
    link = defaultdict(set)
    for p, ds in pdocs.items():
        for x, y in itertools.combinations(sorted(ds), 2):
            link[(x, y)].add(p)
    linked = sorted({d for pair in link for d in pair},
                    key=lambda s: float(docs[s]["year_est"] or 0))
    X = {sm: float(docs[sm]["year_est"]) for sm in linked}

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.axhline(0, color="#d9d6cf", lw=1.0, zorder=1)

    # arcs below the line; the wider the span, the deeper the arc
    for (x, y), pp in sorted(link.items(), key=lambda kv: -len(kv[1])):
        x1, x2 = sorted((X[x], X[y]))
        span = max(x2 - x1, 1.2)
        depth = -(0.30 + 0.052 * span)
        ts = np.linspace(0, 1, 80)
        bx = (1 - ts) ** 2 * x1 + 2 * (1 - ts) * ts * (x1 + x2) / 2 + ts ** 2 * x2
        by = 2 * (1 - ts) * ts * (2 * depth)
        many = len(pp) > 1
        ax.plot(bx, by, color=ORANGE if many else "#a3a099",
                lw=2.0 if many else 1.0, alpha=0.9 if many else 0.75,
                zorder=3 if many else 2, solid_capstyle="round")
        if many:
            t = ax.text((x1 + x2) / 2, depth - 0.10, f"{len(pp)} shared",
                        fontsize=7.8, color=ORANGE, ha="center", va="top",
                        fontweight="bold")
            halo(t)

    cols = {"Palestine": ORANGE, "Egypt": BLUE, "Unknown": GREY}
    for sm in linked:
        reg = REGION.get(docs[sm]["place"], "Unknown")
        ax.scatter(X[sm], 0, s=130, color=cols[reg], edgecolor=SURFACE,
                   lw=1.8, zorder=5)
    # labels: lowest free shelf, measuring each label's real width in years
    CHAR = 0.60          # one character at 7.6pt, in years of the x axis
    shelves = []
    for sm in sorted(linked, key=lambda s: X[s]):
        lab = sm.split(" + ")[0]
        half = len(lab) * CHAR / 2 + 0.7
        for k, right in enumerate(shelves):
            if X[sm] - half > right:
                shelves[k] = X[sm] + half; lvl = k; break
        else:
            shelves.append(X[sm] + half); lvl = len(shelves) - 1
        y = 0.19 + 0.235 * lvl
        ax.plot([X[sm], X[sm]], [0.07, y - 0.035], color="#cdcac3", lw=0.7, zorder=2)
        t = ax.text(X[sm], y, lab, fontsize=7.6, ha="center", va="bottom",
                    color=INK, zorder=6)
        halo(t)

    ax.axvspan(999, 1029, color=ORANGE, alpha=0.05, zorder=0)
    ax.axvspan(1029, 1068, color=BLUE, alpha=0.05, zorder=0)
    t = ax.text(1014, 1.72, "Palestine  1002–1028", fontsize=9.6, color=ORANGE,
                ha="center", fontweight="bold"); halo(t)
    t = ax.text(1048, 1.72, "Egypt  1030–1064", fontsize=9.6, color=BLUE,
                ha="center", fontweight="bold"); halo(t)
    ax.annotate("the same couple, betrothal and ketubba",
                xy=(1063.4, -0.36), xytext=(1050, -2.30), fontsize=8.2,
                color=INK2, ha="center", zorder=7,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8,
                                connectionstyle="arc3,rad=0.2"))
    ax.set_xlim(997, 1071); ax.set_ylim(-2.65, 2.00)
    ax.set_yticks([])
    ax.set_xticks([1000, 1010, 1020, 1030, 1040, 1050, 1060])
    ax.set_xlabel("year the document was written")
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=6)
    save(fig, "fig_backbone.png")


# ================================================= 3. how big was the pool
def fig_pool():
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    for key, col, lab in [("whole_corpus", BLUE, "whole corpus, 38 documents"),
                          ("fustat_1030_1074", ORANGE, "Fustat 1030–1074, 18 documents")]:
        d = NUM["pool"][key]
        xs = [c["N"] for c in d["curve"]]
        ys = [c["expected_repeaters"] for c in d["curve"]]
        ax.plot(xs, ys, color=col, lw=2.0, zorder=3, solid_capstyle="round")
        ax.axhline(d["observed_repeaters"], color=col, lw=0.9, ls=(0, (4, 3)), alpha=0.65)
        est = d["estimate"]
        ax.scatter([est], [d["observed_repeaters"]], s=64, color=col,
                   edgecolor=SURFACE, lw=1.8, zorder=5)
        t = ax.text(est, d["observed_repeaters"] + 2.4, f"≈{est:,}", fontsize=9.5,
                    color=col, ha="center", fontweight="bold")
        halo(t)
        t = ax.text(xs[0] * 1.05, ys[0] + 2.2, lab, fontsize=9, color=col,
                    ha="left", fontweight="bold")
        halo(t)
        t = ax.text(7600, d["observed_repeaters"] + 1.3,
                    f"observed: {d['observed_repeaters']}", fontsize=8.4, color=col,
                    ha="right")
        halo(t)
    ax.set_xscale("log")
    ax.set_xlabel("size of the pool of adult men a document could draw its cast from")
    ax.set_ylabel("people expected in more than one document")
    ax.set_ylim(0, 78)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xticks([100, 300, 1000, 3000, 8000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    save(fig, "fig_pool_size.png")


# ==================================== 4. the component that co-presence holds
def core_periphery(Gx, ax, highlight, title=None, seed=7):
    comps = sorted(nx.connected_components(Gx), key=len, reverse=True)
    gi = Gx.subgraph(comps[0]).copy()
    bt = between(gi)
    mx = max(bt.values()) or 1
    ring = {n: 1.0 - 0.78 * (bt[n] / mx) ** 0.55 for n in gi}
    comm = nx.community.louvain_communities(gi, weight="weight", seed=42)
    n2c = {n: i for i, c in enumerate(comm) for n in c}
    k = len(comm)
    order = sorted(gi, key=lambda n: (n2c[n], -bt[n]))
    ang = {}
    bycom = defaultdict(list)
    for n in order:
        bycom[n2c[n]].append(n)
    a0 = 0.0
    for ci in sorted(bycom):
        mem = bycom[ci]
        span = 2 * math.pi * len(mem) / len(order)
        for j, n in enumerate(mem):
            ang[n] = a0 + span * (j + 0.5) / len(mem)
        a0 += span
    pos = {n: (ring[n] * math.cos(ang[n]), ring[n] * math.sin(ang[n])) for n in gi}
    # pull the brokers to the middle so the eye reads distance-from-centre
    for u, v in gi.edges():
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=EDGE, lw=0.55, alpha=0.55, zorder=1, solid_capstyle="round")
    pal = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, VIOLET, "#7d8f9b"]
    for n in gi:
        big = n in highlight
        ax.scatter(*pos[n], s=210 if big else 42,
                   color=pal[n2c[n] % len(pal)], edgecolor=SURFACE,
                   lw=1.9 if big else 1.0, zorder=4 if big else 3)
    place_labels(ax, pos, highlight, fs=8.6, dy=-0.115)
    ax.add_artist(plt.Circle((0, 0), 1.0, fill=False, color=GRID, lw=0.9, zorder=0))
    ax.set_xlim(-1.28, 1.28); ax.set_ylim(-1.24, 1.24)
    ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10.5, color=INK, loc="center", pad=6)
    return gi


def fig_core_periphery():
    cuts = NUM["networks"]["presence"]["cut_vertices_giant"]
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    gi = core_periphery(G, ax, cuts)
    save(fig, "fig_core_periphery.png")


# ============================== 5. what the formulaic nasi clause does (new)
def fig_nasi():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.3))
    core_periphery(G, axes[0], NUM["networks"]["presence"]["cut_vertices_giant"],
                   title="people who stood together\nlargest component: %d"
                         % NUM["networks"]["presence"]["giant"])
    core_periphery(GN, axes[1], NUM["networks"]["presence_plus_nasi"]["cut_vertices_giant"],
                   title="the same, with the nasi of the dating clause added\nlargest component: %d"
                         % NUM["networks"]["presence_plus_nasi"]["giant"])
    save(fig, "fig_nasi.png")


# =========================================================== 6. the family
def fig_kinship():
    KIN = {"married", "betrothed", "divorced", "first_husband_of", "father_of",
           "mother_of", "sibling_of", "first_cousin_of", "uncle_of",
           "ancestor_of", "son_in_law_of", "agent_for"}
    K = nx.Graph()
    for r in rels:
        if r["relation"] in KIN:
            K.add_edge(r["source"], r["target"], rel=r["relation"])
    big = K.subgraph(max(nx.connected_components(K), key=len)).copy()
    bt = between(big)
    gen = {n: persons.get(n, {}).get("gender", "M") for n in big}
    fig, ax = plt.subplots(figsize=(8.0, 6.2))
    pos = nx.kamada_kawai_layout(big)
    MARR = {"married", "betrothed", "divorced", "first_husband_of"}
    for u, v, d in big.edges(data=True):
        marr = d["rel"] in MARR
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=ORANGE if marr else "#a8a49c", lw=1.7 if marr else 0.9,
                alpha=0.85 if marr else 0.6, zorder=1, solid_capstyle="round")
    mx = max(bt.values()) or 1
    for n in big:
        ax.scatter(*pos[n], s=46 + 340 * bt[n] / mx,
                   color=MAGENTA if gen[n] == "F" else BLUE,
                   edgecolor=SURFACE, lw=1.3, zorder=3)
    key = [n for n, _ in sorted(bt.items(), key=lambda x: -x[1])[:9]]
    key = list(dict.fromkeys(["Ama al-Aziz bt. Hizkiyahu"] + key))
    place_labels(ax, pos, key, fs=8.3, dy=-0.055)
    ax.legend(handles=[
        Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markersize=8, label="man"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MAGENTA, markersize=8, label="woman"),
        Line2D([0], [0], color=ORANGE, lw=2, label="marriage or betrothal"),
        Line2D([0], [0], color="#a8a49c", lw=1.2, label="descent, sibling, agency")],
        loc="lower left", frameon=False, fontsize=8.8, handletextpad=0.5, labelspacing=0.5)
    ax.axis("off")
    save(fig, "fig_kinship.png")


# ================================================ 7. Karaites and Rabbanites
def sect_group(n):
    s = persons.get(n, {}).get("sect", "unknown")
    if s.startswith("Rabbanite"):
        return "R"
    if s in ("Karaite", "Karaite (probable)"):
        return "K"
    if s.startswith("Karaite"):
        return "Kp"
    return "U"


def fig_rabbanite():
    """One small panel per document-cluster that contains an identified
    Rabbanite. Every orange dot sits inside a cluster; none sits between two."""
    keep = []
    for c in nx.connected_components(G):
        sub = G.subgraph(c)
        if any(sect_group(u) == "R" or sect_group(v) == "R" for u, v in sub.edges()):
            keep.append(sorted(c))
    keep.sort(key=len, reverse=True)
    n = len(keep)
    ncol = 5
    nrow = math.ceil(n / ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(9.2, 2.15 * nrow))
    axes = np.atleast_1d(axes).ravel()
    for ax, comp in zip(axes, keep):
        H = G.subgraph(comp).copy()
        pos = nx.kamada_kawai_layout(H) if len(comp) > 2 else nx.circular_layout(H)
        for u, v in H.edges():
            cross = "R" in (sect_group(u), sect_group(v)) and \
                    {sect_group(u), sect_group(v)} != {"R"}
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                    color=ORANGE if cross else EDGE, lw=0.9 if cross else 0.5,
                    alpha=0.75 if cross else 0.5, zorder=2 if cross else 1,
                    solid_capstyle="round")
        for nd in H:
            g = sect_group(nd)
            ax.scatter(*pos[nd], s=112 if g == "R" else 26,
                       color=ORANGE if g == "R" else (BLUE if g == "K" else "#a9c4e2"),
                       edgecolor=SURFACE, lw=1.3 if g == "R" else 0.7,
                       zorder=4 if g == "R" else 3)
        sm = sorted({d for _, _, dd in H.edges(data=True) for d in dd["docs"]})
        ttl = sm[0].split(" + ")[0] if sm else ""
        ax.set_title(f"{ttl}\n{len(comp)} people", fontsize=8.2, color=INK2,
                     loc="center", pad=4, linespacing=1.3)
        ax.set_aspect("equal"); ax.axis("off")
        ax.margins(0.18)
    for ax in axes[n:]:
        ax.axis("off")
    fig.legend(handles=[
        Line2D([0], [0], marker="o", color="w", markerfacecolor=ORANGE, markersize=9,
               label="identified Rabbanite"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markersize=7,
               label="identified Karaite"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#a9c4e2", markersize=7,
               label="presumed Karaite"),
        Line2D([0], [0], color=ORANGE, lw=1.6, label="a tie across the divide")],
        loc="lower center", frameon=False, fontsize=9, ncol=4, handletextpad=0.4,
        bbox_to_anchor=(0.5, -0.02))
    fig.subplots_adjust(bottom=0.13, hspace=0.34, wspace=0.06)
    save(fig, "fig_rabbanite.png", pad=0.12)


# ================================================== 8. priestly titles (new)
def fig_titles():
    order = [("Scribe", "scribes"), ("Witness", "signing witnesses"),
             ("WitnessOfAgency", "witnesses of the agency"),
             ("Agent", "agents (paqid)"), ("Groom", "grooms"),
             ("FamilyMention", "fathers in genealogies"), ("Bride", "brides")]
    vals = [NUM["titles"]["by_role"][k] for k, _ in order]
    base = NUM["titles"]["all_persons"]["percent"]
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    y = np.arange(len(order))[::-1]
    cols = [ORANGE if v["percent"] > base else BLUE for v in vals]
    ax.barh(y, [v["percent"] for v in vals], height=0.58, color=cols,
            edgecolor=SURFACE, linewidth=1.2)
    for yi, v in zip(y, vals):
        ax.text(v["percent"] + 1.3, yi, f"{v['percent']:.0f}%", va="center",
                fontsize=9.4, color=INK)
    ax.axvline(base, color=INK2, lw=1.0, ls=(0, (4, 3)), zorder=4)
    t = ax.text(base + 1.0, len(order) - 0.35,
                f"everyone in the database: {base:.0f}%", fontsize=8.6, color=INK2)
    halo(t)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{lab}  (n={v['n']})" for (_, lab), v in zip(order, vals)],
                       fontsize=9.6, color=INK)
    ax.set_xlim(0, 76)
    ax.set_xlabel("share of appearances made by a ha-Kohen or a ha-Levi")
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    save(fig, "fig_titles.png")


# ============================== 9. how many attest, by region (new)
def fig_attesters():
    rows = [r for r in NUM["attesters_by_region"]["rows"] if r["region"] != "Unknown"]
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    for i, (reg, col) in enumerate([("Palestine", ORANGE), ("Egypt", BLUE)]):
        sel = sorted([r for r in rows if r["region"] == reg], key=lambda r: r["n"])
        xs = []
        for v in sorted({r["n"] for r in sel}):
            k = sum(1 for r in sel if r["n"] == v)
            xs += list(np.linspace(-0.085 * (k - 1), 0.085 * (k - 1), k))
        for r, dx in zip(sel, xs):
            ax.scatter(i + dx, r["n"], s=118 if r["court_copy"] else 82,
                       color=col, edgecolor=SURFACE, lw=1.5, zorder=3,
                       marker="s" if r["court_copy"] else "o")
        m = float(np.median([r["n"] for r in sel]))
        ax.hlines(m, i - 0.3, i + 0.3, color=INK, lw=2.0, zorder=5)
        t = ax.text(i - 0.34, m, f"median {m:.0f}", va="center", ha="right",
                    fontsize=9.2, color=INK, fontweight="bold")
        halo(t)
        if reg == "Palestine":
            for r, dx in zip(sel, xs):
                t = ax.text(i + dx + 0.09, r["n"] + 0.42,
                            f"{r['place']} {int(float(r['year']))}", fontsize=8.4,
                            color=INK2, va="bottom", ha="left")
                halo(t)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([
        f"Palestine\n{sum(1 for r in rows if r['region']=='Palestine')} documents",
        f"Egypt\n{sum(1 for r in rows if r['region']=='Egypt')} documents"], fontsize=10)
    ax.set_ylabel("people named as attesting the document")
    ax.set_ylim(0, 18.6); ax.set_xlim(-0.95, 1.75)
    ax.set_yticks([0, 4, 8, 12, 16])
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.legend(handles=[Line2D([0], [0], marker="s", color="w", markerfacecolor=MUTED,
                              markersize=8, label="court copy")],
              loc="upper right", frameon=False, fontsize=8.8, handletextpad=0.4)
    save(fig, "fig_attesters.png")


# ================================ 10. ketubba vs betrothal, damage controlled
def fig_ketubba():
    kv = NUM["ketubba_vs_betrothal"]
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    groups = ["ketubba", "betrothal"]
    labels = {"ketubba": "ketubbot", "betrothal": "deeds of betrothal"}
    cols = {"ketubba": BLUE, "betrothal": ORANGE}
    x = np.arange(2)
    for ax, (field, title, fmt) in zip(axes, [
            ("mean_cast", "people named per document", "{:.1f}"),
            ("mean_witnesses_of_agency", "witnesses of the agency per document", "{:.2f}")]):
        w = 0.34
        for j, scope in enumerate(["all", "complete_only"]):
            vals = [kv[g][scope][field] for g in groups]
            ax.bar(x + (j - 0.5) * w, vals, w * 0.9,
                   color=[cols[g] for g in groups],
                   alpha=1.0 if scope == "complete_only" else 0.42,
                   edgecolor=SURFACE, linewidth=1.2)
            for xi, v in zip(x + (j - 0.5) * w, vals):
                ax.text(xi, v + (0.18 if field == "mean_cast" else 0.045),
                        fmt.format(v), ha="center", fontsize=8.8, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels([labels[g] for g in groups], fontsize=9.6)
        ax.set_title(title, fontsize=10.2)
        ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
        ax.set_ylim(0, (10.2 if field == "mean_cast" else 2.5))
    axes[0].set_ylabel("mean")
    axes[0].legend(handles=[
        matplotlib.patches.Patch(facecolor=MUTED, alpha=0.42, label="all documents"),
        matplotlib.patches.Patch(facecolor=MUTED, label="undamaged documents only")],
        loc="upper left", frameon=False, fontsize=8.6)
    save(fig, "fig_ketubba_betrothal.png")


if __name__ == "__main__":
    print("figures:")
    fig_clique()
    fig_backbone()
    fig_pool()
    fig_core_periphery()
    fig_nasi()
    fig_kinship()
    fig_rabbanite()
    fig_titles()
    fig_attesters()
    fig_ketubba()
    print("done ->", os.path.normpath(FIG))
