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
- **Identity merging** across documents/name-forms follows the editors' explicit
  identifications only (e.g. the Arabic/Hebrew doublet Daoud/David; David b. Yeshaʿya
  the scholar between TS 18 J 5.10 and Mosseri Ia.2). Unmerged same-name candidates
  are listed in the validation report.

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
        ▼
src/analyze_networks.py          SNA phase (v1; being rebuilt on the v2 schema):
                                 5 weighted networks, centrality algorithms, Louvain
                                 communities, interactive HTML + PNG visualizations
```

Run:

```bash
pip install -r requirements.txt
cd src && python3 build_dataset2.py     # rebuilds dataset/ from the curated layers
```

To add a new Geniza fragment: add one row in `data_docs.py`, its appearances in
`data_appearances.py` (and relations/sect entries if relevant), then rebuild.

## Repository layout

```
extraction/     PDF-to-text extraction code (step 1)
src/            curated data layers + build & analysis scripts
data/external/  Princeton Geniza Lab exports (people, places)
dataset/        the built database (CSVs + Excel) — v2, shelfmark identifiers
networks/       v1 network outputs (PNG, interactive HTML, per-node metrics)
docs/           work plan & analysis report (docx)
```

## Status / roadmap

- [x] Harvest of both sources incl. commentaries and footnotes; validation scan
- [x] v2 database: person IDs & merges, closed place/action/relation vocabularies,
      Princeton Geniza Lab integration, shelfmark identifiers
- [ ] Rebuild the five networks on the v2 schema (weighted, typed by action)
- [ ] RDF export (persons, documents, places, actions as predicates)
- [ ] Final seminar paper: SNA results vs. the historiography of Karaite–Rabbanite relations

## Attribution & licensing

- The **database structure and code** are released under the MIT license (see `LICENSE`).
- The **harvested facts** derive from the copyrighted editions of Olszowy-Schlanger (1998)
  and Zinger (2017); the dataset records facts (names, roles, dates) with source
  references, for academic research. Please cite both works in any use of this data.
- The files in `data/external/` are exports from the **Princeton Geniza Lab**
  (https://geniza.princeton.edu); credit PGP when using them.
