# -*- coding: utf-8 -*-
"""
Export the Karaite Geniza database to RDF (Turtle).

Design
------
Rather than reifying every appearance as an opaque blob, the graph uses the
standard event/role pattern of prosopographic ontologies (cf. CIDOC-CRM E7
Activity, Factoid model): the *appearance* is a first-class resource that links
a Person, a Document and an Action from the closed vocabulary, and carries the
evidential certainty. This keeps the historian's uncertainty machine-readable
and lets SPARQL reconstruct any of the networks used in the paper.

Vocabulary reuse: FOAF (persons/names), Dublin Core (document metadata), SKOS
(closed vocabularies as concept schemes), WGS84 geo (place coordinates),
PROV-O (source attribution). Project-specific terms live in the kg: namespace.

Usage:  cd src && python3 build_rdf.py
Output: ../rdf/karaite_geniza.ttl  (+ ontology header in the same file)
"""
import csv, os, re, hashlib

DS = "../dataset"
OUT = "../rdf"
os.makedirs(OUT, exist_ok=True)

def read(f):
    return list(csv.DictReader(open(f"{DS}/{f}", encoding="utf-8-sig")))

def slug(s, maxlen=60):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return (s[:maxlen] or "x")

def lit(s):
    s = (s or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'

persons   = read("persons.csv")
documents = read("documents.csv")
appear    = read("appearances.csv")
relations = read("relations.csv")
places    = read("places.csv")
actions   = read("actions.csv")
reltypes  = read("relation_types.csv")
edges     = read("edges_coappearance.csv")

doc_uri = {d["shelfmark"]: f"doc:{slug(d['shelfmark'])}" for d in documents}
per_uri = {p["canonical_name"]: f"kgp:{p['person_id']}" for p in persons}
plc_uri = {p["name_en"]: f"kgl:{p['place_id']}" for p in places}

L = []
W = L.append

# ---------------------------------------------------------------- prefixes
W("""@prefix kg:    <https://w3id.org/karaite-geniza/ontology#> .
@prefix kgp:   <https://w3id.org/karaite-geniza/person/> .
@prefix kgl:   <https://w3id.org/karaite-geniza/place/> .
@prefix doc:   <https://w3id.org/karaite-geniza/document/> .
@prefix app:   <https://w3id.org/karaite-geniza/appearance/> .
@prefix act:   <https://w3id.org/karaite-geniza/action/> .
@prefix rel:   <https://w3id.org/karaite-geniza/relation/> .
@prefix sect:  <https://w3id.org/karaite-geniza/sect/> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix geo:   <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
""")

# ---------------------------------------------------------------- ontology
W("""### ---------------------------------------------------------------- ontology
kg: a owl:Ontology ;
    dcterms:title "Karaite Geniza Social Network Ontology"@en ;
    dcterms:description "A lightweight prosopographic ontology for Karaite legal documents from the Cairo Geniza. Appearances are modelled as events linking a person, a document and an action from a closed vocabulary, with an explicit evidential certainty."@en ;
    dcterms:source "Olszowy-Schlanger 1998; Zinger 2017"@en .

kg:Person a owl:Class ; rdfs:subClassOf foaf:Person ;
    rdfs:label "Person"@en ; rdfs:label "אדם"@he .
kg:Document a owl:Class ;
    rdfs:label "Geniza document"@en ; rdfs:label "מסמך גניזה"@he .
kg:Place a owl:Class ;
    rdfs:label "Place"@en ; rdfs:label "מקום"@he .
kg:Appearance a owl:Class ;
    rdfs:label "Appearance"@en ; rdfs:label "הופעה"@he ;
    rdfs:comment "The event of a person performing one action in one document."@en .
kg:Action a owl:Class ; rdfs:subClassOf skos:Concept ;
    rdfs:label "Action"@en ; rdfs:label "פעולה"@he .
kg:Sect a owl:Class ; rdfs:subClassOf skos:Concept ;
    rdfs:label "Sect"@en ; rdfs:label "עדה"@he .

kg:hasAppearance   a owl:ObjectProperty ; rdfs:domain kg:Person ; rdfs:range kg:Appearance .
kg:inDocument      a owl:ObjectProperty ; rdfs:domain kg:Appearance ; rdfs:range kg:Document .
kg:performedAction a owl:ObjectProperty ; rdfs:domain kg:Appearance ; rdfs:range kg:Action .
kg:byPerson        a owl:ObjectProperty ; rdfs:domain kg:Appearance ; rdfs:range kg:Person .
kg:certainty       a owl:DatatypeProperty ; rdfs:domain kg:Appearance ;
    rdfs:comment "attested | reconstructed | contextual"@en .
kg:writtenAt       a owl:ObjectProperty ; rdfs:domain kg:Document ; rdfs:range kg:Place .
kg:placeCertainty  a owl:DatatypeProperty ; rdfs:domain kg:Document .
kg:yearEstimate    a owl:DatatypeProperty ; rdfs:domain kg:Document ; rdfs:range xsd:gYear .
kg:documentType    a owl:DatatypeProperty ; rdfs:domain kg:Document .
kg:hasSect         a owl:ObjectProperty ; rdfs:domain kg:Person ; rdfs:range kg:Sect .
kg:sectEvidence    a owl:DatatypeProperty ; rdfs:domain kg:Person .
kg:originPlace     a owl:ObjectProperty ; rdfs:domain kg:Person ; rdfs:range kg:Place .
kg:coAppearsWith   a owl:ObjectProperty, owl:SymmetricProperty ;
    rdfs:domain kg:Person ; rdfs:range kg:Person ;
    rdfs:comment "Joint presence in at least one legal act; kg:weight gives the number of shared documents."@en .
kg:weight          a owl:DatatypeProperty ; rdfs:range xsd:integer .
kg:evidence        a owl:DatatypeProperty .
kg:derivation      a owl:DatatypeProperty ;
    rdfs:comment "explicit (stated in the source) | derived_from_roles"@en .

### interpersonal relations (closed vocabulary)""")

for rt in reltypes:
    r = rt["relation"]
    sym = " , owl:SymmetricProperty" if r in ("sibling_of","first_cousin_of","married","betrothed",
                                              "divorced","business_associate_of","corresponded_with",
                                              "colleague_of","rival_of","associated_with") else ""
    W(f'rel:{r} a owl:ObjectProperty{sym} ; rdfs:subPropertyOf kg:relatedTo ; '
      f'rdfs:label {lit(r.replace("_"," "))}@en ; rdfs:label {lit(rt["relation_he"])}@he .')
W("kg:relatedTo a owl:ObjectProperty ; rdfs:label \"related to\"@en .\n")

# ---------------------------------------------------------------- vocabularies
W("### ---------------------------------------------------------------- closed vocabularies")
W('kg:ActionScheme a skos:ConceptScheme ; skos:prefLabel "Document actions"@en .')
for a in actions:
    W(f'act:{a["action_id"]} a kg:Action ; skos:inScheme kg:ActionScheme ; '
      f'skos:prefLabel {lit(a["action_en"])}@en ; skos:prefLabel {lit(a["action_he"])}@he ; '
      f'skos:definition {lit(a["definition"])}@en ; kg:actionClass {lit(a["action_class"])} .')
W("")
SECTS = {"Karaite":"Karaite","Karaite (probable)":"Karaite_probable","Karaite (presumed)":"Karaite_presumed",
         "Rabbanite":"Rabbanite","Rabbanite (probable)":"Rabbanite_probable","unknown":"unknown"}
W('kg:SectScheme a skos:ConceptScheme ; skos:prefLabel "Sect identifications"@en .')
for label, s in SECTS.items():
    W(f'sect:{s} a kg:Sect ; skos:inScheme kg:SectScheme ; skos:prefLabel {lit(label)}@en .')
W("")

# ---------------------------------------------------------------- places
W("### ---------------------------------------------------------------- places")
for p in places:
    t = [f'a kg:Place', f'rdfs:label {lit(p["name_en"])}@en', f'rdfs:label {lit(p["name_he"])}@he',
         f'kg:placeCategory {lit(p["category"])}']
    if p["princeton_url"]:
        t.append(f'owl:sameAs <{p["princeton_url"]}>')
    if p["coordinates"]:
        # "31° 46′ 36″ N, 35° 14′ 3″ E" -> decimal
        m = re.findall(r"(\d+)°\s*(\d+)′\s*([\d.]+)″\s*([NSEW])", p["coordinates"])
        if len(m) == 2:
            def dec(d, mi, s, h):
                v = int(d) + int(mi)/60 + float(s)/3600
                return -v if h in ("S","W") else v
            t.append(f'geo:lat "{dec(*m[0]):.5f}"^^xsd:decimal')
            t.append(f'geo:long "{dec(*m[1]):.5f}"^^xsd:decimal')
    W(f'{plc_uri[p["name_en"]]} ' + " ;\n    ".join(t) + " .")
W("")

# ---------------------------------------------------------------- documents
W("### ---------------------------------------------------------------- documents")
for d in documents:
    u = doc_uri[d["shelfmark"]]
    t = [f'a kg:Document', f'dcterms:identifier {lit(d["shelfmark"])}',
         f'rdfs:label {lit(d["shelfmark"])}', f'kg:documentType {lit(d["doc_type"])}',
         f'dcterms:date {lit(d["date_text"])}', f'dcterms:source {lit(d["source"])}']
    if d["year_est"]:
        t.append(f'kg:yearEstimate "{d["year_est"]}"^^xsd:gYear')
    if d["place"] and d["place"] != "Unknown":
        t.append(f'kg:writtenAt {plc_uri[d["place"]]}')
        t.append(f'kg:placeCertainty {lit(d["place_certainty"])}')
    if d["place_2"]:
        t.append(f'kg:writtenAt {plc_uri[d["place_2"]]}')
    if d["notes"]:
        t.append(f'rdfs:comment {lit(d["notes"])}@en')
    W(f'{u} ' + " ;\n    ".join(t) + " .")
W("")

# ---------------------------------------------------------------- persons
W("### ---------------------------------------------------------------- persons")
for p in persons:
    u = per_uri[p["canonical_name"]]
    t = [f'a kg:Person', f'foaf:name {lit(p["canonical_name"])}',
         f'dcterms:identifier {lit(p["person_id"])}',
         f'kg:hasSect sect:{SECTS[p["sect"]]}',
         f'foaf:gender {lit("female" if p["gender"]=="F" else "male")}']
    if p["name_variants"]:
        t.append(f'skos:altLabel {lit(p["name_variants"])}@en')
    if p["sect_evidence"]:
        t.append(f'kg:sectEvidence {lit(p["sect_evidence"])}@en')
    if p["origin_or_nisba_place"]:
        t.append(f'kg:originPlace {plc_uri[p["origin_or_nisba_place"]]}')
    if p["year_min"]:
        t.append(f'kg:activeFrom "{p["year_min"]}"^^xsd:gYear')
        t.append(f'kg:activeTo "{p["year_max"]}"^^xsd:gYear')
    if p["princeton_url"]:
        t.append(f'owl:sameAs <{p["princeton_url"]}>')
        t.append(f'kg:externalMatchCertainty {lit(p["princeton_match_certainty"])}')
    if p["notes"]:
        t.append(f'rdfs:comment {lit(p["notes"])}@en')
    W(f'{u} ' + " ;\n    ".join(t) + " .")
W("")

# ---------------------------------------------------------------- appearances
W("### ---------------------------------------------------------------- appearances (person x action x document)")
seen = set()
for i, a in enumerate(appear, 1):
    key = (a["person_id"], a["shelfmark"], a["action_id"])
    h = hashlib.md5("|".join(key).encode()).hexdigest()[:8]
    uri = f'app:{a["person_id"]}_{slug(a["shelfmark"],28)}_{a["action_id"]}_{h}'
    if uri in seen: continue
    seen.add(uri)
    t = [f'a kg:Appearance',
         f'kg:byPerson {per_uri[a["person"]]}',
         f'kg:inDocument {doc_uri[a["shelfmark"]]}',
         f'kg:performedAction act:{a["action_id"]}',
         f'kg:certainty {lit(a["certainty"])}']
    if a["note"]:
        t.append(f'rdfs:comment {lit(a["note"])}@en')
    W(f'{uri} ' + " ;\n    ".join(t) + " .")
    W(f'{per_uri[a["person"]]} kg:hasAppearance {uri} .')
W("")

# ---------------------------------------------------------------- relations
W("### ---------------------------------------------------------------- interpersonal relations")
for r in relations:
    s, t_, rl = per_uri[r["source"]], per_uri[r["target"]], r["relation"]
    W(f'{s} rel:{rl} {t_} .')
    # a reified statement carries the evidence
    h = hashlib.md5(f'{r["source_id"]}{rl}{r["target_id"]}'.encode()).hexdigest()[:8]
    W(f'''kg:st_{h} a rdf:Statement ;
    rdf:subject {s} ; rdf:predicate rel:{rl} ; rdf:object {t_} ;
    kg:evidence {lit(r["evidence"])} ; kg:derivation {lit(r["derivation"])}''' +
      (f' ; rdfs:comment {lit(r["note"])}@en .' if r["note"] else ' .'))
W("")

# ---------------------------------------------------------------- co-appearance
W("### ---------------------------------------------------------------- weighted co-appearance network")
for e in edges:
    a, b = per_uri[e["source"]], per_uri[e["target"]]
    h = hashlib.md5(f'{e["source_id"]}{e["target_id"]}'.encode()).hexdigest()[:8]
    W(f'{a} kg:coAppearsWith {b} .')
    W(f'''kg:co_{h} a rdf:Statement ;
    rdf:subject {a} ; rdf:predicate kg:coAppearsWith ; rdf:object {b} ;
    kg:weight {e["weight"]} ; kg:evidence {lit(e["docs"])} .''')

ttl = "\n".join(L) + "\n"
open(f"{OUT}/karaite_geniza.ttl", "w", encoding="utf-8").write(ttl)

# ---------------------------------------------------------------- validate
try:
    from rdflib import Graph
    g = Graph()
    g.parse(f"{OUT}/karaite_geniza.ttl", format="turtle")
    print(f"RDF OK: {len(g)} triples")
    q = """PREFIX kg: <https://w3id.org/karaite-geniza/ontology#>
           PREFIX act: <https://w3id.org/karaite-geniza/action/>
           PREFIX foaf: <http://xmlns.com/foaf/0.1/>
           SELECT ?n (COUNT(?a) AS ?c) WHERE {
             ?a a kg:Appearance ; kg:performedAction act:ACT07 ; kg:byPerson ?p .
             ?p foaf:name ?n . } GROUP BY ?n ORDER BY DESC(?c) LIMIT 5"""
    print("SPARQL check - most frequent witnesses:")
    for row in g.query(q):
        print("   ", row[0], int(row[1]))
    g.serialize(destination=f"{OUT}/karaite_geniza.rdf", format="xml")
    print("also written: rdf/karaite_geniza.rdf (RDF/XML)")
except ImportError:
    print("rdflib not installed - Turtle written but not validated")
