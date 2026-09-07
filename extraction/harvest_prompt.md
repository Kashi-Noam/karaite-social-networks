# The harvesting prompt

The prosopographic data in `dataset/` was extracted from the two source
publications with a large language model (Claude, Fable 5). Each document's
full text — the English description, translation, textual notes and the
editor's commentary — was fed to the model together with the prompt below.
This is the final version, the one the shipped dataset was built with; the
paper's appendix A prints the same text.

The prompt went through three revisions. The first run on a small sample
showed two recurring failures: the model merged two people with similar names
into one, and it recorded a person known only from the commentary as if he
were named in the document. The rules section below is what fixed them, and
the three-level `certainty` field is what makes the second failure detectable
after the fact rather than invisible.

```
You are extracting prosopographic data from a scholarly edition of a
Karaite marriage document from the Cairo Geniza.

INPUT: the English description, translation, textual notes and the
editor's commentary for one document.

EXTRACT:
  shelfmark, document type, date, place
  every named person, with the role he or she performs

ROLES - use ONLY these values:
  Groom, Bride, GroomFather, BrideFather, BrideGrandfather,
  GroomGrandfather, Agent, GroomAgent, WitnessOfAgency, Witness,
  Scribe, Nasi, Judge, Trustee, Guarantor, Party, Declarant, Mentioned

FOR EVERY PERSON record a certainty value:
  attested      - the person is named in the document itself
  reconstructed - the editor reconstructs the name
  contextual    - the person appears only in the commentary

RULES:
  - quote the passage each item is taken from
  - do NOT merge two similar names into one person unless the
    editor states the identification explicitly
  - do NOT infer a sect; record only what the editor states
  - a person named in a genealogy ('son of X') is recorded with the
    role that names him, not as a participant
  - leave a field empty rather than guessing
```

## From the 18 roles to the 15 actions

The prompt's role list is a *reading* vocabulary: it names what the document
calls someone. `dataset/actions.csv` is an *analytical* vocabulary: it says
what that person did, and which class of act it was. `src/data_appearances.py`
holds the mapping. Two steps in it carry weight for the analysis:

- **`Nasi` → `NamedNasi`, class `Reference`.** The reigning nasi is named in
  the dating clause of the deed. He is not a participant, and putting him in
  the `Court` class instead would make a formulaic line look like an act. The
  paper's Table 3 shows exactly how much difference this one decision makes.
- **`Mentioned` splits three ways** — `FamilyMention` (a father in a party's
  genealogy), `DocumentMention` (named in passing in the text) and
  `ScholarlyMention` (known only from the editors' commentary) — because only
  the split makes it possible to separate what the document says from what the
  editors reconstruct. All three are in the `Reference` class.

Everything in the `Reference` class is excluded from every network in the
paper. See the rule stated at the top of `src/backbone.py`.

## What was checked by hand

About a fifth of the documents were checked line by line against the printed
book, including every document that later turned out to be structurally
important. In addition, an automatic scan matched every "X b. Y" string in the
full text against the harvested person list; it surfaced roughly thirty-five
people who appear only in the commentary and footnotes and had been missed,
including Efraim b. Shemarya and the gaon Solomon b. Judah, and all were added.

Two further errors of a different kind were found later, in the assembled
database rather than in the reading, and both are fixed in the current data:
a rule that marked anyone recorded as "the bride's side" as female, which
mislabelled ten fathers; and a groom recorded as a witness to the appointment
of his own bride's agent, where the source says only that he was present.
