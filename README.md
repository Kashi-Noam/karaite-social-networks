# Karaite Social Networks from the Cairo Geniza

A prosopographic database and Social Network Analysis (SNA) of the medieval Karaite
community of Egypt and Palestine (10th–13th centuries), built from Cairo Geniza legal
documents. Seminar project for the course **"Karaite Jews in the Middle East"**
(Hebrew University of Jerusalem).

מאגר פרוסופוגרפי וניתוח רשתות חברתיות של הקהילה הקראית במזרח התיכון בימי הביניים,
על בסיס מסמכים משפטיים מגניזת קהיר.

## Sources

The data were harvested document by document — including the editors' introductions,
commentaries and footnotes — with a large language model (Claude, Fable 5), and then
checked against the printed book by hand. `extraction/harvest_prompt.md` holds the
prompt, the mapping from its 18 roles to the 15 actions in `dataset/actions.csv`, and
an account of what the manual check caught. The sources are:

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

**`docs/מי החזיק את הקהילה הקראית יחד - v7.docx`** — *מי החזיק את הקהילה הקראית יחד? ניתוח רשתות חברתיות של
מסמכים משפטיים קראיים מגניזת קהיר* — the seminar paper (Hebrew, RTL).
Centrality measures: degree, betweenness, closeness, eigenvector and PageRank, plus
Louvain communities (seeded, so the partition is reproducible).

**The one filter rule.** An edge means *these two people were present at the same legal
act*, so an appearance enters a network only if its action class is not `Reference` —
which excludes the nasi named in the dating clause, fathers named in genealogies, people
named in passing, and everyone known only from the editors' commentary. Every network in
the paper obeys this rule; two derived networks (with the nasi clause restored, and with
the editors' reconstructions dropped) are reported beside it. The rule is stated in full
at the top of `src/backbone.py`.

Its findings, in the order the paper makes them:

- The corpus is **far thinner than it looks**. Of the 238 people present at a documented
  legal act, 226 appear in a single document; 12 appear in two, none in three. Of 1026
  edges only 3 rest on more than one document, and all three join the same couple,
  whose wedding was written up twice. There is no repeated tie between two people
  anywhere in the corpus.
- That thinness is a **sampling result, not a social one**. Drawing the observed cast
  sizes at random from a pool of N adult men reproduces the observed number of repeaters
  at N ≈ 2,301 for the whole corpus and N ≈ 962 for Fustat 1030–1074; Chao1 agrees.
- The largest component that **co-presence** holds together is Palestinian (53 people,
  4 documents) and rests on three men: two signing witnesses and one scribe. Restore the
  formulaic dating clause and the largest component becomes Egyptian (59 people, 8
  Fustat deeds that share no participant at all) with the nasi as its top broker. The
  "giant component" of the Egyptian corpus is an artefact of a dating formula.
- The recurring signatories are not men without standing: **35.9% of signing witnesses
  and 66.7% of scribes are a ha-Kohen or a ha-Levi**, against 17.9% of everyone in the
  database and 9.1% of grooms. In 14 of the 15 documents with three or more attesters at
  least one carries the title.
- The **number of attesters is regional**: median 12 in the five Palestinian documents
  against 5.0 in the eighteen Egyptian ones, which qualifies the usual explanation of the
  many signatures by Anan's requirement of "ten of the people of the place".
- Ketubbot and deeds of betrothal differ in **composition, not in size**: the apparent
  size gap disappears once fragments are excluded (8.21 vs 8.2 named per undamaged
  document), while the gap in witnesses of the agency survives (1.07 vs 1.9) and both
  acting judges in the corpus sit in deeds of betrothal.
- Karaite–Rabbanite contact is **routine and internal**: a Rabbanite is present in 10 of
  the 44 documents that name anyone, those documents are the ones that preserve the most
  names (9.0 names on average against 4.94), and no Rabbanite bridges two Karaite clusters.
  The stronger evidence is elsewhere in the data: the same recurring signatories also
  sign Karaite divorces and deeds of release, and two sit in a Rabbanite court
  (`attested_outside_corpus` in `dataset/persons.csv`).
- Women are a **property of the genre**: 35 women in the network, all brides bar one
  legal party, 0 woman-to-woman edges out of 1026, and 36 of the documents name exactly
  one woman. In the kinship network the picture inverts — 29 of 36 women carry positive
  betweenness against 60 of 168 men.

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
        ├──► src/analyze_v2.py   exploratory networks: centralities, Louvain, metrics
        │                        CSVs, interactive HTML, full-size plates
        └──► src/backbone.py     EVERY number the paper cites -> networks/paper_numbers.json
             src/figures.py      EVERY figure the paper prints -> figures/
             src/make_paper_v7.js  builds the paper from those two, and nothing else
                                   (and calls src/fix_docx.py on the result)
```

Run:

```bash
pip install -r requirements.txt
cd src
python3 build_dataset2.py     # dataset/  (CSVs + Excel + validation report)
python3 build_rdf.py          # rdf/      (Turtle + RDF/XML)
python3 analyze_v2.py         # networks/ (metrics, interactive HTML, full-size plates)
python3 backbone.py           # networks/paper_numbers.json  — every number in the paper
python3 figures.py            # figures/                     — every figure in the paper
npm install docx
node make_paper_v7.js         # docs/מי החזיק את הקהילה הקראית יחד - v7.docx
```

`make_paper_v7.js` finishes by running `fix_docx.py` on the file it wrote. docx-js
produces two constructs Word refuses to open: every image carries the same drawing id,
and the page-number field is packed into a single run instead of one run per field
character. LibreOffice reads both, so converting to PDF does not catch them; Word
answers with "Word found unreadable content". The script repairs both in place.

## Networks

| network | nodes | edges | what it shows |
|---|---|---|---|
| presence (the paper's N1) | 238 | 1026 | 31 components; largest is Palestinian (53 people, 4 documents) |
| presence + the nasi clause | 242 | 1060 | largest becomes Egyptian (59 people, 8 Fustat deeds sharing no participant) |
| attested only | 234 | 1003 | the same, with the editors' reconstructions dropped: unchanged conclusions |
| kinship / marriage / agency | 204 | 179 | 45 families; largest (32) = nesi'im × Tustari via one betrothal |
| attestation (witnesses, scribes) | 136 | 525 | the recurring signatories and the two regional blocks |
| Karaite–Rabbanite contact | 88 | 96 | 72 cross-sect ties, every one internal to a single document |

`src/analyze_v2.py` also writes `N4_cross_sect_with_commentary`, which adds the ties the
editors reconstruct in their prose (rivalry, correspondence, patronage). It is kept
separate on purpose: a claim resting on it is a claim about the historiography, not
about the documents.

### Figures

`figures/` holds the ten figures the paper prints, all written by `src/figures.py` from
the dataset and `networks/paper_numbers.json`, in one visual system. Captions live in the
paper, so nothing in the images is set in Hebrew.

`networks/full/` holds the exploratory networks whole, at plate size with every node
labelled, for reading on screen; `networks/*.html` holds the interactive versions with
per-node metrics on hover.

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
- [x] One stated filter rule applied to every network; the nasi-clause comparison as
      the robustness test
- [x] `src/backbone.py` + `src/figures.py`: every number and every figure in the paper
      reproducible in one run
- [x] `attested_outside_corpus`: signatories tracked into Karaite divorces, deeds of
      release and a Rabbanite court
- [ ] Corpus expansion: further mixed contracts (TS 8.223, TS 24.1, TS Misc. 35.13,
      Antonin 637), the Karaite divorce deeds and deeds of release already referenced in
      `attested_outside_corpus`, Rabbanite court records involving Karaites
- [ ] Comparative Rabbanite baseline corpus — the one test that would show whether the
      share of Kohanim and Levites among signatories is Karaite or simply Genizan

## Attribution & licensing

- The **database structure and code** are released under the MIT license (see `LICENSE`).
- The **harvested facts** derive from the copyrighted editions of Olszowy-Schlanger (1998)
  and Zinger (2017); the dataset records facts (names, roles, dates) with source
  references, for academic research. Please cite both works in any use of this data.
- The files in `data/external/` are exports from the **Princeton Geniza Lab**
  (https://geniza.princeton.edu); credit PGP when using them.
