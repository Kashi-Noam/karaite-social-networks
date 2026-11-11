# -*- coding: utf-8 -*-
"""Non-marriage Karaite legal documents: divorces, deeds of release, inheritance,
a court register and a sworn deposition.

These are the documents that Olszowy-Schlanger (1998, ch. 1 n. 6 and the notes to
nos. 3, 5, 7 and 57) and Zinger (2017, nn. 11-17) list as Karaite legal deeds that
are not marriage contracts. Neither publication edits them, so the participants
are taken from the Princeton Geniza Project (PGP): its description of each record
and, where there is one, the transcription it hosts (Goitein, Mann, Krakowski,
Gil). The PGP record is named in each document's `source`.

Left out, with the reason:
  Mosseri Ia.1.2 (951, Judaeo-Persian, Iran)  no accessible text, outside the region
  CUL Or. 1080 J 262                          PGP describes a court deposition whose
                                              Karaite character neither source asserts
  TS 16.56                                    Babylonian-style (Rabbanite) deed
  Bodl. MS Heb. b.13.37, Mosseri VII.7        Zinger (n. 13) doubts the attribution

Certainty follows the corpus convention: "attested" = the name stands in the
document text or the PGP description of it; "reconstructed" = an editor's
identification of a damaged name.
"""

LEGAL_SOURCE = {
 "LD01": "PGP 7746 (Goitein index card); Olszowy-Schlanger 1998, p. 3 n. 6 and notes to no. 57",
 "LD02": "PGP 9469; ed. Olszowy-Schlanger 1996, pp. 272-274; Olszowy-Schlanger 1998, notes to no. 3",
 "LD03": "PGP 9468; ed. Olszowy-Schlanger 1996, pp. 271-272",
 "LD04": "PGP 8432 (Goitein index card); Olszowy-Schlanger 1998, notes to no. 7; Zinger 2017, n. 13",
 "LD05": "PGP 3421 (Goitein transcription); Olszowy-Schlanger 1998, notes to no. 5; Zinger 2017, n. 13",
 "LD06": "PGP 1711 (ed. Mann 1931, 1:380-382); Zinger 2017, n. 13",
 "LD07": "PGP 3654 (Goitein transcription); Olszowy-Schlanger 1998, notes to no. 7; Zinger 2017, n. 13",
 "LD08": "PGP 19632 (Halper catalogue); Zinger 2017, n. 13",
 "LD09": "PGP 7430 (Krakowski digital edition); ed. Mann, Texts and Studies 2:196-198; Zinger 2017, n. 15",
 "LD10": "PGP 3192 (Goitein transcription); Zinger 2017, n. 13 (ed. Rivlin 1999, doc. 15)",
 "LD11": "PGP 1618 (ed. Gil 1983, 2:543-545, doc. 302); Zinger 2017, n. 13",
 "LD12": "PGP 2728 (Goitein transcription, Zinger translation); Zinger 2017, n. 17",
}

# (doc_id, shelfmark, doc_type, date_text, year_est, place, notes)
LEGAL_DOCS = [
 ("LD01","TS 10 J 2.4","bill of divorce (before the wedding)","26 November 1029",1029,"Fustat",
  "Karaite divorce of a betrothed couple; the scribe is neither of the two witnesses; verso notes the return of engagement gifts"),
 ("LD02","TS 12.70","bill of divorce","1030s [?] (by the witness Yefet b. Eli b. Zita)",1032,"Fustat [?]",
  "one of two surviving actual Karaite bills of divorce; wife's name not in the PGP record"),
 ("LD03","TS 12.54","bill of divorce","24 Shevat 135[.] Sel. (1039-1048)",1043,"Fustat",
  "one of two surviving actual Karaite bills of divorce; witnesses not in the PGP record"),
 ("LD04","TS J 3.47r","deed of release (draft)","11 November 1030",1030,"Fustat [?]",
  "draft on the recto of the sheet whose verso holds no. 7 of the edition (TS J 3.47v); no signatures"),
 ("LD05","TS 16.131","deed of release (fragment)","mid-11th c. [?] (by the witness Alan b. Nahum)",1055,"Fustat [?]",
  "signed by many, four signatures preserved; Olszowy-Schlanger identifies Alan b. Nahum by his hand"),
 ("LD06","TS 16.160","deed of release (fragment)","9 Av 13[.]8 Sel. (997-1087)",None,"Fustat",
  "release of Sa'id b. Israel al-Tustari; names of witnesses not preserved; year digit lost"),
 ("LD07","TS 8.137","deed of release","Av 1371 Sel. = July 1060",1060,"Fustat",
  "in Judaeo-Arabic, vocalized; release from a debt recorded in a ruq'a of Shawwal 451 AH"),
 ("LD08","Halper 334 + CAJS RAR MS 82.313.33","deed of release after divorce","1350 Sel. = 1038/39",1038,"n.p.",
  "Karaite by its era formula; the ex-husband renounces claims on his former parents-in-law"),
 ("LD09","TS 16.171 + TS AS 146.459","deed of inheritance division (draft)","Tammuz 1315 Sel. = June/July 1004",1004,"Fustat [?]",
  "three trustees divide the estate of Sahl b. Joseph, who died intestate, among four sons; two minors' shares stay in trust"),
 ("LD10","TS 12.646","will (fragment)","first half of the 11th c. [?]",1025,"n.p.",
  "will of a Karaite mother of two girls before a delivery; no names preserved"),
 ("LD11","TS 12.147","deposition on the state of the crops (calendar testimony)","Dhu al-Qa'da 443 AH = March 1052",1052,"Gaza",
  "Karaite delegation of Gaza and Jerusalem inspects fields to fix the intercalation; each signs in his own hand"),
 ("LD12","Yevr.-Arab. I 1701","record of the Karaite court of Cairo (register)","7 Tevet 14[..] Sel. (after 1089; c. 1200 [?])",1200,"Cairo",
  "inquiry into rumours of harassment of a married woman, convened by the nasi in his sister's house; ban declared next day"),
]

# (doc_id, canonical person name, role, certainty, note)
LEGAL_APPEARANCES = [
 # ---- LD01 TS 10 J 2.4, divorce after betrothal, Fustat 1029
 ("LD01","Sedaqa b. Musa","Party","attested","the husband (fiance)"),
 ("LD01","Umm al-Khayr bt. Musa","Party","attested","the wife (fiancee); returned the engagement gifts"),
 ("LD01","Sedaqa b. Nahum ha-Kohen","Witness","attested","also witness of the agency in no. 57 of the edition"),
 ("LD01","Wahb b. Abraham","Witness","attested",""),

 # ---- LD02 TS 12.70, divorce, Fustat [?]
 ("LD02","Ammar al-Khatiri","Party","attested","the husband"),
 ("LD02","Yefet ha-Kohen b. Eli b. Zita","Witness","attested","the same man witnesses nos. 3 and 57 of the edition"),
 ("LD02","Mevorakh b. Jehuda ha-Levi","Witness","attested",""),

 # ---- LD03 TS 12.54, divorce, Fustat 1039-1048
 ("LD03","Hasan b. Tayyib","Party","attested","the husband"),
 ("LD03","Husn bt. Ya'qub","Party","attested","the wife"),

 # ---- LD04 TS J 3.47r, draft deed of release, 1030
 ("LD04","Ya'ish b. Mevorakh","Agent","attested","attorney (paqid) of Benjamin b. Jacob al-Basri"),
 ("LD04","Benjamin b. Jacob al-Basri","Party","attested","the releasing creditor, acting through his attorney"),
 ("LD04","Isaac b. Tayyib al-Sayrafi","Party","attested","the released debtor, a money-changer; 21.5 dinars still owed, repaid at one dinar a month"),

 # ---- LD05 TS 16.131, deed of release
 ("LD05","Karima bt. Sedaqa ha-Melammed","Party","attested","the releasing party"),
 ("LD05","Sedaqa ha-Melammed (father of Karima)","Mentioned","attested","named in his daughter's genealogy"),
 ("LD05","Abraham b. Hujayj","Party","attested","the released party, 'the elder'"),
 ("LD05","Joseph b. Azarya (TS 16.131)","Witness","attested","same name as the witness of the agency in no. 1 of the edition (Fustat, 1060s); kept apart because no editor identifies them"),
 ("LD05","Alan b. Nahum","Witness","reconstructed","only 'b. Nahum' preserved; identified by his handwriting (Olszowy-Schlanger 1998, notes to no. 5)"),
 ("LD05","Isaac b. [...] (TS 16.131)","Witness","attested","father's name lost"),
 ("LD05","Farah b. Mumal","Witness","attested",""),

 # ---- LD06 TS 16.160, deed of release, Fustat
 ("LD06","Yeshu'a b. Abraham","Party","attested","renounces every claim"),
 ("LD06","Sa'id b. Israel al-Tustari","Party","attested","the released party (Sa'adya b. Israel b. Jacob al-Tustari)"),

 # ---- LD07 TS 8.137, deed of release, Fustat 1060
 ("LD07","Mufarrij b. Isaac al-Sabbagh (Ibn Naqdash al-Ramli)","Party","attested","the dyer, of Ramle; the releasing creditor"),
 ("LD07","Sulayman b. David ('Ajlun al-Qazzaz)","Party","attested","the silk-worker; released from a debt of 4.875 dinars"),
 ("LD07","Mansur b. Mubarak","Witness","attested",""),
 ("LD07","[...] al-Ma'ruf al-Dar (TS 8.137)","Witness","attested","name damaged; reading uncertain"),

 # ---- LD08 Halper 334, release after divorce, 1038/39
 ("LD08","Siba' b. Menashe","Party","attested","the former husband; renounces his claims"),
 ("LD08","Benjamin b. Joseph","Party","attested","father of the divorced wife; released"),
 ("LD08","Ghaniyya bt. Amram","Party","attested","mother of the divorced wife; released"),
 ("LD08","Rida bt. Benjamin","Mentioned","attested","the divorced wife, named as their daughter"),

 # ---- LD09 TS 16.171, division of an inheritance, 1004
 ("LD09","Aaron b. Solomon al-Sirafi","Trustee","attested","the money-changer; one of the three trustees"),
 ("LD09","Nissi b. Aaron b. Bakhtawayh","Trustee","attested","one of the three trustees; in 1016 he records Husn's gift of a codex to the Karaites of Jerusalem (PGP 38543)"),
 ("LD09","Joseph b. Yazdad","Trustee","attested","one of the three trustees"),
 ("LD09","Joseph b. Sahl (heir of Sahl b. Joseph)","Party","attested","eldest heir, Abu al-Husayn"),
 ("LD09","Bishr b. Sahl (heir of Sahl b. Joseph)","Party","attested","heir, Abu al-Tayyib"),
 ("LD09","Aaron b. Sahl (heir of Sahl b. Joseph)","Party","attested","heir, Abu Mansur; a minor of fifteen"),
 ("LD09","Moses b. Sahl (heir of Sahl b. Joseph)","Party","attested","heir, Abu Imran; a minor"),
 ("LD09","Sahl b. Joseph","Mentioned","attested","the deceased, who left no will"),
 ("LD09","Husn bt. Ya'qub b. Joseph b. Khushnam","Party","attested","with the trustees, administers the minors' shares"),

 # ---- LD10 TS 12.646, will: no name preserved

 # ---- LD11 TS 12.147, deposition on the crops, Gaza 1052
 ("LD11","Sedaqa b. Salih b. Sahl b. Zita","Declarant","attested","signs first"),
 ("LD11","Hananya b. Levi b. al-Husayn","Declarant","attested",""),
 ("LD11","Ezra b. Joseph b. Abraham al-Nakhuda","Declarant","attested","'the ship-owner'"),
 ("LD11","Musallam b. Musa","Declarant","attested",""),
 ("LD11","Salih b. Azarya","Declarant","attested","signs twice"),
 ("LD11","Sedaqa b. Joseph b. Shim'on","Declarant","attested",""),
 ("LD11","Yehoshua b. Ezra","Declarant","attested",""),
 ("LD11","Husayn b. Salama b. Hatim","Declarant","attested",""),
 ("LD11","Menashe b. Joseph b. Sahl","Declarant","attested",""),
 ("LD11","Yefet b. Hanina","Declarant","attested","reading uncertain"),
 ("LD11","Joseph b. Netanel","Declarant","attested",""),
 ("LD11","Salama b. Mahmud (the qadi)","Mentioned","attested","Muslim qadi, owner of one of the inspected fields"),
 ("LD11","Ibrahim b. al-Kufiani","Mentioned","attested","owner of a field used for comparison"),

 # ---- LD12 Yevr.-Arab. I 1701, Karaite court of Cairo
 ("LD12","Solomon (nasi, Cairo register)","Judge","attested","'ha-nasi ha-gadol Sh[elomo]', convened the inquiry in his sister's house"),
 ("LD12","Neham'el b. Mevorakh b. Jehuda b. Aaron","Scribe","attested","the writer of the record, who received the petition"),
 ("LD12","Abu Nasr b. Qayyuma","Party","attested","the accused; under an earlier restraining order"),
 ("LD12","Daughter of Abu al-Ma'ali b. Tamar","Party","attested","the complainant, never named; wife of Abu Sa'd"),
 ("LD12","Abu Sa'd b. Sedaqa al-Labban","Party","attested","the milkman, her husband and guardian"),
 ("LD12","Abu al-Ma'ali b. Tamar","Mentioned","attested","her father, named in her designation"),
 ("LD12","Abu al-Faraj al-Tahhan","Declarant","attested","the miller, Abu Sa'd's brother-in-law; testified to the harassment"),
 ("LD12","Netan'el ha-Kohen b. Amram","Witness","attested",""),
 ("LD12","Yefet ha-Melammed b. Halfon","Witness","attested","reading of the father's name uncertain; also witnesses the addendum"),
 ("LD12","Abraham b. Yefet","Witness","attested","also witnesses the addendum"),
]

LEGAL_SECT = {
 "Solomon (nasi, Cairo register)": ("Karaite","the Karaite nasi presiding over the Karaite court of Cairo (Yevr.-Arab. I 1701)"),
 "Salama b. Mahmud (the qadi)": ("unknown","Muslim qadi; outside the closed sect list (TS 12.147)"),
 "Ibrahim b. al-Kufiani": ("unknown","field owner in Gaza, probably Muslim (TS 12.147)"),
}

# (source, relation, target, evidence doc, note)
LEGAL_RELATIONS = [
 ("Sedaqa b. Musa","divorced","Umm al-Khayr bt. Musa","LD01","divorce after betrothal"),
 ("Hasan b. Tayyib","divorced","Husn bt. Ya'qub","LD03",""),
 ("Siba' b. Menashe","divorced","Rida bt. Benjamin","LD08",""),
 ("Benjamin b. Joseph","married","Ghaniyya bt. Amram","LD08",""),
 ("Benjamin b. Joseph","father_of","Rida bt. Benjamin","LD08",""),
 ("Ghaniyya bt. Amram","mother_of","Rida bt. Benjamin","LD08",""),
 ("Sedaqa ha-Melammed (father of Karima)","father_of","Karima bt. Sedaqa ha-Melammed","LD05",""),
 ("Ya'ish b. Mevorakh","agent_for","Benjamin b. Jacob al-Basri","LD04","attorney in a deed of release"),
 ("Sahl b. Joseph","father_of","Joseph b. Sahl (heir of Sahl b. Joseph)","LD09",""),
 ("Sahl b. Joseph","father_of","Bishr b. Sahl (heir of Sahl b. Joseph)","LD09",""),
 ("Sahl b. Joseph","father_of","Aaron b. Sahl (heir of Sahl b. Joseph)","LD09",""),
 ("Sahl b. Joseph","father_of","Moses b. Sahl (heir of Sahl b. Joseph)","LD09",""),
 ("Abu Sa'd b. Sedaqa al-Labban","married","Daughter of Abu al-Ma'ali b. Tamar","LD12",""),
 ("Abu al-Ma'ali b. Tamar","father_of","Daughter of Abu al-Ma'ali b. Tamar","LD12",""),
 ("Abu al-Faraj al-Tahhan","associated_with","Abu Sa'd b. Sedaqa al-Labban","LD12","brother-in-law"),
]

LEGAL_ORIGIN = {
 "Benjamin b. Jacob al-Basri": "PL12",
 "Mufarrij b. Isaac al-Sabbagh (Ibn Naqdash al-Ramli)": "PL04",
}
