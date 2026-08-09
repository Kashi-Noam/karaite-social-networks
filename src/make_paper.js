const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, PageBreak,
  Footer, PageNumber, BorderStyle
} = require("docx");

const NET = "../networks/";
const B = (t,o={}) => new TextRun({text:t, bold:true, ...o});
const T = (t,o={}) => new TextRun({text:t, ...o});
const I = (t,o={}) => new TextRun({text:t, italics:true, ...o});
const P = (c,o={}) => new Paragraph({children:Array.isArray(c)?c:[T(c)], spacing:{after:95,line:258}, alignment:AlignmentType.JUSTIFIED, ...o});
const H1 = t => new Paragraph({text:t, heading:HeadingLevel.HEADING_1, spacing:{before:250,after:130}});
const H2 = t => new Paragraph({text:t, heading:HeadingLevel.HEADING_2, spacing:{before:240,after:120}});

const img = (file, w, h, caption) => [
  new Paragraph({children:[new ImageRun({type:"png", data:fs.readFileSync(NET+file), transformation:{width:w,height:h}})],
                 alignment:AlignmentType.CENTER, spacing:{before:120,after:60}}),
  new Paragraph({children:[T(caption,{size:17,italics:true})], alignment:AlignmentType.CENTER, spacing:{after:140}})
];

function tbl(headers, rows, widths){
  const total = widths.reduce((a,b)=>a+b,0);
  return new Table({
    columnWidths:widths, width:{size:total,type:WidthType.DXA},
    rows:[
      new TableRow({tableHeader:true, children:headers.map((h,i)=>new TableCell({
        width:{size:widths[i],type:WidthType.DXA},
        shading:{type:ShadingType.CLEAR, fill:"E8EEF7"},
        children:[new Paragraph({children:[B(h,{size:17})],spacing:{after:30}})]}))}),
      ...rows.map(r=>new TableRow({children:r.map((c,i)=>new TableCell({
        width:{size:widths[i],type:WidthType.DXA},
        children:[new Paragraph({children:[T(String(c),{size:17})],spacing:{after:30}})]}))}))
    ]});
}

const numbering = {config:[
  {reference:"b", levels:[{level:0, format:LevelFormat.BULLET, text:"•", alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:460,hanging:230}}}}]},
  {reference:"n", levels:[{level:0, format:LevelFormat.DECIMAL, text:"%1.", alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:460,hanging:280}}}}]}]};
const BUL = c => new Paragraph({children:Array.isArray(c)?c:[T(c)], numbering:{reference:"b",level:0}, spacing:{after:65}, alignment:AlignmentType.JUSTIFIED});
const NUM = c => new Paragraph({children:Array.isArray(c)?c:[T(c)], numbering:{reference:"n",level:0}, spacing:{after:65}, alignment:AlignmentType.JUSTIFIED});
const REF = c => new Paragraph({children:Array.isArray(c)?c:[T(c)], spacing:{after:55}, indent:{left:420,hanging:420}});
const CODE = t => new Paragraph({children:[T(t,{font:"Consolas",size:15})], spacing:{after:20}, indent:{left:280},
  shading:{type:ShadingType.CLEAR, fill:"F4F4F4"}});

const children = [
  // ---------------- title
  new Paragraph({children:[B("Who Held the Karaite Community Together?",{size:36})], alignment:AlignmentType.CENTER, spacing:{before:380,after:80}}),
  new Paragraph({children:[T("A Social Network Analysis of Karaite Legal Documents from the Cairo Geniza",{size:26,color:"333333"})], alignment:AlignmentType.CENTER, spacing:{after:220}}),
  new Paragraph({children:[T("Noam Kashi",{size:22})], alignment:AlignmentType.CENTER, spacing:{after:40}}),
  new Paragraph({children:[T("Seminar paper, “Karaite Jews in the Middle East”, The Hebrew University of Jerusalem",{size:19,color:"555555"})], alignment:AlignmentType.CENTER, spacing:{after:300}}),

  new Paragraph({children:[B("Abstract. ",{size:19}), T("This paper applies Social Network Analysis (SNA) to the corpus of Karaite legal documents from the Cairo Geniza. From the fifty-seven marriage documents edited by Judith Olszowy-Schlanger, from the record of a joint Karaite–Rabbanite court session published by Oded Zinger, and from the editors’ commentaries, I built a documented prosopographic database of 350 individuals, 390 attested appearances and 212 typed interpersonal relations, published as CSV, as an Excel workbook and as an RDF/Turtle graph of some 17,700 triples. Five weighted networks derived from this database are analysed with degree, betweenness, eigenvector and PageRank centralities and with Louvain community detection. Three findings emerge. First, the structural core of the corpus is judicial rather than familial: the reigning ",{size:19}), I("nasi",{size:19}), T(" and a handful of recurring professional witnesses hold the highest brokerage scores, and the network’s giant component is assembled out of court copies and court-certified deeds. Second, elite marriage strategy is legible as graph structure: a single betrothal fuses the two largest family trees in the corpus, the ",{size:19}), I("nesi’im",{size:19}), T(" dynasty and the Tustari banking family. Third, Karaite–Rabbanite contact is routine rather than marginal — a quarter of the documents involve an identified Rabbanite — and it concentrates in shared courts and in the scribal profession, supporting the revisionist historiography of Rustow and Zinger.",{size:19})], alignment:AlignmentType.JUSTIFIED, spacing:{after:240}}),
  new Paragraph({children:[new PageBreak()]}),

  // ---------------- 1
  H1("1. Introduction"),
  P([T("The Karaite communities of Fatimid Egypt and Palestine are among the best-documented Jewish minorities of the medieval Islamic world, yet their social structure is usually described qualitatively: an aristocratic dynasty of "), I("nesi’im"), T(" descended from ‘Anan ben David, wealthy courtier-bankers such as the Tustaris, a scholarly centre in Jerusalem, and a shifting, contested boundary with the Rabbanite majority. The Cairo Geniza preserves the raw material for a more precise account. Karaite marriage documents name not only the couple but the bride’s agent, the witnesses to his appointment, the signing witnesses, the scribe, and the reigning "), I("nasi"), T(" — a dense record of who stood beside whom in a legally binding act.")]),
  P([T("This paper asks a structural question of that material: "), I("which individuals actually held the Karaite community together?"), T(" Rather than reading each document as an isolated event, I treat the corpus as a single network in which persons are nodes and joint participation in a legal act is an edge. The method makes visible what close reading cannot easily quantify — who recurs across documents, who bridges otherwise unconnected families and cities, and where the Karaite and Rabbanite worlds actually touch.")]),
  P([T("Three research questions organise the analysis. (1) Is the corpus held together by kinship or by legal institutions? (2) Does the marriage strategy of the Karaite elite have a visible structural signature? (3) How frequent, and of what kind, is Karaite–Rabbanite contact in the legal sphere? Section 2 describes the sources and the technical extraction; section 3 the methodology and its scholarly context; section 4 the RDF representation; section 5 the five networks and their analysis; section 6 concludes with limitations and next steps.")]),

  // ---------------- 2
  H1("2. Sources and Data Extraction"),
  P([T("The database rests on two published editions. The primary source is Judith Olszowy-Schlanger’s "), I("Karaite Marriage Documents from the Cairo Geniza"), T(" (1998), which edits fifty-seven documents written between "), T("c."), T(" 984 and 1201: deeds of betrothal, "), I("ketubbot"), T(", court copies, blank formularies, and two mixed Karaite–Rabbanite contracts drawn up according to the Karaite formula. Each document is presented with a Hebrew transcription, an English translation, textual notes and a historical commentary. The second source is Oded Zinger’s edition of a joint Karaite–Rabbanite court session held in Fustat on 13 July 1055, in which the Rabbanite judge ‘Eli b. ‘Amram and a group of Rabbanite elders convened at the "), I("majlis"), T(" of the Karaite "), I("nasi"), T(" Josiah b. Solomon to adjudicate an inheritance (Zinger 2017).")]),
  P([B("Extraction. "), T("Both PDFs were converted to layout-preserving text with "), T("pdftotext",{font:"Consolas",size:19}), T(", and the edition section of the book was segmented programmatically into fifty-seven per-document files. The Hebrew transcription blocks were stripped: the volume is a scan whose OCR renders Hebrew as noise, so the reliable text is the English translation, the notes and the commentary. All extraction code is published with this project ("), T("extraction/extract_texts.py",{font:"Consolas",size:19}), T("); the source PDFs are not redistributed.")]),
  P([B("Harvesting. "), T("Data entry itself was manual and document-by-document. For every document I recorded the shelfmark, type, date, place, and every named person with the role he or she performs. Crucially, the editors’ "), B("commentaries were harvested as a source in their own right"), T(": they identify the same individual across documents, supply sect identifications, reconstruct family links, and connect the corpus to the wider Geniza. A systematic name-scan of the full text against the captured data recovered a further thirty-five individuals mentioned only in commentary and footnotes — among them Efraim b. Shemarya, the Gaon Solomon b. Jehuda, the first generation of the Tustari family and its banking correspondents in Baghdad and Damascus.")]),
  P([B("Standardisation. "), T("Every appearance carries an explicit certainty value: "), I("attested"), T(" (named in the document), "), I("reconstructed"), T(" (editorial reconstruction), or "), I("contextual"), T(" (known only from the editors’ commentary). Sect identification is a closed vocabulary in which “Karaite (presumed)” marks the default assumption for a participant in a Karaite deed, while every explicit identification carries a written evidence note. Places were normalised to a closed list of twenty-five entries with stable IDs, so that “Fustat” and “Fustat [?]” became one place plus a separate certainty column; fifteen places and twenty-five persons were matched to the Princeton Geniza Lab authority lists, adding coordinates, dates and external URIs. Persons received unique identifiers, and were merged across name-forms only where an editor makes the identification explicitly; unmerged same-name candidates are listed in a validation report for manual review.")]),
  P([B("Resulting database. "), T("60 source units (58 documents plus two chapter-level prosopographic units), 350 persons, 390 appearances, 212 typed relations and 1,358 weighted co-appearance edges. Documents are identified by shelfmark, e.g. "), T("TS 24.13",{font:"Consolas",size:19}), T(" or "), T("Mosseri VII.43 + TS Ar.53.53",{font:"Consolas",size:19}), T(".")]),

  // ---------------- 3
  H1("3. Methodology"),
  P([T("Social Network Analysis has an established place in Geniza and in medieval Jewish studies. Goitein’s "), I("A Mediterranean Society"), T(" (1967–1993) is in effect a prosopography assembled by hand, and its judgements about “who mattered” are network claims without a graph. Explicit quantitative work followed: Goldberg (2012) reconstructed the trading network of the eleventh-century Maghribi merchants, and Rustow (2008) rewrote Karaite–Rabbanite relations as a question of patronage ties rather than sectarian boundaries. Beyond the Geniza, SNA has become standard in medieval prosopography — Padgett and Ansell’s (1993) analysis of Medici marriage and business ties is the canonical demonstration that a political outcome can be explained by network position, and Preiser-Kapeller (2015) and the "), I("People of Medieval Scotland"), T(" project show how a document corpus becomes a queryable graph.")]),
  P([T("Two methodological commitments follow from the nature of the evidence. First, "), B("an edge must correspond to a documented act"), T(". I therefore build the primary network from co-appearance in the same legal document — a conservative operationalisation of Mullett’s point that medieval social ties are visible only through the acts that record them. Contextual and purely genealogical mentions are excluded from that network and analysed separately. Second, "), B("uncertainty must stay in the data"), T(", not be silently resolved: certainty levels, sect evidence and merge decisions are all machine-readable columns, so any conclusion can be recomputed under stricter assumptions.")]),
  P([B("Actions as a typed vocabulary. "), T("Each appearance is classified with one of fifteen closed “actions”: Groom, Bride, LegalParty, Guarantor, Agent, WitnessOfAgency, Witness, Scribe, Declarant, Judge, Trustee, NamedNasi, FamilyMention, DocumentMention, ScholarlyMention. The vocabulary is deliberately precise enough to distinguish a witness of agency from a signing witness, and general enough to apply across document types — which lets the same annotation drive both the network typing and the RDF predicates.")]),
  P([B("Algorithms. "), T("All networks are weighted and undirected, weight being the number of shared documents. I compute degree and weighted degree (activity), betweenness centrality with edge length 1/weight (brokerage between otherwise disconnected groups; Freeman 1977), eigenvector centrality and PageRank (embeddedness in a well-connected neighbourhood), and Louvain community detection (Blondel et al. 2008) with modularity as a measure of partition quality. Computations use NetworkX (Hagberg et al. 2008).")]),

  // ---------------- 4
  H1("4. RDF Representation"),
  P([T("The database is published as an RDF graph so that it can be queried, extended and linked to other projects rather than merely read. The design follows the event/role pattern familiar from CIDOC-CRM and from factoid prosopography (Bradley and Short 2005): rather than asserting a direct “X witnessed Y”, the model makes the "), B("appearance"), T(" a first-class resource connecting a person, a document and an action, and carrying its evidential certainty. This keeps the historian’s uncertainty inside the graph. Existing vocabularies are reused where possible — FOAF for persons, Dublin Core for document metadata, SKOS for the closed vocabularies, WGS84 for coordinates, "), T("owl:sameAs",{font:"Consolas",size:19}), T(" for Princeton Geniza Lab identifiers — with project-specific terms in a "), T("kg:",{font:"Consolas",size:19}), T(" namespace. Relations and co-appearance edges are additionally reified as "), T("rdf:Statement",{font:"Consolas",size:19}), T(" resources so that each carries its evidence and its derivation (explicit vs. inferred from roles).")]),
  P("A single appearance is expressed as:"),
  CODE("app:P069_TS_24_13_ACT07_ab12f4  a kg:Appearance ;"),
  CODE("    kg:byPerson        kgp:P069 ;"),
  CODE("    kg:inDocument      doc:TS_24_13 ;"),
  CODE("    kg:performedAction act:ACT07 ;      # Witness / עד חותם"),
  CODE("    kg:certainty       \"attested\" ."),
  P([T("The resulting file contains "), B("17,725 triples"), T(" and validates under rdflib. Because the actions are SKOS concepts and the relations are typed properties, whole networks can be reconstructed in SPARQL — for instance, all persons who ever acted as a bride’s agent, or every document in which a Rabbanite appears:")], {spacing:{before:150}}),
  CODE("SELECT ?doc ?name WHERE {"),
  CODE("  ?a kg:inDocument ?doc ; kg:byPerson ?p ."),
  CODE("  ?p foaf:name ?name ; kg:hasSect sect:Rabbanite . }"),

  // ---------------- 5
  H1("5. Networks and Analysis"),
  P([T("Five networks were derived from the same database, each answering a different question. Table 1 summarises their structural statistics.")]),
  tbl(["Network","Nodes","Edges","Components","Giant","Modularity"],
    [["N1 Co-appearance (all persons)","275","1,358","23","66","0.874"],
     ["N1g Giant component only","66","405","1","66","0.658"],
     ["N2 Bipartite person–document","286","258","30","68","—"],
     ["N3 Kinship, marriage, agency","204","180","45","32","—"],
     ["N4 Karaite–Rabbanite contact","118","145","11","—","—"],
     ["N5 Attestation (witnesses/scribes)","138","526","18","44","0.819"]],
    [3000,1000,1000,1400,1000,1400]),
  new Paragraph({children:[T("Table 1. Structural statistics of the five networks.",{size:17,italics:true})], alignment:AlignmentType.CENTER, spacing:{before:60,after:200}}),

  H2("5.1 The co-appearance network: a judicial core"),
  P([T("The full co-appearance network is extremely modular (Q = 0.874) and breaks into twenty-three components. This is the documentary signature of marriage records: each contract produces a dense clique of one event, and most events never touch. The historically meaningful object is therefore the "), B("giant component"), T(" — sixty-six people fused out of roughly a dozen separate contracts (Figure 1) — and the small set of individuals responsible for fusing them.")]),
  ...img("fig1_coappearance.png", 520, 390, "Figure 1. Giant component of the co-appearance network (66 persons). Node size = PageRank, colour = sect."),
  P([T("Within the giant component, betweenness centrality is concentrated in strikingly few hands: ‘Alan b. Naḥum (0.488), the "), I("nasi"), T(" David b. Ṣemaḥ (0.478) and El‘azar b. Samuel b. Sahl ha-‘Eved (0.343) together control almost all shortest paths. Across the corpus as a whole, the highest PageRank belongs again to David b. Ṣemaḥ (0.011), followed by the banker Sahlawaya b. Ḥayyim (0.008) and by three recurring witnesses — Yefet ha-Kohen b. ‘Eli b. Zīta, Bishr b. Abraham ha-Levi and ‘Eli b. Mu‘ammar.")]),
  P([T("The composition of that list is the paper’s first finding. Not one of the top brokers is a groom or a bride. They are a "), I("nasi"), T(" acting in his judicial capacity and a handful of professional witnesses and scribes. Olszowy-Schlanger argued from the formulae of the "), I("nasi"), T(" clause that the essential function of the "), I("nasi"), T(" was judicial — he certified deeds of attorney executed abroad (TS 16.50, Mosseri Ia.2) and presided over the Karaite court in Fustat. The network measures that function: it is precisely through his court that otherwise unrelated families become part of one social structure.")]),
  P([T("The Louvain partition of the giant component (Q = 0.658, five communities) confirms the reading: the communities are not families but "), B("document clusters bound by shared court personnel"), T(", each anchored by one or two repeat signatories.")]),

  H2("5.2 The bipartite view: which documents do the work"),
  P([T("Projecting persons and documents into a single bipartite graph (Figure 2) shows which documents carry the network. The largest are the Ramle court copy Bodl. MS Heb. a.3.4v (17 participants), the Jerusalem "), I("ketubba"), T(" CUL Add. 3430 of 1028 (15) and the Palestinian court copy TS 6 Ja 2 of 1002 (14). Two observations follow. Palestinian documents carry markedly longer witness lists than Egyptian ones, consistent with the picture of a small, dense, pious Jerusalem community; and court copies — documents produced when an original was lost or had to be certified — are over-represented among the high-degree documents. The corpus is held together by the paperwork of the court, not by the weddings themselves.")]),
  ...img("fig2_bipartite.png", 500, 375, "Figure 2. Bipartite person–document network. Green nodes are documents."),

  H2("5.3 Kinship and marriage: the structure of an elite alliance"),
  P([T("Restricting the graph to typed relations — marriage, betrothal, divorce, descent, siblingship, cousinhood and agency — produces forty-five components which are, quite literally, families (Figure 3). The largest, with thirty-two members, is the merger of the two most powerful Karaite lineages of the eleventh century: the "), I("nesi’im"), T(" dynasty running from ‘Anan b. David through David b. Bo‘az, Solomon, Ḥizqiyyahu and Josiah down to the "), I("nesi’im"), T(" of 1201, and the Tustari banking family. What fuses them is a single act: the betrothal of Yefet b. Abraham al-Tustarī to Amat al-‘Azīz, daughter of the "), I("nasi"), T(" Ḥizqiyyahu (TS 16.50, 1040s) — a document whose deed of attorney was certified, in turn, by the Karaite court of the "), I("nasi"), T(" David b. Ṣemaḥ in Fustat.")]),
  ...img("fig3_kinship.png", 515, 394, "Figure 3. Kinship, marriage and agency network (45 components)."),
  P([T("Betweenness in this network is accordingly held by the marriage brokers of the aristocracy: Ḥizqiyyahu b. Solomon (0.014), his daughter Amat al-‘Azīz (0.012) and Yefet al-Tustarī (0.011). The graph also exposes two further strategies. Cousin marriage keeps other components compact — the al-‘Ānī family of Cairo in 1004 (TS 24.7) and the family of Moses ha-Kohen b. Aaron in the 1080s (TS 24.45) both marry first cousins. And cross-sect alliance appears at the very top of society: Nasiya, daughter of the same Moses ha-Kohen, married David b. Daniel b. ‘Azarya of the Rabbanite gaonic family in 1082.")]),
  P([T("A gendered pattern is visible as well. Of 350 individuals, only 52 are women (15%), and they enter the network almost exclusively as brides. Yet the "), I("agent_for"), T(" edges show that a bride’s legal personality is real: she appoints a "), I("paqid"), T(" — usually her father, but in ten documents an unrelated notable — so that women’s edges frequently connect them to communal figures outside their own family.")]),

  H2("5.4 Karaite–Rabbanite contact"),
  P([T("Fifteen of the sixty source units — a quarter of the corpus — involve at least one identified Rabbanite, and the contact network built around them contains 107 direct Karaite–Rabbanite edges (Figure 4). The roles Rabbanites play in Karaite documents are diverse and, tellingly, unremarkable in their contexts:")]),
  BUL([B("Witnesses"), T(": Samuel bar Rabbi Moses the "), I("ḥaver"), T(" in Tyre (Mosseri Ia.2, 1051); Shela ha-Kohen bar Rabbi Mevasser (TS 20.2); Levi ha-Levi bar Jacob, known from the Rabbanite court of Fustat (ENA 4020.38v). The Aramaic "), I("bar"), T(" formula, against Karaite "), I("ben"), T(", is the editors’ diagnostic.")]),
  BUL([B("Scribe"), T(": Isaac bar ‘Azaryahu, who wrote the latest "), I("ketubba"), T(" in the corpus (TS 16.67, Cairo 1201) in a cursive Rabbanite hand.")]),
  BUL([B("Grooms"), T(": the two mixed contracts written in the Karaite formula — the remarriage of the Karaite Rayyisa to the Rabbanite Yeḥya b. Abraham (Bodl. MS Heb. a.3.42, Fustat 1117) and the betrothal of the Karaite Karīma to a Rabbanite (ENA NS 18.37, 1030s) — plus a dedicated formulary with ready-made clauses for a Karaite wife and Rabbanite husband (Bodl. MS Heb. d.66, 1036).")]),
  BUL([B("Judge and trustees"), T(": the 1055 session, in which the Rabbanite ‘Eli b. ‘Amram sits as "), I("bet din"), T(" in the Karaite "), I("nasi"), T("’s "), I("majlis"), T(", and appoints three Rabbanite trustees, among them the merchant Nahray b. Nissim.")]),
  ...img("fig4_cross_sect.png", 520, 390, "Figure 4. Karaite–Rabbanite contact network. Red = Rabbanite, blue = Karaite, grey = unknown."),
  P([T("Betweenness in this network is highest for ‘Eli b. ‘Amram (0.027), the Gaon Solomon b. Jehuda (0.026) and his rival Nathan b. Abraham (0.023) — that is, for Rabbanite leaders whose ties to Karaites are documented in the commentaries: Solomon complained about his rival’s Karaite connections, and Nathan courted the Karaite brothers Nathana’el and Berakha b. Rawḥ for support. The structural point is that Karaite–Rabbanite contact clusters in two places: where a shared court infrastructure existed (Tyre, and Fustat in 1055), and in the professional stratum of scribes and witnesses. This is the pattern Rustow (2008) predicts when sectarian identity is treated as a patronage relation rather than a boundary, and it is exactly what Zinger (2017) infers from the joint session.")]),
  P([B("A caveat with teeth. "), T("Because a Rabbanite is only counted when an editor identifies one, this measure is a strict lower bound. Rabbanites whose names lack the Aramaic marker are invisible, so the true frequency of contact can only be higher — which strengthens, rather than weakens, the conclusion.")]),

  H2("5.5 The attestation network: a professional notarial class"),
  P([T("The final network isolates the legal profession: witnesses, witnesses of agency, scribes and declarants, linked when they sign the same document (Figure 5). It has 138 nodes, 526 edges, a giant component of 44 and high modularity (0.819). Brokerage is concentrated in Bishr b. Abraham ha-Levi (0.049), ‘Eli b. Mu‘ammar (0.040) and the scribe David b. Isaac ha-Kohen (0.024).")]),
  ...img("fig5_attestation.png", 505, 379, "Figure 5. Witness, scribe and declarant co-signature network."),
  P([T("These men define two regional blocks. A "), B("Palestinian block"), T(" spans Jerusalem, Ramle and Tyre between 1002 and 1028: ‘Eli b. Mu‘ammar signs both the Palestinian court copy of 1002 and the Jerusalem "), I("ketubba"), T(" of 1028; Bishr b. Abraham ha-Levi signs that same Jerusalem document and the Ramle court copy; David b. Isaac ha-Kohen witnesses the Ramle "), I("ketubba"), T(" of 1006 and writes the Ramle court copy. An "), B("Egyptian block"), T(" covers Fustat in the 1030s–1060s, held by ‘Alan b. Naḥum, El‘azar b. Samuel b. Sahl ha-‘Eved and Yefet ha-Kohen b. ‘Eli b. Zīta. The two blocks barely touch, and the shift of density from the first to the second mirrors a documented migration: the "), I("nesi’im"), T(" Ḥizqiyyahu and Josiah left Jerusalem for Fustat in the 1050s, and the centre of Karaite institutional life moved with them.")]),
  P([T("There is a methodological corollary. It is precisely these recurring signatories that allow Olszowy-Schlanger to date undated fragments — a fragment is placed in the 1060s because El‘azar b. Samuel signed a dated contract of 1062. The property that makes a person useful to the palaeographer is the same property that makes him a high-betweenness node. The network is, in part, a formal model of the editor’s own dating logic.")]),

  // ---------------- 6
  H1("6. Conclusions, Limitations and Next Steps"),
  P([T("Three conclusions answer the questions posed at the outset. "), B("(1)"), T(" The corpus is held together by legal institutions, not by kinship: marriage documents generate isolated cliques, and it is the court — the "), I("nasi"), T(" in his judicial role, court copies, court certifications and repeat court personnel — that fuses them into a community-wide structure. "), B("(2)"), T(" Elite marriage strategy has a clear structural signature: one betrothal merges the "), I("nesi’im"), T(" and Tustari lineages into the largest family component in the corpus, while cousin marriage keeps other lineages compact. "), B("(3)"), T(" Karaite–Rabbanite contact in the legal sphere is routine, concentrated in shared courts and in the scribal profession, and its measured frequency is a lower bound.")]),
  P([B("Limitations. "), T("The Ben Ezra Geniza is a Rabbanite depository, so the surviving Karaite corpus is not a random sample; as Zinger argues, the near-absence of non-marriage Karaite legal documents may itself be historically meaningful rather than accidental. Identity merging follows the editors, whose identifications are themselves arguments. The sect default “Karaite (presumed)” is an assumption and is never used as evidence. Fragmentary documents carry an estimated year for temporal analysis, with the honest range preserved beside it. Finally, the corpus is small: centrality rankings are robust for the top few names but should not be over-read further down.")]),
  P([B("Next steps."),], {spacing:{after:60}}),
  NUM([B("Corpus expansion. "), T("Add the six further mixed contracts noted by Olszowy-Schlanger (TS 8.223, TS 24.1, TS Misc. 35.13, TS 13 J 6.33, Antonin 637), the Karaite divorce documents, and Rabbanite court records involving Karaites (TS 13 J 1.18; TS 20.187, ed. Hary and Rustow 2006). Each addition tests whether the judicial core is an artefact of the marriage corpus.")]),
  NUM([B("Temporal networks. "), T("Slice the graph by half-century to measure the Jerusalem-to-Fustat shift quantitatively rather than descriptively.")]),
  NUM([B("Linked open data. "), T("Extend the "), T("owl:sameAs",{font:"Consolas",size:19}), T(" alignment with the Princeton Geniza Project beyond the present twenty-five persons, so that the graph becomes queryable together with the far larger Rabbanite prosopography.")]),
  NUM([B("Comparative baseline. "), T("Build the equivalent network from a comparable Rabbanite marriage corpus; only a baseline can show whether the Karaite pattern — a judicial core and a thin professional stratum — is distinctively Karaite or simply what Geniza marriage documents look like.")]),

  // ---------------- bibliography
  P([B("Data and code availability. "), T("The full database (CSV and Excel), the RDF/Turtle and RDF/XML graphs, the extraction and analysis code, and interactive versions of all five networks are available in the project repository ("), T("extraction/",{font:"Consolas",size:19}), T(", "), T("src/",{font:"Consolas",size:19}), T(", "), T("dataset/",{font:"Consolas",size:19}), T(", "), T("rdf/",{font:"Consolas",size:19}), T(", "), T("networks/",{font:"Consolas",size:19}), T("). The source PDFs are not redistributed. Every quantitative claim above is reproduced by running "), T("build_dataset2.py",{font:"Consolas",size:19}), T(", "), T("build_rdf.py",{font:"Consolas",size:19}), T(" and "), T("analyze_v2.py",{font:"Consolas",size:19}), T(".")]),

  H1("Bibliography"),
  REF([T("Blondel, Vincent D., Jean-Loup Guillaume, Renaud Lambiotte, and Etienne Lefebvre. 2008. “Fast Unfolding of Communities in Large Networks.” "), I("Journal of Statistical Mechanics: Theory and Experiment"), T(" 2008 (10): P10008.")]),
  REF([T("Bradley, John, and Harold Short. 2005. “Texts into Databases: The Evolving Field of New-Style Prosopography.” "), I("Literary and Linguistic Computing"), T(" 20 (Suppl.): 3–24.")]),
  REF([T("Freeman, Linton C. 1977. “A Set of Measures of Centrality Based on Betweenness.” "), I("Sociometry"), T(" 40 (1): 35–41.")]),
  REF([T("Gil, Moshe. 1992. "), I("A History of Palestine, 634–1099"), T(". Cambridge: Cambridge University Press.")]),
  REF([T("Goitein, S. D. 1967–1993. "), I("A Mediterranean Society: The Jewish Communities of the Arab World as Portrayed in the Documents of the Cairo Geniza"), T(". 6 vols. Berkeley: University of California Press.")]),
  REF([T("Goldberg, Jessica. 2012. "), I("Trade and Institutions in the Medieval Mediterranean: The Geniza Merchants and Their Business World"), T(". Cambridge: Cambridge University Press.")]),
  REF([T("Hagberg, Aric A., Daniel A. Schult, and Pieter J. Swart. 2008. “Exploring Network Structure, Dynamics, and Function Using NetworkX.” In "), I("Proceedings of the 7th Python in Science Conference"), T(", 11–15.")]),
  REF([T("Hary, Benjamin, and Marina Rustow. 2006. “Karaites at the Rabbinical Court: A Legal Deed from Mahdiyya Dated 1073 (T-S 20.187).” "), I("Ginzei Qedem"), T(" 2: 9–36.")]),
  REF([T("Olszowy-Schlanger, Judith. 1998. "), I("Karaite Marriage Documents from the Cairo Geniza: Legal Tradition and Community Life in Mediaeval Egypt and Palestine"), T(". Leiden: Brill.")]),
  REF([T("Olszowy-Schlanger, Judith. 2003. “Karaite Legal Documents.” In "), I("Karaite Judaism: A Guide to Its History and Literary Sources"), T(", edited by Meira Polliack, 255–73. Leiden: Brill.")]),
  REF([T("Padgett, John F., and Christopher K. Ansell. 1993. “Robust Action and the Rise of the Medici, 1400–1434.” "), I("American Journal of Sociology"), T(" 98 (6): 1259–1319.")]),
  REF([T("Preiser-Kapeller, Johannes. 2015. “Calculating the Middle Ages? The Project ‘Complexities and Networks in the Medieval Mediterranean and Near East’.” "), I("Medieval Worlds"), T(" 2: 100–127.")]),
  REF([T("Princeton Geniza Project / Princeton Geniza Lab. "), I("People and Places datasets"), T(". https://geniza.princeton.edu (accessed 2026).")]),
  REF([T("Rustow, Marina. 2008. "), I("Heresy and the Politics of Community: The Jews of the Fatimid Caliphate"), T(". Ithaca: Cornell University Press.")]),
  REF([T("Rustow, Marina. 2011. “The Qaraites as Sect: The Tyranny of a Construct.” In "), I("Sects and Sectarianism in Jewish History"), T(", edited by Sacha Stern, 266–88. Leiden: Brill.")]),
  REF([T("Zinger, Oded. 2017. “A Karaite-Rabbanite Court Session in mid-Eleventh Century Egypt.” "), I("Ginzei Qedem"), T(" 13: 95*–116*.")]),

];

const doc = new Document({
  numbering,
  styles:{default:{document:{run:{font:"Cambria", size:21}}},
    paragraphStyles:[
      {id:"Heading1", name:"Heading 1", basedOn:"Normal", next:"Normal", quickFormat:true,
       run:{size:27, bold:true, color:"1F3864", font:"Cambria"}},
      {id:"Heading2", name:"Heading 2", basedOn:"Normal", next:"Normal", quickFormat:true,
       run:{size:23, bold:true, color:"2E5496", font:"Cambria"}}]},
  sections:[{
    properties:{page:{margin:{top:1300, bottom:1300, left:1300, right:1300}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({children:[PageNumber.CURRENT], size:17})]})]})},
    children
  }]
});

Packer.toBuffer(doc).then(b=>{fs.writeFileSync("../docs/Karaite_SNA_Paper.docx", b); console.log("written");});
