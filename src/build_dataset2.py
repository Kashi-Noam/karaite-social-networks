# -*- coding: utf-8 -*-
"""Build v2 dataset: person IDs & merges, closed place list, closed action vocabulary,
Princeton Geniza Lab joins, unified Excel workbook, validation report."""
import csv, os, re, unicodedata
from collections import defaultdict, Counter
from data_docs import DOCUMENTS
from data_appearances import A as BASE_A
from data_persons_relations import SECT as BASE_SECT, RELATIONS as BASE_RELATIONS
from data_extra import EXTRA_DOCS, EXTRA_APPEARANCES, EXTRA_SECT, EXTRA_RELATIONS, MERGES, VARIANTS, PRINCETON_MATCHES, PERSON_META
from data_places_actions import PLACES, DOC_PLACE, PERSON_ORIGIN, ACTIONS, ROLE2ACTION, RELATION_TYPES
from data_legal import LEGAL_DOCS, LEGAL_APPEARANCES, LEGAL_SECT, LEGAL_RELATIONS, LEGAL_SOURCE, LEGAL_ORIGIN
PERSON_ORIGIN = {**PERSON_ORIGIN, **LEGAL_ORIGIN}

MNT = "../data/external"
OUT = "../dataset"
os.makedirs(OUT, exist_ok=True)

# ---------------- load & merge raw layers
def canon(name):
    if name in MERGES: return MERGES[name][0]
    return name

DOCS = list(DOCUMENTS) + list(LEGAL_DOCS) + [d[:7] for d in EXTRA_DOCS]
docmeta = {d[0]: d for d in DOCS}

# ---- shelfmark as primary document identifier ----
SHELF = {}
for _d in DOCS:
    if _d[0].startswith("SRC_"):
        SHELF[_d[0]] = _d[0].replace("SRC_CH3","Chapter 3 (Olszowy-Schlanger)").replace("SRC_CH9","Chapter 9 (Olszowy-Schlanger)")
    elif _d[0]=="Z01":
        SHELF[_d[0]] = "Mosseri VII.43 + TS Ar.53.53"
    else:
        SHELF[_d[0]] = _d[1]
SHELF["CH3"] = "Chapter 3 (Olszowy-Schlanger)"
SHELF["CH9"] = "Chapter 9 (Olszowy-Schlanger)"
import re as _re
_docpat = _re.compile(r"\b(OS\d{2}|LD\d{2}|Z01|SRC_CH3|SRC_CH9|CH3|CH9)\b")
def ref(x):
    """replace doc ids with shelfmarks inside any string"""
    return _docpat.sub(lambda m: SHELF.get(m.group(1), m.group(1)), str(x))


APPS = []
for (doc,p,role,cert,note) in list(BASE_A)+list(LEGAL_APPEARANCES)+list(EXTRA_APPEARANCES):
    p2 = canon(p)
    if p != p2:
        note = (note+" | " if note else "") + f"merged from '{p}' ({MERGES[p][1]}: {MERGES[p][2]})"
        if cert=="attested": cert="reconstructed"
    APPS.append((doc,p2,role,cert,note))

RELS = []
seen_rel=set()
for (s,rel,t,ev,note) in list(BASE_RELATIONS)+list(LEGAL_RELATIONS)+list(EXTRA_RELATIONS):
    s2,t2 = canon(s), canon(t)
    if (s2,rel,t2) in seen_rel: continue
    seen_rel.add((s2,rel,t2))
    RELS.append([s2,rel,t2,ev,"explicit",note])

SECT = dict(BASE_SECT); SECT.update(LEGAL_SECT); SECT.update(EXTRA_SECT)
SECT = {canon(k):v for k,v in SECT.items()}

# derived relations from same-doc roles
by_doc_role = defaultdict(lambda: defaultdict(list))
for (doc,p,role,cert,note) in APPS:
    by_doc_role[doc][role].append(p)
def add_rel(s,rel,t,ev,note=""):
    if (s,rel,t) not in seen_rel and s!=t:
        RELS.append([s,rel,t,ev,"derived_from_roles",note]); seen_rel.add((s,rel,t))
for doc, rr in by_doc_role.items():
    for gf in rr.get("GroomFather",[]):
        for g in rr.get("Groom",[]): add_rel(gf,"father_of",g,doc)
    for bf in rr.get("BrideFather",[]):
        for b in rr.get("Bride",[]): add_rel(bf,"father_of",b,doc)
    for ag in rr.get("Agent",[]):
        for b in rr.get("Bride",[]): add_rel(ag,"agent_for",b,doc,"bride's agent (paqid)")
    for ag in rr.get("GroomAgent",[]):
        for g in rr.get("Groom",[]): add_rel(ag,"agent_for",g,doc,"groom's agent")

# ---------------- person registry with IDs
persons = defaultdict(lambda: {"roles":defaultdict(set),"docs":set(),"years":[],"place_ids":set(),"notes":set()})
for (doc,p,role,cert,note) in APPS:
    d = docmeta[doc]
    persons[p]["roles"][role].add(doc)
    persons[p]["docs"].add(doc)
    if len(d)>4 and d[4]: persons[p]["years"].append(d[4])
    raw_place = d[5] if len(d)>5 else ""
    pid_info = DOC_PLACE.get(raw_place)
    if pid_info and pid_info[0] not in ("PL00",): persons[p]["place_ids"].add(pid_info[0])
    if note: persons[p]["notes"].add(note)
for r in RELS:
    for n in (r[0],r[2]):
        if n not in persons:
            persons[n]["notes"].add(f"appears only through a relation ({r[3]})")

pid_of = {name: f"P{i+1:03d}" for i,name in enumerate(sorted(persons, key=lambda s: s.lower()))}

def sect_of(name):
    if name in SECT: return SECT[name]
    docs = persons[name]["docs"]
    if any(d.startswith(("OS","LD")) for d in docs):
        return ("Karaite (presumed)","participant in a Karaite legal document; no contrary evidence")
    return ("unknown","")

ROLE_ORDER = ["Groom","Bride","GroomFather","BrideFather","BrideGrandfather","GroomGrandfather",
              "Agent","GroomAgent","WitnessOfAgency","Witness","Scribe","Nasi","Judge","Trustee",
              "Guarantor","Party","Declarant","Mentioned"]
CLOSED_SECTS={"Karaite","Karaite (presumed)","Karaite (probable)","Rabbanite","Rabbanite (probable)","unknown"}

FEMALE_MARKERS=["bt.","Sitt","Sitt-al-Ahl","Sitt-al-Husn","Sitt-al-Fadl","Ama","Amat","Umm","Daughter",
 "Mu'ammala","Rayyisa","Malka","Husn","Hana","Na'ama","Mubaraka","Sara","Miriam","Rivqa","Karima","Sayyida",
 "Ghaliya","Faras","Fadla","Farajiyya","Sarwa","Yaman","Nasiya","al-Tifrat","Bahiyya","Wife"]
# Roles that only men fill anywhere in this corpus. Checked before any guess
# from the name, because a person labelled "Simha (father of Faras)" is a man
# however feminine his daughter's name is.
MALE_ROLES={"Groom","GroomFather","BrideFather","GroomGrandfather","BrideGrandfather","GroomAgent",
 "Witness","WitnessOfAgency","Scribe","Nasi","Judge","Trustee","Guarantor"}

def gender_of(name, info):
    roles=set(info["roles"])
    if "Bride" in roles: return "F"
    if roles & MALE_ROLES: return "M"
    if re.search(r"\bfather of\b", name, re.I): return "M"
    if re.search(r"\bmother of\b", name, re.I): return "F"
    rels=[r[1] for r in RELS if r[0]==name]
    if "mother_of" in rels: return "F"
    if "father_of" in rels: return "M"
    # Name morphology, matched on whole words only: plain substring matching
    # made "Fadla" catch "Fadlan" and "Faras" catch "(father of Faras)".
    if any(re.search(r"(?<![\w'])"+re.escape(m)+r"(?![\w'])", name) for m in FEMALE_MARKERS): return "F"
    return "M"

def action_of(role, cert):
    if role=="Mentioned":
        return "ACT15" if cert=="contextual" else "ACT14"
    return ROLE2ACTION[role]

# ---------------- Princeton joins
pgp_people = {p["name"]: p for p in csv.DictReader(open(f"{MNT}/people_list_from_princeton_gniza_lab.csv",encoding="utf-8-sig"))}
pgp_places = {p["name"]: p for p in csv.DictReader(open(f"{MNT}/places_list_from_princeton_gniza_lab.csv",encoding="utf-8-sig"))}
for our,(pname,certainty,note) in PRINCETON_MATCHES.items():
    assert pname in pgp_people, f"PGP name not found: {pname}"

# ---------------- write CSVs
def wcsv(fname, header, rows):
    with open(f"{OUT}/{fname}","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
    return [header]+rows

# documents
doc_rows=[]
for d in DOCS:
    doc_id=d[0]; raw_place=d[5] if len(d)>5 else ""
    pid,certn,pid2,pnote = DOC_PLACE.get(raw_place,("PL00","unknown",None,""))
    src = ("Olszowy-Schlanger 1998, no. %d"%int(doc_id[2:])) if doc_id.startswith("OS") else (LEGAL_SOURCE[doc_id] if doc_id in LEGAL_SOURCE else ("Zinger 2017" if doc_id=="Z01" else "secondary source unit"))
    doc_rows.append([SHELF[doc_id],src,d[2],d[3],d[4] if len(d)>4 and d[4] else "",
                     pid,PLACES[pid][0],certn,PLACES[pid2][0] if pid2 else "",pnote or "", ref(d[6]) if len(d)>6 else ""])
documents_table = wcsv("documents.csv",
 ["shelfmark","source","doc_type","date_text","year_est","place_id","place","place_certainty","place_2","place_note","notes"],doc_rows)

# appearances
app_rows=[]
for (doc,p,role,cert,note) in APPS:
    d=docmeta[doc]
    act=action_of(role,cert)
    raw_place=d[5] if len(d)>5 else ""
    pid=DOC_PLACE.get(raw_place,("PL00",))[0]
    app_rows.append([SHELF[doc],pid_of[p],p,role,act,ACTIONS[act][0],ACTIONS[act][1],cert,
                     d[4] if len(d)>4 and d[4] else "",PLACES[pid][0],d[2],ref(note)])
appearances_table = wcsv("appearances.csv",
 ["shelfmark","person_id","person","role","action_id","action_en","action_he","certainty","year_est","place","doc_type","note"],app_rows)

# persons
person_rows=[]
for name in sorted(persons, key=lambda s:s.lower()):
    info=persons[name]
    sect,ev = sect_of(name)
    assert sect in CLOSED_SECTS, f"sect not in closed list: {sect}"
    roles="; ".join(f"{r} ({', '.join(SHELF[x] for x in sorted(info['roles'][r]))})" for r in ROLE_ORDER if r in info["roles"])
    acts=sorted({ACTIONS[action_of(r, 'attested')][0] for r in info["roles"] if r!="Mentioned"} |
                ({"DocumentMention/ScholarlyMention"} if "Mentioned" in info["roles"] else set()))
    pm = PRINCETON_MATCHES.get(name)
    pgp = pgp_people.get(pm[0]) if pm else None
    origin = PERSON_ORIGIN.get(name,"")
    # attestation from sources outside the corpus (see PERSON_META)
    meta = PERSON_META.get(name)
    att_range = ("" if not meta else (str(meta[0]) if meta[0]==meta[1] else f"{meta[0]}-{meta[1]}"))
    att_ev = meta[2] if meta else ""
    if meta and meta[3]:
        info["notes"].add(meta[3])
    person_rows.append([pid_of[name],name,ref(VARIANTS.get(name,"")),sect,ref(ev),gender_of(name,info),
        roles,"; ".join(acts),len(info["docs"]),"; ".join(SHELF[x] for x in sorted(info["docs"])),
        min(info["years"]) if info["years"] else "",max(info["years"]) if info["years"] else "",
        "; ".join(sorted(PLACES[p][0] for p in info["place_ids"])),
        PLACES[origin][0] if origin else "",
        pm[0] if pm else "", pm[1] if pm else "", pgp["url"] if pgp else "",
        ref(" | ".join(sorted(info["notes"]))), att_range, att_ev])
persons_table = wcsv("persons.csv",
 ["person_id","canonical_name","name_variants","sect","sect_evidence","gender","roles","actions",
  "num_docs","docs","year_min","year_max","doc_places","origin_or_nisba_place",
  "princeton_name","princeton_match_certainty","princeton_url","notes",
  "attested_outside_corpus","attested_outside_evidence"],person_rows)

# relations
rel_rows=[]
for s,rel,t,ev,deriv,note in RELS:
    assert rel in RELATION_TYPES, f"relation not in closed list: {rel}"
    rel_rows.append([pid_of[s],s,rel,RELATION_TYPES[rel],pid_of[t],t,ref(ev),deriv,ref(note)])
relations_table = wcsv("relations.csv",
 ["source_id","source","relation","relation_he","target_id","target","evidence","derivation","note"],rel_rows)

# relation types
reltype_table = wcsv("relation_types.csv",["relation","relation_he"],[[k,v] for k,v in RELATION_TYPES.items()])

# actions vocabulary
actions_table = wcsv("actions.csv",["action_id","action_en","action_he","definition","action_class"],
    [[k,*v] for k,v in ACTIONS.items()])

# places
place_usage=Counter()
for d in DOCS:
    raw=d[5] if len(d)>5 else ""
    place_usage[DOC_PLACE.get(raw,("PL00",))[0]]+=1
place_rows=[]
for pid,(en,he,cat,pgpn) in PLACES.items():
    pgp=pgp_places.get(pgpn) if pgpn else None
    place_rows.append([pid,en,he,cat,place_usage.get(pid,0),
        pgpn or "",pgp["coordinates"] if pgp else "",pgp["url"] if pgp else "",
        pgp["name_variants"] if pgp else ""])
places_table = wcsv("places.csv",
 ["place_id","name_en","name_he","category","num_documents","princeton_name","coordinates","princeton_url","princeton_name_variants"],place_rows)

# co-appearance edges (active, non-contextual)
ACTIVE=set(ROLE_ORDER)-{"Mentioned"}
doc_people=defaultdict(set)
for (doc,p,role,cert,note) in APPS:
    if role in ACTIVE and cert!="contextual": doc_people[doc].add(p)
pair=defaultdict(set)
for doc,pp in doc_people.items():
    pp=sorted(pp)
    for i in range(len(pp)):
        for j in range(i+1,len(pp)): pair[(pp[i],pp[j])].add(doc)
edge_rows=[[pid_of[a],a,pid_of[b],b,len(ds),"; ".join(SHELF[x] for x in sorted(ds))] for (a,b),ds in sorted(pair.items())]
edges_table = wcsv("edges_coappearance.csv",["source_id","source","target_id","target","weight","docs"],edge_rows)

# princeton people tab: matched persons with the FULL PGP record
pp_rows=[]
for our,(pname,certainty,note) in sorted(PRINCETON_MATCHES.items()):
    g=pgp_people[pname]
    pp_rows.append([pid_of[our],our,certainty,ref(note),g["name"],g["name_variants"],g["gender"],g["social_roles"],
        g["auto_date_range"],g["manual_date_range"],g["description"],g["tags"],g["related_people_count"],
        g["family_traces_roots_to"],g["home_base"],g["traveled_to"],g["related_documents_count"],g["url"]])
princeton_table = wcsv("princeton_people_matches.csv",
 ["person_id","our_canonical_name","match_certainty","match_note","pgp_name","pgp_name_variants","pgp_gender",
  "pgp_social_roles","pgp_auto_dates","pgp_manual_dates","pgp_description","pgp_tags","pgp_related_people",
  "pgp_family_roots","pgp_home_base","pgp_traveled_to","pgp_related_documents","pgp_url"],pp_rows)

# ---------------- validation report
val=[]
val.append(["persons",len(persons)]); val.append(["appearances",len(APPS)])
val.append(["documents (incl. 2 secondary source units)",len(DOCS)])
val.append(["relations",len(RELS)]); val.append(["coappearance edges",len(pair)])
val.append(["princeton people matches",len(PRINCETON_MATCHES)])
val.append(["sect distribution",str(dict(Counter(r[3] for r in person_rows)))])
val.append(["action distribution",str(dict(Counter(r[5] for r in app_rows)))])
val.append(["place distribution (documents)",str({PLACES[p][0]:c for p,c in place_usage.items()})])
# closed list enforcement
bad_roles=[r for (_,_,r,_,_) in APPS if r not in ROLE_ORDER]; val.append(["roles outside closed list",str(bad_roles)])
bad_places=[d[0] for d in DOCS if (d[5] if len(d)>5 else "") not in DOC_PLACE]; val.append(["documents with unmapped place strings",str(bad_places)])
# duplicate candidates for manual review: same normalized "first + patronym"
def normname(n):
    n=unicodedata.normalize("NFKD",n); n="".join(c for c in n if not unicodedata.combining(c))
    n=n.lower(); n=re.sub(r"\((.*?)\)","",n); n=n.replace("ha-kohen","").replace("ha-levi","")
    n=n.replace(" bt. "," b. ").replace(" ben "," b. ")
    n=re.sub(r"[^a-z\.\s]"," ",n); n=re.sub(r"\s+"," ",n).strip()
    parts=n.split(" b. ")
    return (parts[0].split()[-1] if parts[0] else "", parts[1].split()[0] if len(parts)>1 and parts[1] else "")
groups=defaultdict(list)
for n in persons: groups[normname(n)].append(n)
dups=[v for k,v in groups.items() if len(v)>1 and k[0] and k[1]]
val.append(["possible-duplicate groups (manual review; NOT merged - editors give no identification)",""])
dup_rows=[]
for g in sorted(dups):
    dup_rows.append(["; ".join(f"{pid_of[x]} {x}" for x in sorted(g))])
validation_table=[["check","result"]]+[[str(a),str(b)] for a,b in val]
with open(f"{OUT}/validation_report.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerows(validation_table); w.writerow([])
    w.writerow(["possible duplicate name-groups (same given name + patronym; review manually)"])
    w.writerows(dup_rows)

# ---------------- Excel workbook
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
wb=Workbook(); wb.remove(wb.active)
HDR=PatternFill("solid",fgColor="D9E2F3"); BOLD=Font(bold=True)

readme=[["Karaite Social Networks from the Cairo Geniza - Unified Database (v2)"],[""],
 ["Sources:"],["  Olszowy-Schlanger, Karaite Marriage Documents from the Cairo Geniza (Brill 1998) - 57 documents + chapters 3 & 9 + editors' comments"],
 ["  Zinger, 'A Karaite-Rabbanite Court Session in mid-Eleventh Century Egypt', Ginzei Qedem 13 (2017) - document + footnotes"],
 ["  Princeton Geniza Lab exports: people list (2,037), places list (559)"],[""],
 ["Tabs:"],["  Documents - 58 documents + 2 secondary source units (SRC_CH3, SRC_CH9); place as closed-list ID + certainty"],
 ["  Persons - one row per individual with unique person_id; name variants; sect + evidence; Princeton match"],
 ["  Appearances - person x role x document; action_id from the closed action vocabulary"],
 ["  Actions - the closed action vocabulary (15 actions, EN/HE, definitions)"],
 ["  Places - the closed place list (IDs, Hebrew names, coordinates and URL from Princeton)"],
 ["  Relations - typed person-person relations; closed vocabulary in Relation_Types"],
 ["  Coappearance_Edges - weighted person-person edges (joint presence in a legal act)"],
 ["  Princeton_People - every person matched to the Princeton Geniza Lab with the FULL PGP record"],
 ["  Validation - counts, closed-list enforcement, possible-duplicate groups for manual review"],[""],
 ["Conventions:"],["  certainty: attested / reconstructed / contextual (contextual = known only from editors' comments)"],
 ["  'Karaite (presumed)' is a default assumption, not evidence - see sect_evidence"],
 ["  Persons are merged across documents/forms ONLY where the editors identify them; candidates are listed in Validation"],
]
ws=wb.create_sheet("README")
for row in readme: ws.append(row)
ws.column_dimensions["A"].width=110; ws["A1"].font=Font(bold=True,size=14)

def add_sheet(title, table, widths=None):
    ws=wb.create_sheet(title)
    for row in table: ws.append([str(c) if c is not None else "" for c in row])
    for c in ws[1]: c.font=BOLD; c.fill=HDR; c.alignment=Alignment(vertical="center")
    ws.freeze_panes="A2"
    for i,col in enumerate(ws.columns,1):
        maxlen=max(len(str(c.value or "")) for c in col)
        ws.column_dimensions[get_column_letter(i)].width=min(max(10,maxlen+2),55)
    ws.auto_filter.ref=ws.dimensions
add_sheet("Documents",documents_table)
add_sheet("Persons",persons_table)
add_sheet("Appearances",appearances_table)
add_sheet("Actions",actions_table)
add_sheet("Places",places_table)
add_sheet("Relations",relations_table)
add_sheet("Relation_Types",reltype_table)
add_sheet("Coappearance_Edges",edges_table)
add_sheet("Princeton_People",princeton_table)
vt=[["check","result"]]+[[str(a),str(b)] for a,b in val]+[["",""],["possible duplicate groups (same given name + patronym; not merged)",""]]+[[r[0],""] for r in dup_rows]
add_sheet("Validation",vt)
wb.save(f"{OUT}/Karaite_Geniza_Database.xlsx")

print("persons:",len(persons),"| appearances:",len(APPS),"| relations:",len(RELS),"| edges:",len(pair))
print("princeton matches:",len(PRINCETON_MATCHES))
print("sects:",dict(Counter(r[3] for r in person_rows)))
print("actions:",dict(Counter(r[5] for r in app_rows)))
print("doc places:",{PLACES[p][0]:c for p,c in place_usage.items()})
print("duplicate candidate groups:",len(dup_rows))
for r in dup_rows[:25]: print("  DUP?",r[0])
