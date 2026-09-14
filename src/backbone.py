# -*- coding: utf-8 -*-
"""
backbone.py — every quantitative claim in the paper, computed from dataset/.

This is the script the paper's data-availability note points at. It writes
`networks/paper_numbers.json`, and the paper generator (make_paper_he2.js)
reads that file, so no number is typed into the prose by hand.

    cd src && python3 backbone.py

WHAT COUNTS AS A CO-APPEARANCE (the one filter rule, applied everywhere)
-----------------------------------------------------------------------
An edge means "these two people were present at the same legal act".
So an appearance enters the network iff

    action_class != "Reference"        (see dataset/actions.csv)

The Reference class holds the four ways a person can be *named* in a document
without having stood in the room: NamedNasi (the reigning nasi in the dating
clause), FamilyMention (a father in a party's genealogy), DocumentMention and
ScholarlyMention (the editors' commentary). ScholarlyMention is exactly the
`contextual` certainty level, so this single rule also excludes everything the
editors reconstruct from outside the document.

Two derived networks are reported alongside it:
  * PRESENCE + NASI - the same network with the formulaic dating clause added
    back, which is the robustness test in the paper's Table 2;
  * ATTESTED ONLY - presence restricted to certainty == "attested", i.e.
    dropping the editors' reconstructions of damaged witness lists.
"""
import csv, heapq, json, math, os, random, itertools
from collections import defaultdict, Counter

import networkx as nx

DS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "networks")
SEED = 42


def read(name):
    with open(os.path.join(DS, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


docs = {d["shelfmark"]: d for d in read("documents.csv")}
persons = {p["canonical_name"]: p for p in read("persons.csv")}
apps = read("appearances.csv")
rels = read("relations.csv")
actions = {a["action_en"]: a for a in read("actions.csv")}

for ap in apps:
    ap["action_class"] = actions[ap["action_en"]]["action_class"]

PRESENCE = [a for a in apps if a["action_class"] != "Reference"]
PRESENCE_NASI = [a for a in apps if a["action_class"] != "Reference"
                 or a["action_en"] == "NamedNasi"]
ATTESTED = [a for a in PRESENCE if a["certainty"] == "attested"]
ATTESTING = {"Witness", "WitnessOfAgency", "Scribe", "Declarant"}

R = {}


# ---------------------------------------------------------------- graph tools
def cast(rows):
    """document -> set of persons present"""
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


def betweenness(G):
    H = G.copy()
    for u, v, dd in H.edges(data=True):
        dd["dist"] = 1.0 / max(dd.get("weight", 1), 1)
    return nx.betweenness_centrality(H, weight="dist", normalized=True)


def describe(G, label):
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    giant = G.subgraph(comps[0]).copy()
    comm = nx.community.louvain_communities(G, weight="weight", seed=SEED)
    return {
        "label": label,
        "nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
        "components": len(comps), "giant": len(comps[0]),
        "component_sizes": [len(c) for c in comps[:8]],
        "density": round(nx.density(G), 4),
        "clustering_whole": round(nx.average_clustering(G), 3),
        "clustering_giant": round(nx.average_clustering(giant), 3),
        "modularity": round(nx.community.modularity(G, comm, weight="weight"), 3),
        "n_communities": len(comm),
        "assortativity_whole": round(nx.degree_assortativity_coefficient(G), 3),
        "assortativity_giant": round(nx.degree_assortativity_coefficient(giant), 3),
        "cut_vertices_giant": sorted(nx.articulation_points(giant)),
    }


# ============================================================ 1. the corpus
def corpus():
    """Reconcile the edition's 57 documents with the database's 60 rows."""
    def family(t):
        t = t.lower()
        if "formular" in t or "book of" in t or "liturgy" in t:
            return "formulary"
        if "secondary" in t:
            return "secondary source unit"
        if "court session" in t:
            return "court record"
        if "betrothal" in t:
            return "deed of betrothal"
        if "ketubba" in t:
            return "ketubba"
        return "other"

    fam = Counter(family(d["doc_type"]) for d in docs.values())
    named = {a["shelfmark"] for a in PRESENCE_NASI}
    frag = Counter()
    for d in docs.values():
        f = family(d["doc_type"])
        if f in ("ketubba", "deed of betrothal"):
            frag[(f, "fragment" if "fragment" in d["doc_type"].lower() else "complete")] += 1
    return {
        "rows": len(docs),
        "edition_documents": sum(1 for d in docs.values() if "Olszowy" in d["source"]),
        "families": dict(fam),
        "fragment_split": {f"{k[0]}|{k[1]}": v for k, v in frag.items()},
        "documents_naming_someone": len(named),
        "documents_with_no_name": len(docs) - len(named),
        "places": dict(Counter(d["place"] for d in docs.values())),
    }


R["corpus"] = corpus()


# ======================================================= 2. the three networks
G, DP = graph(PRESENCE)
GN, DPN = graph(PRESENCE_NASI)
GA, DPA = graph(ATTESTED)
R["networks"] = {
    "presence": describe(G, "presence"),
    "presence_plus_nasi": describe(GN, "presence + nasi clause"),
    "attested_only": describe(GA, "attested only"),
}

GIANT = G.subgraph(max(nx.connected_components(G), key=len)).copy()
GIANT_N = GN.subgraph(max(nx.connected_components(GN), key=len)).copy()
R["networks"]["presence"]["giant_documents"] = sorted(
    {d for _, _, dd in GIANT.edges(data=True) for d in dd["docs"]})
R["networks"]["presence_plus_nasi"]["giant_documents"] = sorted(
    {d for _, _, dd in GIANT_N.edges(data=True) for d in dd["docs"]})


# ================================================== 3. the backbone: repeaters
def repeaters(rows):
    pd_ = defaultdict(set)
    for a in rows:
        pd_[a["person"]].add(a["shelfmark"])
    rep = {p: sorted(ds) for p, ds in pd_.items() if len(ds) > 1}
    return rep


REP = repeaters(PRESENCE)
REP_A = repeaters(ATTESTED)
edge_repeat = [(u, v, dd["weight"], dd["docs"])
               for u, v, dd in G.edges(data=True) if dd["weight"] > 1]
R["backbone"] = {
    "persons_in_network": G.number_of_nodes(),
    "persons_in_one_document": G.number_of_nodes() - len(REP),
    "repeaters": len(REP),
    "repeaters_detail": {p: ds for p, ds in sorted(REP.items())},
    "repeaters_attested_only": len(REP_A),
    "max_documents_per_person": max(len(v) for v in REP.values()),
    "edges_total": G.number_of_edges(),
    "edges_resting_on_two_documents": len(edge_repeat),
    "edges_detail": [[u, v, w, ds] for u, v, w, ds in edge_repeat],
    "share_single_document": round(
        100 * (G.number_of_nodes() - len(REP)) / G.number_of_nodes(), 1),
}


# =========================================== 4. which document pairs could share
def eligible_pairs(rows, max_gap=45):
    named = sorted(cast(rows).keys())
    cs = cast(rows)
    tot = elig = shared = shared_all = 0
    rejected = Counter()
    for x, y in itertools.combinations(named, 2):
        tot += 1
        dx, dy = docs[x], docs[y]
        px, py = dx["place"], dy["place"]
        try:
            yx, yy = float(dx["year_est"]), float(dy["year_est"])
        except ValueError:
            yx = yy = None
        ok = True
        if px != "Unknown" and py != "Unknown" and px != py:
            ok = False
            rejected["place"] += 1
        elif yx is not None and yy is not None and abs(yx - yy) > max_gap:
            ok = False
            rejected["time"] += 1
        does = len(cs[x] & cs[y]) > 0
        shared_all += does
        if ok:
            elig += 1
            shared += does
    return {"documents_naming_someone": len(named), "pairs": tot,
            "eligible": elig, "eligible_sharing": shared,
            "all_sharing": shared_all,
            "rate_percent": round(100 * shared / elig, 1) if elig else None,
            "naive_rate_percent": round(100 * shared_all / tot, 1) if tot else None,
            "rejected_by": dict(rejected)}


R["eligible_pairs"] = eligible_pairs(PRESENCE)
R["eligible_pairs_attested"] = eligible_pairs(ATTESTED)


# The pair test runs on the date and place columns, and those are not equally
# solid across the corpus.  Fourteen documents carry no date of their own and
# were given the midpoint of the century the editor assigns them; ten have no
# place at all, and an unknown place never rejects a pair.  Rerunning the test
# on the subsets whose metadata is real says which way that biases the answer.
CENTURY_ONLY = {
    "Bodl. MS Heb. b.12.31", "ENA NS 17.24", "ENA NS 3.23 + ENA NS 3.27",
    "II Firk. Heb. A. 717r", "TS 12.449", "TS 12.658", "TS 13 J 37.11",
    "TS 16.236", "TS 16.80", "TS 20.2", "TS 8.152", "TS AS 146.34",
    "TS AS 146.417r", "TS NS 320.34a,b",
}


def pair_test_sensitivity(rows):
    cs = cast(rows)
    named = sorted(cs)
    sizes = lambda ss: round(sum(len(cs[s]) for s in ss) / len(ss), 2)

    def subset(keep):
        sub = [r for r in rows if r["shelfmark"] in keep]
        return eligible_pairs(sub)

    dated = {s for s in named if s not in CENTURY_ONLY}
    certain = {s for s in named if docs[s]["place_certainty"] == "certain"}
    return {
        "all": eligible_pairs(rows),
        "dated_only": subset(dated),
        "certain_place_only": subset(certain),
        "by_max_gap": {str(g): eligible_pairs(rows, max_gap=g) for g in
                       (25, 45, 70, 10000)},
        "metadata_quality": {
            "place_certain": len(certain),
            "place_probable": sum(1 for s in named
                                  if docs[s]["place_certainty"] == "probable"),
            "place_unknown": sum(1 for s in named
                                 if docs[s]["place_certainty"] == "unknown"),
            "date_from_document": len(dated),
            "date_century_only": len(named) - len(dated),
        },
        "mean_cast": {
            "dated": sizes(dated),
            "century_only": sizes([s for s in named if s in CENTURY_ONLY]),
            "place_unknown": sizes([s for s in named
                                    if docs[s]["place"] == "Unknown"]),
        },
    }


R["pair_test_sensitivity"] = pair_test_sensitivity(PRESENCE)


# ==================================================== 5. how big was the pool?
def simulate_pool(rows, trials=400, seed=SEED):
    """Draw the observed cast sizes at random from a pool of N adult men and
    count how many people come out in more than one document.  The N where the
    curve crosses the observed number of repeaters is the estimate."""
    sizes = [len(v) for v in cast(rows).values() if len(v) > 1]
    observed = len(repeaters(rows))
    rng = random.Random(seed)
    curve = []
    for N in [100, 150, 200, 300, 400, 500, 650, 800, 1000, 1300,
              1600, 2000, 2600, 3200, 4000, 5000, 6500, 8000]:
        if N < max(sizes):
            continue
        tot = 0
        for _ in range(trials):
            seen = Counter()
            for k in sizes:
                for who in rng.sample(range(N), k):
                    seen[who] += 1
            tot += sum(1 for c in seen.values() if c > 1)
        curve.append({"N": N, "expected_repeaters": round(tot / trials, 2)})
    est = None
    for a, b in zip(curve, curve[1:]):
        if a["expected_repeaters"] >= observed >= b["expected_repeaters"]:
            lo, hi = a, b
            span = lo["expected_repeaters"] - hi["expected_repeaters"]
            f = (lo["expected_repeaters"] - observed) / span if span else 0
            est = int(round(lo["N"] + f * (hi["N"] - lo["N"])))
            break
    return {"observed_repeaters": observed, "cast_sizes": sorted(sizes, reverse=True),
            "documents_used": len(sizes), "curve": curve, "estimate": est}


def chao1(rows):
    """Chao (1984): N >= S + f1^2 / (2 f2), from the singleton/doubleton counts."""
    counts = Counter()
    for a in rows:
        counts[a["person"]] += 0
    pd_ = defaultdict(set)
    for a in rows:
        pd_[a["person"]].add(a["shelfmark"])
    n = Counter(len(v) for v in pd_.values())
    S, f1, f2 = len(pd_), n[1], n[2]
    if f2 == 0:
        return {"observed": S, "f1": f1, "f2": f2, "estimate": None,
                "note": "no doubletons; the bias-corrected form is used instead",
                "estimate_bias_corrected": int(round(S + f1 * (f1 - 1) / 2))}
    return {"observed": S, "f1": f1, "f2": f2,
            "estimate": int(round(S + f1 * f1 / (2 * f2))),
            "estimate_bias_corrected": int(round(S + f1 * (f1 - 1) / (2 * (f2 + 1))))}


FUSTAT = [a for a in PRESENCE
          if docs[a["shelfmark"]]["place"] == "Fustat"
          and docs[a["shelfmark"]]["year_est"] not in ("", None)
          and 1030 <= float(docs[a["shelfmark"]]["year_est"]) <= 1074]
R["pool"] = {"whole_corpus": simulate_pool(PRESENCE),
             "fustat_1030_1074": simulate_pool(FUSTAT),
             "chao_whole_corpus": chao1(PRESENCE),
             "chao_fustat": chao1(FUSTAT)}


# ------------------------------------------------ is the pool estimate sound?
# Three questions a reader is entitled to ask, each answered by a computation
# rather than by an assurance:
#   1. does the Monte-Carlo agree with the expectation worked out on paper?
#   2. does losing documents - the Geniza's defining property - bias it?
#   3. what happens if witnesses were not drawn with equal probability?
def expected_repeaters(pool, sizes):
    """E[#people in >1 document] when each document draws its cast at random
    from a pool of `pool` men.  Person-by-person: with p_i = k_i / pool, the
    chance of appearing never is prod(1-p_i) and exactly once is
    sum_i p_i/(1-p_i) * prod(1-p_i)."""
    p = [k / pool for k in sizes]
    none = math.prod(1 - x for x in p)
    once = sum(x / (1 - x) for x in p) * none
    return pool * (1 - none - once)


def solve_pool(sizes, observed):
    """The pool size at which the expectation above equals what we observed."""
    if not sizes or observed <= 0:
        return None
    lo, hi = max(sizes) + 1, 200_000
    if expected_repeaters(lo, sizes) < observed:
        return None
    for _ in range(70):
        mid = (lo + hi) / 2
        if expected_repeaters(mid, sizes) > observed:
            lo = mid
        else:
            hi = mid
    return int(round(lo))


def weighted_sample(pool, k, weights, rng):
    """k distinct indices drawn with probability proportional to `weights`
    (Efraimidis-Spirakis: take the k largest u**(1/w))."""
    keys = ((rng.random() ** (1.0 / weights[i]), i) for i in range(pool))
    return [i for _, i in heapq.nlargest(k, keys)]


def pool_robustness(rows, subsample_trials=300, seed=SEED):
    cs = {k: v for k, v in cast(rows).items() if len(v) > 1}
    shelf = sorted(cs)
    sizes = [len(cs[s]) for s in shelf]
    observed = len(repeaters(rows))

    def observed_in(subset):
        c = Counter()
        for s in subset:
            for p in cs[s]:
                c[p] += 1
        return sum(1 for v in c.values() if v > 1)

    rng = random.Random(seed)
    subsample = {}
    for frac in (0.75, 0.5, 0.35):
        ests = []
        for _ in range(subsample_trials):
            sub = rng.sample(shelf, max(3, round(frac * len(shelf))))
            e = solve_pool([len(cs[s]) for s in sub], observed_in(sub))
            if e:
                ests.append(e)
        ests.sort()
        subsample[f"keep_{int(frac * 100)}_percent"] = {
            "usable_trials": len(ests),
            "median_estimate": ests[len(ests) // 2] if ests else None,
            "q1": ests[len(ests) // 4] if ests else None,
            "q3": ests[3 * len(ests) // 4] if ests else None,
        }

    def under_preference(alpha, trials=60):
        """Repeat the draw when the chance of being asked to witness falls off
        as a power law over the pool, and report where the curve now crosses."""
        r = random.Random(seed)
        curve = []
        for pool in (1500, 2300, 3500, 5000, 8000, 12000):
            w = [1.0 / ((i + 1) ** alpha) for i in range(pool)]
            tot = 0
            for _ in range(trials):
                seen = Counter()
                for k in sizes:
                    for who in weighted_sample(pool, k, w, r):
                        seen[who] += 1
                tot += sum(1 for v in seen.values() if v > 1)
            curve.append({"pool": pool, "expected_repeaters": round(tot / trials, 1)})
        crossing = None
        for a, b in zip(curve, curve[1:]):
            if a["expected_repeaters"] >= observed >= b["expected_repeaters"]:
                crossing = [a["pool"], b["pool"]]
                break
        return {"curve": curve, "crossing": crossing}

    pairs = sum(a * b for a, b in itertools.combinations(sizes, 2))
    return {
        "observed_repeaters": observed,
        "documents_used": len(sizes),
        "analytic_estimate": solve_pool(sizes, observed),
        "first_order_estimate": int(round(pairs / observed)) if observed else None,
        "subsample": subsample,
        "preference": {f"alpha_{a}": under_preference(a) for a in (0.0, 0.3, 0.6)},
    }


R["pool_robustness"] = {"whole_corpus": pool_robustness(PRESENCE),
                        "fustat_1030_1074": pool_robustness(FUSTAT)}


# ===================================================== 6. who holds it together
def broker_table(Gx, rows, top=12):
    bt = betweenness(Gx)
    roles = defaultdict(set)
    for a in rows:
        roles[a["person"]].add(a["action_en"])
    pos = {k: v for k, v in bt.items() if v > 0}
    out = []
    for n, v in sorted(pos.items(), key=lambda x: -x[1])[:top]:
        out.append({"person": n, "betweenness": round(v, 4),
                    "degree": Gx.degree(n), "roles": sorted(roles[n]),
                    "formal_office": bool(roles[n] & {"Judge", "Trustee", "NamedNasi", "Scribe", "Declarant"})})
    return {"n_with_positive_betweenness": len(pos), "top": out}


R["brokers"] = {
    "presence": broker_table(G, PRESENCE),
    "presence_plus_nasi": broker_table(GN, PRESENCE_NASI),
}
R["brokers"]["no_office_among_positive"] = sum(
    1 for x in R["brokers"]["presence"]["top"] if not x["formal_office"])


# ============================================ 7. Kohen and Levi by role  (new)
def title(name):
    if "Kohen" in name:
        return "Kohen"
    if "Levi" in name:
        return "Levi"
    return "Israel"


def title_share(rows, action=None):
    sel = [a for a in rows if action is None or a["action_en"] == action]
    if not sel:
        return None
    n = sum(1 for a in sel if title(a["person"]) != "Israel")
    return {"n": len(sel), "priestly": n, "percent": round(100 * n / len(sel), 1)}


R["titles"] = {
    "by_role": {act: title_share(apps, act) for act in
                ["Scribe", "Witness", "WitnessOfAgency", "Agent", "Groom",
                 "Bride", "FamilyMention", "Judge", "NamedNasi"]},
    "all_persons": {"n": len(persons),
                    "priestly": sum(1 for n in persons if title(n) != "Israel"),
                    "percent": round(100 * sum(1 for n in persons if title(n) != "Israel") / len(persons), 1)},
}
att_docs = defaultdict(set)
for a in apps:
    if a["action_en"] in ATTESTING and a["certainty"] != "contextual":
        att_docs[a["shelfmark"]].add(a["person"])
big = {k: v for k, v in att_docs.items() if len(v) >= 3}
R["titles"]["documents_with_3plus_attesters"] = len(big)
R["titles"]["of_those_with_a_priestly_attester"] = sum(
    1 for v in big.values() if any(title(x) != "Israel" for x in v))
R["titles"]["exceptions"] = [k for k, v in big.items()
                             if not any(title(x) != "Israel" for x in v)]


# ================================== 8. how many attest, Palestine vs Egypt (new)
REGION = {"Fustat": "Egypt", "Cairo": "Egypt", "Egypt (region)": "Egypt",
          "Jerusalem": "Palestine", "Ramle": "Palestine", "Tyre": "Palestine",
          "Palestine (region)": "Palestine"}


def attester_counts():
    rows = []
    for sm, pp in att_docs.items():
        d = docs[sm]
        reg = REGION.get(d["place"], "Unknown")
        rows.append({"shelfmark": sm, "region": reg, "place": d["place"],
                     "year": d["year_est"], "n": len(pp),
                     "fragment": "fragment" in d["doc_type"].lower(),
                     "court_copy": "court copy" in d["doc_type"].lower()})
    return rows


AT = attester_counts()


def med(v):
    v = sorted(v)
    return (v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2) if v else None


R["attesters_by_region"] = {
    "rows": AT,
    "summary": {reg: {"documents": len([r for r in AT if r["region"] == reg]),
                      "median": med([r["n"] for r in AT if r["region"] == reg]),
                      "max": max([r["n"] for r in AT if r["region"] == reg], default=None)}
                for reg in ("Palestine", "Egypt")},
    "excluding_court_copies": {
        reg: {"documents": len([r for r in AT if r["region"] == reg and not r["court_copy"]]),
              "median": med([r["n"] for r in AT if r["region"] == reg and not r["court_copy"]])}
        for reg in ("Palestine", "Egypt")},
}


# ============================== 9. ketubba vs betrothal, controlling for damage
def doc_family(sm):
    t = docs[sm]["doc_type"].lower()
    if "formular" in t or "book of" in t or "liturgy" in t:
        return "formulary"
    if "betrothal" in t:
        return "betrothal"
    if "ketubba" in t:
        return "ketubba"
    return "other"


def by_family():
    out = {}
    for fam in ("ketubba", "betrothal"):
        sel = [sm for sm in DP if doc_family(sm) == fam]
        whole = [sm for sm in sel if "fragment" not in docs[sm]["doc_type"].lower()]
        def stats(lst):
            if not lst:
                return None
            casts = [len(DP[sm]) for sm in lst]
            woa = [sum(1 for a in PRESENCE if a["shelfmark"] == sm and a["action_en"] == "WitnessOfAgency") for sm in lst]
            nasi = sum(1 for sm in lst if any(a["shelfmark"] == sm and a["action_en"] == "NamedNasi" for a in apps))
            judge = sum(1 for sm in lst if any(a["shelfmark"] == sm and a["action_en"] == "Judge" for a in apps))
            return {"documents": len(lst),
                    "mean_cast": round(sum(casts) / len(casts), 2),
                    "median_cast": med(casts),
                    "mean_witnesses_of_agency": round(sum(woa) / len(lst), 2),
                    "documents_naming_the_nasi": nasi,
                    "documents_with_a_judge_acting": judge}
        out[fam] = {"all": stats(sel), "complete_only": stats(whole)}
    return out


R["ketubba_vs_betrothal"] = by_family()


# ==================================================== 10. women  (corrected)
GENDER = {n: p["gender"] for n, p in persons.items()}


def women():
    inG = [n for n in G if GENDER.get(n) == "F"]
    ww = [(u, v) for u, v in G.edges() if GENDER.get(u) == "F" and GENDER.get(v) == "F"]
    per_doc = Counter()
    for sm, pp in DP.items():
        per_doc[sum(1 for x in pp if GENDER.get(x) == "F")] += 1
    roles = Counter(a["action_en"] for a in PRESENCE if GENDER.get(a["person"]) == "F")
    # The same count over every appearance, mention included.  It is larger:
    # three documents name two women or more (the 1055 protocol names four),
    # but in each of them only one woman was actually present, which is why
    # there is no woman-woman edge anywhere in the network.
    mention_doc = defaultdict(set)
    for a in apps:
        if GENDER.get(a["person"]) == "F":
            mention_doc[a["shelfmark"]].add(a["person"])
    per_doc_mentions = Counter(len(v) for v in mention_doc.values())
    multi = {sm: sorted(v) for sm, v in mention_doc.items() if len(v) > 1}
    return {"women_in_network": len(inG), "men_in_network": G.number_of_nodes() - len(inG),
            "woman_woman_edges": len(ww),
            "documents_by_number_of_women": dict(sorted(per_doc.items())),
            "documents_by_number_of_women_mentions":
                dict(sorted(per_doc_mentions.items())),
            "documents_naming_two_or_more_women": multi,
            "roles": dict(roles),
            "women_in_database": sum(1 for g in GENDER.values() if g == "F")}


R["women"] = women()

# kinship network: is a woman's structural weight really unusual?
KIN = {"married", "betrothed", "divorced", "first_husband_of", "father_of",
       "mother_of", "sibling_of", "first_cousin_of", "uncle_of", "ancestor_of",
       "son_in_law_of", "agent_for"}
K = nx.Graph()
for r in rels:
    if r["relation"] in KIN:
        K.add_edge(r["source"], r["target"], weight=1)
kb = betweenness(K)
fem = [kb[n] for n in K if GENDER.get(n) == "F"]
mal = [kb[n] for n in K if GENDER.get(n) == "M"]
kdeg = dict(K.degree())
R["kinship"] = {
    "nodes": K.number_of_nodes(), "edges": K.number_of_edges(),
    "components": nx.number_connected_components(K),
    "largest_family": len(max(nx.connected_components(K), key=len)),
    "clustering": round(nx.average_clustering(K), 3),
    "women": {"n": len(fem), "positive_betweenness": sum(1 for x in fem if x > 0),
              "mean_betweenness": round(sum(fem) / len(fem), 5),
              "mean_degree": round(sum(kdeg[n] for n in K if GENDER.get(n) == "F") / len(fem), 2)},
    "men": {"n": len(mal), "positive_betweenness": sum(1 for x in mal if x > 0),
            "mean_betweenness": round(sum(mal) / len(mal), 5),
            "mean_degree": round(sum(kdeg[n] for n in K if GENDER.get(n) == "M") / len(mal), 2)},
    "top_betweenness": [{"person": n, "betweenness": round(v, 4), "degree": kdeg[n],
                         "gender": GENDER.get(n)}
                        for n, v in sorted(kb.items(), key=lambda x: -x[1])[:8]],
}
_amat = K.subgraph(max(nx.connected_components(K), key=len)).copy()
_amat.remove_node("Ama al-Aziz bt. Hizkiyahu")
R["kinship"]["largest_family_without_ama_al_aziz"] = sorted(
    (len(c) for c in nx.connected_components(_amat)), reverse=True)


# ================================================= 11. Karaites and Rabbanites
def sect_group(n):
    s = persons.get(n, {}).get("sect", "unknown")
    if s.startswith("Rabbanite"):
        return "R"
    if s == "Karaite" or s == "Karaite (probable)":
        return "K"
    if s.startswith("Karaite"):
        return "Kp"
    return "U"


rab_docs = sorted({a["shelfmark"] for a in PRESENCE_NASI if sect_group(a["person"]) == "R"})
rab_docs_any = sorted({a["shelfmark"] for a in apps if sect_group(a["person"]) == "R"})
pair = Counter()
for u, v in G.edges():
    pair[tuple(sorted((sect_group(u), sect_group(v))))] += 1
named_docs = sorted(cast(PRESENCE_NASI).keys())
R["sects"] = {
    "documents_naming_someone": len(named_docs),
    "documents_with_a_present_rabbanite": len(rab_docs),
    "documents_with_a_rabbanite_anywhere": len(rab_docs_any),
    "rabbanite_documents": rab_docs,
    "edge_pairs": {"|".join(k): v for k, v in sorted(pair.items())},
    "cross_sect_edges_explicit": pair[("K", "R")],
    "cross_sect_edges_presumed": pair[("Kp", "R")],
    "mean_cast_with_rabbanite": round(
        sum(len(DPN[s]) for s in rab_docs) / len(rab_docs), 2),
    "mean_cast_without": round(
        sum(len(DPN[s]) for s in named_docs if s not in rab_docs) /
        max(1, len(named_docs) - len(rab_docs)), 2),
    "rabbanites_in_network": sum(1 for n in G if sect_group(n) == "R"),
    "rabbanite_mean_degree": round(
        sum(G.degree(n) for n in G if sect_group(n) == "R") /
        max(1, sum(1 for n in G if sect_group(n) == "R")), 2),
    "rabbanite_max_betweenness": round(
        max((betweenness(G)[n] for n in G if sect_group(n) == "R"), default=0), 5),
    "sect_distribution": dict(Counter(p["sect"] for p in persons.values())),
}


# ============================== 12. the agent (paqid): who acts for the bride?
def agents():
    kin = defaultdict(set)
    for r in rels:
        if r["relation"] in ("father_of", "mother_of", "sibling_of", "uncle_of",
                             "first_cousin_of", "ancestor_of"):
            kin[r["source"]].add(r["target"])
            kin[r["target"]].add(r["source"])
    out = []
    for r in rels:
        if r["relation"] != "agent_for":
            continue
        src, tgt = r["source"], r["target"]
        rel = "kin" if tgt in kin.get(src, ()) else None
        if rel is None:
            # patronymic match: "X b. Y" and "Z bt. Y" are siblings
            import re
            ms = re.search(r"\bb\.\s+(.+)$", src)
            mt = re.search(r"\bbt\.\s+(.+)$", tgt)
            if ms and mt and ms.group(1).split(" (")[0] == mt.group(1).split(" (")[0]:
                rel = "sibling (patronymic)"
        out.append({"agent": src, "for": tgt, "evidence": r["evidence"],
                    "relation": rel or "not a known relative"})
    counts = Counter(x["relation"] for x in out)
    reuse = Counter(x["agent"] for x in out)
    return {"appointments": len(out), "detail": out,
            "by_relation": dict(counts),
            "agents_serving_twice": {k: v for k, v in reuse.items() if v > 1}}


R["agents"] = agents()


# ================================ 13. the signatories outside this corpus (new)
outside = [{"person": p["canonical_name"],
            "where": p.get("attested_outside_corpus", ""),
            "evidence": p.get("attested_outside_evidence", "")}
           for p in persons.values() if p.get("attested_outside_corpus")]
R["outside_corpus"] = {"persons": len(outside), "detail": outside}


# ============================================ 14. is Louvain stable?  (seeding)
counts = []
for s in range(20):
    c = nx.community.louvain_communities(G, weight="weight", seed=s)
    counts.append(len(c))
comm42 = nx.community.louvain_communities(G, weight="weight", seed=SEED)
pdocs = defaultdict(set)
for a in PRESENCE:
    pdocs[a["person"]].add(a["shelfmark"])
single_doc_comms = sum(1 for c in comm42
                       if len({d for n in c for d in pdocs[n]}) == 1)
R["louvain"] = {"seed": SEED, "communities_at_seed": len(comm42),
                "counts_over_20_seeds": counts,
                "min": min(counts), "max": max(counts),
                "communities_that_are_one_document": single_doc_comms}


# ================================================= 15. alternative weightings
def weighted_variants():
    wA, wB, wC = defaultdict(int), defaultdict(float), defaultdict(int)
    for doc, pp in DP.items():
        pp = sorted(pp); k = len(pp)
        for u, v in itertools.combinations(pp, 2):
            wA[(u, v)] += 1
            wB[(u, v)] += 1.0 / max(k - 1, 1)
            wC[(u, v)] = 1
    out = {}
    for name, w in (("shared_documents", wA), ("newman_1_over_k", wB), ("binary", wC)):
        H = nx.Graph()
        for (u, v), ww in w.items():
            H.add_edge(u, v, weight=round(ww, 4))
        bt = betweenness(H)
        out[name] = [n for n, _ in sorted(bt.items(), key=lambda x: -x[1])[:10]]
    a, b, c = out["shared_documents"], out["newman_1_over_k"], out["binary"]
    return {"top10": out, "overlap_A_B": len(set(a) & set(b)),
            "overlap_A_C": len(set(a) & set(c))}


R["weighting"] = weighted_variants()

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "paper_numbers.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

print("wrote networks/paper_numbers.json")
for k in ("corpus", "backbone", "eligible_pairs", "louvain"):
    print(f"\n[{k}]")
    for kk, vv in R[k].items():
        if not isinstance(vv, (list, dict)) or len(str(vv)) < 160:
            print(f"   {kk}: {vv}")
print("\n[networks]")
for k, v in R["networks"].items():
    print(f"   {k}: nodes={v['nodes']} edges={v['edges']} comps={v['components']} "
          f"giant={v['giant']} Q={v['modularity']} cut={v['cut_vertices_giant']}")
