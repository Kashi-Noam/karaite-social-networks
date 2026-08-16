# Full size plates

The paper prints close-ups. A page is about 16 cm wide, and a fragmented network
of a few hundred people cannot be drawn legibly at that width: either the labels
shrink below reading size or most of them have to be dropped. The figures in the
paper therefore show the part of each network under discussion.

This folder holds the same networks whole, at 6000 x 4200 pixels, with every
node named. They are meant to be opened and zoomed, not printed. Components are
laid out one per cell and packed onto shelves, so a person's neighbourhood stays
together and the isolated pairs at the edge of the corpus remain visible.

| plate | file | what it shows |
|---|---|---|
| 1 | `N1_coappearance_all.png` | co-appearance of all 275 persons, every component |
| 2 | `N1_giant.png` | the giant component, 66 persons, the core of the corpus |
| 3 | `N2_person_document.png` | bipartite network of persons and documents |
| 4 | `N3_kinship.png` | kinship, marriage and agency, all 45 family components |
| 5 | `N4_cross_sect.png` | Karaite–Rabbanite contact, all components |
| 6 | `N5_attestation.png` | witnesses and scribes, all components |
| 7 | `N6_ketubbot.png` | ketubbot only |
| 8 | `N6_betrothals.png` | deeds of betrothal only |
| 9 | `N7_document_network.png` | documents joined by the persons they share |

Node colour is sect, node size is PageRank within that network, and edge width is
the number of documents two people share. Names are in Latin transcription, as in
`dataset/persons.csv`; the `person_id` column there links a name to everything
else recorded about that person.

For panning, filtering and per-node metrics on screen, the interactive versions in
the parent folder (`N1_coappearance.html` and the rest) are easier to work with.
Regenerate everything with `cd src && python3 analyze_v2.py`.
