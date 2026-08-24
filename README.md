# Karaite Social Networks from the Cairo Geniza

A prosopographic database and Social Network Analysis (SNA) of the medieval Karaite
community of Egypt and Palestine (10th–13th centuries), built from Cairo Geniza legal
documents. Seminar project for the course **"Karaite Jews in the Middle East"**
(Hebrew University of Jerusalem).

מאגר פרוסופוגרפי וניתוח רשתות חברתיות של הקהילה הקראית במזרח התיכון בימי הביניים,
על בסיס מסמכים משפטיים מגניזת קהיר.

## Sources

The data were harvested manually, document by document — including the editors'
introductions, commentaries and footnotes — from:

1. **Olszowy-Schlanger, Judith.** *Karaite Marriage Documents from the Cairo Geniza:
   Legal Tradition and Community Life in Mediaeval Egypt and Palestine.* Leiden: Brill, 1998.
   All 57 edited documents (deeds of betrothal, ketubbot, court copies, formularies and two
   mixed Karaite–Rabbanite contracts, 984–1201 CE), plus the prosopographic material of
   chapter 3 (Tustaris, Sahlawaya, al-Qazzaz, ben Zita families) and chapter 9 (genealogy
   of the Karaite nesiʾim).
2. **Zinger, Oded.** "A Karaite-Rabbanite Court Session in mid-Eleventh Century Egypt,"
   *Ginzei Qedem* 13 (2017): 95\*–116\*. The record of a joint court session held on
   13 July 1055 at the majlis of the Karaite nasi Josiah b. Solomon, with the Rabbanite
   judge ʿEli b. ʿAmram — including the persons discussed in the footnotes.
3. **Princeton Geniza Lab** (https://geniza.princeton.edu) — exports of the people and
   places lists, used to enrich and cross-identify persons (25 matches) and places
   (15 gazetteer links with coordinates).

> **Copyright note:** the two source PDFs and the raw extracted text are **not**
> included in this repository. `extraction/extract_texts.py` reproduces the text
> extraction step if you have legal access to the publications.

## Database overview (v2)

| table | rows | content |
|---|---|---|
| `dataset/documents.csv` | 60 | 58 documents + 2 secondary source units. **Identifier = shelfmark** (e.g. `TS 16.109 + TS AS 153.489`); place as closed-list ID + separate certainty column |
| `dataset/persons.csv` | 350 | unique `person_id`, canonical name, name variants, sect + written evidence, gender, roles, actions, documents, activity years, origin/nisba place, Princeton match |
| `dataset/appearances.csv` | 390 | person × role × document — the atomic evidence unit, with `certainty` (attested / reconstructed / contextual) and an `action_id` from the closed action vocabulary |
| `dataset/actions.csv` | 15 | closed action vocabulary (EN/HE + definitions): Groom, Bride, LegalParty, Guarantor, Agent, WitnessOfAgency, Witness, Scribe, Declarant, Judge, Trustee, NamedNasi, FamilyMention, DocumentMention, ScholarlyMention |
| `dataset/places.csv` | 25 | closed place list with IDs, Hebrew names, Princeton coordinates/URLs |
| `dataset/relations.csv` | 212 | typed person–person relations (20-type closed vocabulary: marriage, kinship, agency, business, correspondence, rivalry…) with per-edge evidence |
| `dataset/edges_coappearance.csv` | 1,358 | weighted person–person edges (joint presence in a legal act) |
| `dataset/princeton_people_matches.csv` | 25 | full Princeton Geniza Lab record for every matched person |
| `dataset/validation_report.csv` | — | counts, closed-list enforcement, possible-duplicate groups for manual review |
| `dataset/Karaite_Geniza_Database.xlsx` | — | all of the above as one Excel workbook (11 tabs) |

### Conventions

- **Certainty levels** on every appearance: `attested` (named in the document),
  `reconstructed` (editorial reconstruction), `contextual` (known only from the editors'
  commentary — mapped to the action `ScholarlyMention`).
- **Sect** is a closed list: Karaite / Karaite (probable) / Karaite (presumed) /
  Rabbanite / Rabbanite (probable) / unknown. *Presumed* is a default assumption for
  participants in Karaite legal documents, not evidence; every explicit identification
  carries a written `sect_evidence`.
- **Descent counts as evidence.** A child of a person who is identified explicitly is
  identified explicitly too, with the parent named in `sect_evidence`. The corpus contains
  no parent and child of different sects, so membership of a named family — Tustari,
  Sahlawaya, al-ʿAnī, ben Zita, the *nesiʾim* — is a documented fact rather than an
  inference. This rule was already applied to sons (`son of Sahlawaya`) and to some
  daughters (`daughter of the nasi Hizkiyahu`); as of the current version it is applied
  consistently, which moved four brides (Sara bt. Yeshaʿya, Sara bt. Sahlawaya, Husn bt.
  Hayyim, Fadla bt. Abraham) from *presumed* to explicit. Note the residual imbalance it
  does not fix: 32% of the men in the corpus carry an explicit identification against 23%
  of the women, because the documents themselves say far less about brides than about
  the witnesses, scribes and fathers who transact around them.
- **Identity merging** across documents/name-forms follows the editors' explicit
  identifications only (e.g. the Arabic/Hebrew doublet Daoud/David; David b. Yeshaʿya
  the scholar between TS 18 J 5.10 and Mosseri Ia.2). Unmerged same-name candidates
  are listed in the validation report.

## The paper

**`docs/עבודה_רשתות_קראים.docx`** — *מי החזיק את הקהילה הקראית יחד? ניתוח רשתות חברתיות של
מסמכים משפטיים קראיים מגניזת קהיר* — the seminar paper (Hebrew, RTL, 9 pp.).
An earlier English version is kept as `docs/Karaite_SNA_Paper.docx`.
Centrality measures: degree, betweenness, closeness, eigenvector and PageRank, plus Louvain
communities. Its findings: the corpus is held together by **judicial** institutions rather than
kinship (the reigning *nasi* and a handful of professional witnesses hold the highest
brokerage scores); elite marriage strategy is legible as graph structure (one betrothal
fuses the *nesiʾim* and Tustari lineages); and Karaite–Rabbanite contact is routine —
a quarter of the documents involve an identified Rabbanite — concentrated in shared courts
and in the scribal profession.

## RDF

`rdf/karaite_geniza.ttl` (+ RDF/XML) — **17,725 triples**, validated with rdflib.
The model follows the event/role pattern of factoid prosopography: an **Appearance** is a
first-class resource linking a Person, a Document and an Action from the closed vocabulary,
and carrying its evidential certainty, so that historical uncertainty stays machine-readable.
Reuses FOAF, Dublin Core, SKOS, WGS84 and PROV-O; `owl:sameAs` links to the Princeton
Geniza Lab. Relations and co-appearance edges are reified as `rdf:Statement` so each carries
its evidence and derivation. Example query — every document in which a Rabbanite appears:

```sparql
SELECT ?doc ?name WHERE {
  ?a kg:inDocument ?doc ; kg:byPerson ?p .
  ?p foaf:name ?name ; kg:hasSect sect:Rabbanite . }
```

## Pipeline

```
extraction/extract_texts.py      pdftotext + split the edition into per-document files
        │                        (requires the source PDFs; output is git-ignored)
        ▼
src/data_docs.py                 ┐
src/data_appearances.py          │  hand-curated harvest layers (the actual data entry,
src/data_persons_relations.py    │  with per-row evidence notes)
src/data_extra.py                │
src/data_places_actions.py       ┘  closed vocabularies: places, actions, relation types
        ▼
src/build_dataset2.py            builds dataset/ (CSVs + Excel workbook + validation)
        ├──► src/build_rdf.py    builds rdf/ (Turtle + RDF/XML, validated, SPARQL-checked)
        ├──► src/analyze_v2.py   5 weighted networks: degree, betweenness, eigenvector,
        │                        PageRank, Louvain; PNG figures + interactive HTML
        └──► src/make_paper_he.js  builds the Hebrew paper from the live results
             src/make_paper.js     builds the English version
```

Run:

```bash
pip install -r requirements.txt
cd src
python3 build_dataset2.py     # dataset/  (CSVs + Excel + validation report)
python3 build_rdf.py          # rdf/      (Turtle + RDF/XML)
python3 analyze_v2.py         # networks/ (metrics, figures, interactive HTML, full-size plates)
npm install docx
node make_paper_he.js         # docs/עבודה_רשתות_קראים.docx   (Hebrew, the submitted paper)
node make_paper.js            # docs/Karaite_SNA_Paper.docx    (English version)
```

## Networks

| network | nodes | edges | what it shows |
|---|---|---|---|
| N1 co-appearance (all persons) | 275 | 1,358 | modular (Q=0.874); giant component of 66 fused by court personnel |
| N1g giant component | 66 | 405 | brokers: ʿAlan b. Naḥum, the *nasi* David b. Ṣemaḥ, Elʿazar b. Samuel |
| N2 bipartite person–document | 286 | 258 | which documents carry the network (court copies over-represented) |
| N3 kinship / marriage / agency | 204 | 180 | 45 families; largest (32) = *nesiʾim* × Tustari via one betrothal |
| N4 Karaite–Rabbanite contact | 118 | 145 | 107 direct cross-sect edges in 15 of 60 source units |
| N5 attestation (witnesses/scribes) | 138 | 526 | a Palestinian and an Egyptian block of professional signatories |
| N6 ketubbot only | 178 | 838 | 28 marriage contracts; sparse, run by witnesses and scribes |
| N6b betrothals only | 96 | 490 | 13 deeds; twice as dense, dominated by the *nasi* — the court's business |

### Figures

The figures printed in the paper are close-ups: a page is roughly 16 cm wide, and a
network of a few hundred people split into dozens of components cannot be drawn
legibly at that width. `networks/full/` therefore holds every network whole, at
6000 x 4200 pixels with all node labels, for reading on screen; `networks/*.html`
holds the interactive versions, with per-node metrics on hover.

To add a new Geniza fragment: add one row in `data_docs.py`, its appearances in
`data_appearances.py` (and relations/sect entries if relevant), then rebuild.

## Repository layout

```
extraction/     PDF-to-text extraction code (step 1)
src/            curated data layers + build, RDF, analysis and paper scripts
data/external/  Princeton Geniza Lab exports (people, places)
dataset/        the built database (CSVs + Excel) — shelfmark identifiers
rdf/            karaite_geniza.ttl / .rdf — 17,725 triples
networks/       figures (PNG), interactive views (HTML), per-node metrics, summary JSON
networks/full/  the same networks whole, at plate size, every node named (see its README)
docs/           the seminar paper + the earlier work plan & report (docx)
```

## Status / roadmap

- [x] Harvest of both sources incl. commentaries and footnotes; validation scan
- [x] v2 database: person IDs & merges, closed place/action/relation vocabularies,
      Princeton Geniza Lab integration, shelfmark identifiers
- [x] Five networks on the v2 schema; centralities, Louvain communities, figures
- [x] RDF export with an event/role ontology, validated and SPARQL-queryable
- [x] Seminar paper (10 pp.): SNA results vs. the historiography of Karaite–Rabbanite relations
- [ ] Corpus expansion: further mixed contracts (TS 8.223, TS 24.1, TS Misc. 35.13,
      Antonin 637), Karaite divorce deeds, Rabbanite court records involving Karaites
- [ ] Temporal slicing by half-century; comparative Rabbanite baseline corpus

## Attribution & licensing

- The **database structure and code** are released under the MIT license (see `LICENSE`).
- The **harvested facts** derive from the copyrighted editions of Olszowy-Schlanger (1998)
  and Zinger (2017); the dataset records facts (names, roles, dates) with source
  references, for academic research. Please cite both works in any use of this data.
- The files in `data/external/` are exports from the **Princeton Geniza Lab**
  (https://geniza.princeton.edu); credit PGP when using them.
