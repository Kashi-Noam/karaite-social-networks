# -*- coding: utf-8 -*-
# APPEARANCES: (doc_id, canonical person name, role, certainty, note)
# certainty: "attested" (named in document text/signatures) | "reconstructed" (editor's reconstruction/index) | "contextual" (mentioned in editor's comments as connected to this document)
# Role vocabulary:
#  Groom, Bride, GroomFather, BrideFather, BrideGrandfather, GroomGrandfather,
#  Agent (bride's agent/paqid), GroomAgent, WitnessOfAgency, Witness, Scribe,
#  Nasi (reigning nasi named in the document), Judge, Trustee, Guarantor, Party,
#  Declarant, Mentioned

A = [
# ---- OS01: betrothal of Na'ama bt. Nisi & Barakat b. Daud, 1060s, Fustat
("OS01","Barakat b. David","Groom","attested",""),
("OS01","David (father of Barakat)","GroomFather","attested","Arabic form Daud in OS01, Hebrew David in OS02"),
("OS01","Na'ama bt. Nisi","Bride","attested",""),
("OS01","Nisi b. Jacob","BrideFather","attested","also her agent (paqid)"),
("OS01","Nisi b. Jacob","Agent","attested",""),
("OS01","Jacob (father of Nisi)","BrideGrandfather","attested",""),
("OS01","Yehezqel b. Benjamin ha-Levi","WitnessOfAgency","attested","also signs as witness"),
("OS01","Joseph b. Azarya","WitnessOfAgency","attested","also signs on margin as witness"),
("OS01","Hasan b. Sedaqa ha-Kohen","Witness","attested",""),
("OS01","Sedaqa b. Isaac","Witness","attested","per name index"),
("OS01","Yefet b. Jacob","Witness","attested",""),
("OS01","El'azar b. Samuel b. Sahl ha-Eved","Witness","attested","also witness in OS32 (1062, Fustat) - basis for dating"),
("OS01","Moses b. A[...]","Witness","attested","name damaged"),
("OS01","Jacob b. Joseph","Witness","attested",""),
("OS01","Samuel b. Sahl","Mentioned","contextual","father of El'azar; signed Rabbanite court doc of Efraim b. Shemarya ~1042 with other Karaites"),

# ---- OS02: ketubba of same couple
("OS02","Barakat b. David","Groom","attested",""),
("OS02","David (father of Barakat)","GroomFather","attested",""),
("OS02","Na'ama bt. Nisi","Bride","attested",""),
("OS02","Nisi b. Jacob","BrideFather","attested",""),
("OS02","Nisi b. Jacob","Agent","attested",""),
("OS02","[...] b. Yesha'ya ha-Kohen","WitnessOfAgency","attested","first name lost"),
("OS02","Barakat b. Azarya","WitnessOfAgency","attested","possibly brother of Joseph b. Azarya (OS01)"),

# ---- OS03: betrothal of Mubaraka & Isaac b. Eli, ~1030, Fustat
("OS03","Isaac b. Eli","Groom","attested",""),
("OS03","Mubaraka bt. [...]","Bride","attested","father's name lost"),
("OS03","Jehuda ha-Levi b. Nisi ha-Melammed","Scribe","attested","also witness"),
("OS03","Jehuda ha-Levi b. Nisi ha-Melammed","Witness","attested",""),
("OS03","Joseph b. Jehuda ha-Levi","Scribe","attested","son of the above; also witness"),
("OS03","Joseph b. Jehuda ha-Levi","Witness","attested",""),
("OS03","Babad ha-Kohen b. David","Witness","attested","Persian name"),
("OS03","Yefet ha-Kohen b. Eli b. Zita","Witness","attested","also witness in OS57 and in Karaite divorce TS 12.70; brother of Yehoshua (OS39)"),
("OS03","Samuel b. Joseph al-Basri","Witness","attested","Iraqi origin; probably d. ~1028 in Fustat"),
("OS03","Sedaqa b. Moses","Witness","attested",""),
("OS03","Joseph b. Aaron ha-Levi","Witness","attested",""),

# ---- OS04: Tustari-nesi'im betrothal draft, 1040s, Fustat
("OS04","Yefet b. Abraham al-Tustari","Groom","attested","only son of Abraham al-Tustari; briefly Fatimid vizier in 1064"),
("OS04","Abraham (Abu Sa'ad) b. Sahl al-Tustari","GroomFather","attested","financial adviser to the mother of Caliph Mustansir; d. 1047"),
("OS04","Ama al-Aziz bt. Hizkiyahu","Bride","attested","in Jerusalem"),
("OS04","Hizkiyahu b. Solomon (nasi)","BrideFather","attested","Karaite nasi in Jerusalem; original agent of his daughter"),
("OS04","Hizkiyahu b. Solomon (nasi)","Agent","attested","first appointment; delegated by deed of attorney"),
("OS04","Ezra b. Ishma'el b. Ezra","Agent","attested","substitute agent in Fustat; prominent Fustat Karaite"),
("OS04","Aaron b. Sahl al-Tustari","WitnessOfAgency","attested","witness of first appointment; youngest Tustari brother; uncle of groom"),
("OS04","Aaron b. Yehoshua","WitnessOfAgency","attested","witness of second appointment, Jerusalem; possibly the grammarian Abu'l-Faraj Harun"),
("OS04","Azarya b. Salih","WitnessOfAgency","attested","witness of second appointment"),
("OS04","David b. Semah (nasi)","Nasi","attested","presided over Karaite court in Fustat certifying the deed of attorney"),
("OS04","David b. Semah (nasi)","Judge","attested","Karaite court certification"),
("OS04","Khatabya b. al-Tabat","Witness","attested","verso, court certificate"),
("OS04","Sahl b. Sa'adya al-Baghdadi","Witness","attested","also in deed of release CUL Or 1080 J 262"),
("OS04","Joseph b. Abraham b. al-Fara","Witness","attested",""),
("OS04","Abraham b. al-Fara","Witness","attested",""),
("OS04","Hesed (Abu Nasr) b. Sahl al-Tustari","Mentioned","contextual","brother of Abraham; murdered 1048"),
("OS04","Sahl (Yashar) b. Israel al-Tustari","Mentioned","attested","deceased patriarch, mentioned with formulae for the dead"),
("OS04","Solomon b. David (nasi)","Mentioned","attested","in bride's genealogy: Hizkiyahu b. Solomon b. David"),

# ---- OS05: betrothal of Ama al-Qadar & Khalaf b. Mahfuz, 1045, Fustat
("OS05","Khalaf b. Mahfuz","Groom","attested",""),
("OS05","Mahfuz (father of Khalaf)","GroomFather","attested","also called Mansur by scribal confusion"),
("OS05","Ama al-Qadar bt. Efraim","Bride","attested",""),
("OS05","Efraim b. Mansur b. Furat","BrideFather","attested","also her agent"),
("OS05","Efraim b. Mansur b. Furat","Agent","attested",""),
("OS05","Sedaqa b. Masliah b. Sahl ha-Levi","Scribe","attested","signs first"),
("OS05","Barakat b. Menahem ha-Kohen","WitnessOfAgency","attested",""),
("OS05","Yefet b. Abraham ha-Levi","WitnessOfAgency","attested",""),
("OS05","David b. Isaac b. Moses ha-Levi","Witness","attested",""),
("OS05","Alan b. Nahum","Witness","attested","also witness OS32 and Karaite deed of release TS 16.131"),
("OS05","Joseph b. [...] b. Efraim","Witness","attested",""),
("OS05","David b. Yesha'ya","Witness","reconstructed","reading uncertain; possibly = father of bride in OS13"),
("OS05","[...] b. Nahum","Witness","attested","possibly brother of Alan b. Nahum; possibly = Nahum b. Nahum (OS09)"),
("OS05","David b. Semah (nasi)","Nasi","attested","'our Lord, the great nasi, David'"),

# ---- OS06: betrothal fragment, 1063, Fustat
("OS06","Hizkiyahu b. Solomon (nasi)","Nasi","attested","acting nasi in Fustat, 'nasi of the Land of Israel and Juda'"),
("OS06","Solomon b. David (nasi)","Mentioned","attested","deceased father in nasi clause"),

# ---- OS07: Arabic settlement of betrothal, 1033, Fustat
("OS07","David b. Amram ha-Levi (Abu'l-Hasan Da'ud b. al-Faraj Imran)","Groom","attested","Karaite notable of Fustat; commissioned Yehoshua b. Jehuda's Genesis commentary"),
("OS07","Daughter of Abu'l-Fadl","Bride","attested","name not given"),
("OS07","Abu'l-Fadl","BrideFather","attested","also her agent"),
("OS07","Abu'l-Fadl","Agent","attested",""),
("OS07","'The exquisite scholar'","WitnessOfAgency","attested","anonymous"),
("OS07","Abu'l-Hasan b. al-Jabawi","WitnessOfAgency","attested",""),
("OS07","Mevorakh b. Amram","Mentioned","contextual","brother of groom, learned Karaite of Fustat"),
("OS07","Yehoshua b. Jehuda (Abu'l-Faraj Furqan ibn Asad)","Mentioned","contextual","Karaite scholar of Jerusalem who wrote commentary at groom's request"),

# ---- OS08: betrothal of Husn bt. Hayyim & Jabir b. Azhar, 1030s-40s, Fustat
("OS08","Jabir b. Azhar ha-Kohen","Groom","attested","probably wakil (merchants' representative) in Tinnis"),
("OS08","Azhar (father of Jabir)","GroomFather","attested",""),
("OS08","Husn bt. Hayyim","Bride","attested","granddaughter of Sahlawaya b. Hayyim"),
("OS08","Hayyim b. Sahlawaya","BrideFather","attested","purchased a Bible in Jerusalem in 1057"),
("OS08","Sahlawaya b. Hayyim","BrideGrandfather","attested","prominent Karaite banker of Fustat (active 1011-1035); still alive"),
("OS08","El'azar b. Menashe","WitnessOfAgency","attested",""),
("OS08","Nathan b. [...]","WitnessOfAgency","attested",""),
("OS08","Eli b. Sahlawaya","Mentioned","contextual","brother of Hayyim; donated Bible codex to Fustat Karaites"),

# ---- OS09
("OS09","[...] b. Khalaf","WitnessOfAgency","attested",""),
("OS09","Nahum b. Nahum","WitnessOfAgency","attested","possibly = [...] b. Nahum of OS05"),

# ---- OS11: betrothal of Ama al-Wahid & Halfon ha-Levi b. Daniel, early 11th c., Cairo
("OS11","Halfon ha-Levi b. Daniel","Groom","attested",""),
("OS11","Daniel b. Bundar","GroomFather","attested","Persian grandfather name"),
("OS11","Ama al-Wahid bt. Halfon","Bride","attested",""),
("OS11","Halfon (father of Ama al-Wahid)","BrideFather","attested",""),
("OS11","Musafir b. Isaac ha-Kohen","WitnessOfAgency","attested",""),
("OS11","Shela b. Joseph","WitnessOfAgency","attested",""),
("OS11","Hillel (the elder)","Agent","attested",""),

# ---- OS12: betrothal fragment, 1041, Fustat
("OS12","Hizkiyahu (groom, OS12)","Groom","attested","only name preserved"),
("OS12","Mevorakh b. Barhun","WitnessOfAgency","attested",""),
("OS12","Sedaqa b. Elun","WitnessOfAgency","attested",""),
("OS12","David b. Semah (nasi)","Nasi","reconstructed","only father's name Semah preserved in clause"),

# ---- OS13: double-proxy betrothal, 1051 Fustat / attorney Tyre 1050
("OS13","Shela b. Amram al-Qirqisani","Groom","attested","resident of Tyre; family from Qirqisiya, Upper Mesopotamia"),
("OS13","Amram al-Qirqisani","GroomFather","attested",""),
("OS13","Yaman bt. David","Bride","attested",""),
("OS13","David b. Yesha'ya ha-Melammed","BrideFather","attested","'champion of the Torah'; possibly = witness of OS05"),
("OS13","Solomon b. Adiya b. Menashe (al-Qazzaz)","GroomAgent","attested","of the al-Qazzaz family of Karaite Fatimid officials in Tyre"),
("OS13","Yefet [b. ? Solomon b. Abraham]","WitnessOfAgency","attested","witness to deed of attorney in Tyre; text damaged"),
("OS13","Samuel bar Rabbi Moses he-haver","WitnessOfAgency","attested","RABBANITE haver; witness of attorney in Tyre; also witness of Tyre Rabbanite court letter to Aleppo 1029"),
("OS13","David b. Semah (nasi)","Nasi","attested","read, verified and certified the deed of attorney"),
("OS13","David b. Semah (nasi)","Judge","attested",""),
("OS13","Semah b. Asa (nasi)","Mentioned","attested","deceased father in nasi clause"),
("OS13","Solomon b. Musafir","Agent","attested","bride's agent; signatory of Tyre court letter to Aleppo 1029; in Damascus deed of receipt 1031"),
("OS13","Aaron b. Semah ha-Kohen","WitnessOfAgency","attested","witness of bride's appointment"),
("OS13","Sedaqa b. Sa'adya","WitnessOfAgency","attested","witness of bride's appointment"),
("OS13","Mansur b. Mevasser","Witness","attested",""),
("OS13","Samuel b. [...]","Witness","attested",""),
("OS13","Joseph ha-Kohen b. Jacob","Mentioned","contextual","Rabbanite scribe of Tyre court; wrote/witnessed Karaite deeds from Tyre (TS AS 153.12+13 J 25.20)"),

# ---- OS14: betrothal of Fadla & Mahfuz b. Menahem, 1049, Fustat
("OS14","Mahfuz b. Menahem","Groom","attested",""),
("OS14","Menahem (father of Mahfuz)","GroomFather","attested",""),
("OS14","Fadla bt. Abraham","Bride","attested",""),
("OS14","Abraham b. Musallam","BrideFather","attested","professional scribe; scribe & witness of OS43; scribe of Karaite calendars"),

# ---- OS15: court copy of ketubba of Mu'ammala bt. Hayyim, 1002, Palestine
("OS15","Mu'ammala bt. Hayyim","Bride","attested","wife; copy made upon her declaration"),
("OS15","Menashe b. Mahbub ha-Levi (of Acre)","Scribe","attested",""),
("OS15","Bahlul b. Isaac ha-Kohen","Witness","attested",""),
("OS15","Isaac b. Eliya ha-Kohen","Witness","attested",""),
("OS15","Isaac b. Samuel al-Fara","Witness","attested",""),
("OS15","Eli b. Mu'ammar","Witness","attested","also witness OS39 (Jerusalem 1028); al-Sharabi 'maker of potions'"),
("OS15","Joseph b. Jacob","Witness","attested",""),
("OS15","Isaac b. Jacob","Witness","attested",""),
("OS15","Sa'adya b. Joseph","Witness","attested",""),
("OS15","Abraham b. Isaac","Witness","attested",""),
("OS15","David b. Solomon","Witness","attested",""),
("OS15","Hiba b. Khalaf al-Shinizi","Witness","attested","family of Iranian origin (Shiniz in Fars)"),
("OS15","Joseph b. Isaac","Witness","attested",""),
("OS15","Jacob b. Isaac","Witness","attested",""),

# ---- OS17
("OS17","Sitt-al-Ahl bt. Joseph","Bride","reconstructed","name partly preserved"),

# ---- OS19: two probably-Rabbanite witnesses
("OS19","Shela ha-Kohen b. Sadoq beRabbi [...]","Witness","attested","Aramaic bar/beRabbi - likely Rabbanite"),
("OS19","Levi ha-Levi bar Joseph","Witness","attested","Aramaic bar - likely Rabbanite"),

# ---- OS20: ketubba of Sara(?) bt. Sahlawaya & Rav Hesed, 1030s-40s, Fustat
("OS20","Rav Hesed","Groom","attested","father's name lost; identification with Hesed al-Tustari rejected by editor"),
("OS20","Sara bt. Sahlawaya","Bride","reconstructed","reading of name uncertain"),
("OS20","Sahlawaya b. Hayyim","BrideFather","attested","the Fustat Karaite banker; father Hayyim already dead here"),
("OS20","David b. Shekhanya","Mentioned","contextual","Rabbanite cantor of Palestinian synagogue in Fustat who wrote poem honoring Sahlawaya"),

# ---- OS21
("OS21","Malka","Bride","attested","only name preserved"),

# ---- OS23: ketubba of Sara bt. Sahl & Abraham b. Jacob, 1089-1187
("OS23","Abraham b. Jacob","Groom","attested",""),
("OS23","Jacob (father of Abraham, OS23)","GroomFather","attested",""),
("OS23","Sara bt. Sahl","Bride","attested","dowry totalling 3884 dinars"),
("OS23","Sahl (father of Sara, OS23)","BrideFather","attested",""),
("OS23","Sa'id ha-Kohen b. Nahum","Witness","attested","reading partly damaged"),

# ---- OS25
("OS25","Meshullam (groom, OS25)","Groom","attested","only name preserved"),
("OS25","Jacob b. Yesha'ya","Agent","attested","bride's agent"),

# ---- OS26: ketubba of Rivqa & El'azar b. Shemen Tov, 1201, Cairo
("OS26","El'azar b. Shemen Tov","Groom","attested",""),
("OS26","Shemen Tov b. Shemarya","GroomFather","attested",""),
("OS26","Shemarya b. Shemen Tov","GroomGrandfather","attested",""),
("OS26","Rivqa bt. Joseph","Bride","attested","father from Byzantium; no dowry - poor bride"),
("OS26","Joseph (father of Rivqa)","BrideFather","attested","'who was from Byzantium'"),
("OS26","Amram ha-Levi b. Joseph ha-Levi","Agent","attested","bride's agent; grandfather Isaac ha-Levi"),
("OS26","[...] b. El'azar b. Halfon","WitnessOfAgency","attested","first name lost"),
("OS26","Isaac b. Yefet","WitnessOfAgency","attested","great-grandfather Isaac was 'a pious man from among the Rabbanites'"),
("OS26","Isaac bar Azaryahu","Scribe","attested","probably RABBANITE (cursive script, Aramaic bar)"),
("OS26","Isaac bar Azaryahu","Witness","attested",""),
("OS26","Nathana'el ha-Kohen b. Meshullam","Witness","attested",""),
("OS26","Eliyahu b. Halfon","Witness","attested",""),
("OS26","Amaryahu Jehuda (nasi)","Nasi","attested","'the great nasi, nasi of those who bring testimony'"),
("OS26","David b. Hasdai (nasi)","Mentioned","attested","father of Amaryahu Jehuda in nasi clause"),
("OS26","Hasdai Emmanuel (nasi)","Mentioned","attested","co-mentioned nasi, son of Sar Shalom"),
("OS26","Sar Shalom (nasi)","Mentioned","attested","possibly a second name of Hizkiyahu"),

# ---- OS27
("OS27","Rayyisa (bride, OS27)","Bride","attested","only name preserved; dowry 1170 dinars"),

# ---- OS28
("OS28","Mevorakh b. Yehya","Groom","attested",""),
("OS28","Mubaraka (bride, OS28)","Bride","attested",""),
("OS28","Aaron b. Mordekhai","Agent","attested","bride's agent"),

# ---- OS29: ketubba of Sitt-al-Ahl & Mevorakh b. Samuel, early 11th c., Tyre?
("OS29","Mevorakh b. Samuel","Groom","attested",""),
("OS29","Sitt-al-Ahl (bride, OS29)","Bride","attested",""),
("OS29","Maimon b. Fadl","WitnessOfAgency","attested",""),
("OS29","Solomon b. Maimon","WitnessOfAgency","attested","son of Maimon b. Fadl"),
("OS29","Eli b. Solomon","Agent","attested","bride's agent"),
("OS29","Shala [?]","Witness","attested","name uncertain"),
("OS29","Mubarak b. Husain","Witness","attested",""),
("OS29","Shela ha-Kohen bar Rabbi Mevasser","Witness","attested","RABBANITE (Aramaic elements in name)"),
("OS29","Mevorakh b. Yefet","Witness","attested","probably = Karaite groom of mixed marriage contract Antonin 637"),
("OS29","Mevasser b. Abraham","Witness","attested",""),
("OS29","Benjamin b. Hasson","Witness","attested","per name index"),

# ---- OS30: ketubba of Farajiyya & Yesha'ya b. Isaac, early 11th c.
("OS30","Yesha'ya b. Isaac","Groom","attested",""),
("OS30","Farajiyya bt. Jehuda","Bride","attested",""),
("OS30","Jehuda (father of Farajiyya)","BrideFather","attested",""),
("OS30","Mansur b. Yehai b. Abu'l-Shahaba","Agent","attested","bride's agent"),
("OS30","Hasan (Yefet) b. Amram known as ben Shemun","WitnessOfAgency","attested","Hebrew translation Yefet written above"),
("OS30","Solomon b. Mansur","WitnessOfAgency","attested",""),

# ---- OS31: ketubba of Sara & Solomon (first cousins, al-Ani), 1004, Cairo
("OS31","Solomon b. Mevasser b. Sahl al-Ani","Groom","attested","prominent Karaite merchant family (from Ana on the Euphrates)"),
("OS31","Mevasser b. Sahl al-Ani","GroomFather","attested",""),
("OS31","Sara bt. Yesha'ya","Bride","attested","first cousin of groom"),
("OS31","Yesha'ya b. Sahl al-Ani","BrideFather","attested","received the payment; brother of Mevasser"),
("OS31","Sahl al-Ani","BrideGrandfather","attested","common grandfather"),

# ---- OS32: ketubba of Faras & Marzuq, 1062, Fustat
("OS32","Marzuq b. Yefet","Groom","attested",""),
("OS32","Yefet (father of Marzuq)","GroomFather","attested",""),
("OS32","Faras bt. Simha","Bride","attested",""),
("OS32","Simha (father of Faras)","BrideFather","attested",""),
("OS32","Hananya b. Elnathan","Agent","attested","bride's agent; probably = legatee in Rabbanite deed TS 13 J 1.18 (Fustat 1078); possibly Abu'l-Zahir ibn al-Qatmani who sold book to Rabbanite synagogue"),
("OS32","Nathana'el b. Mevasser ha-Levi","WitnessOfAgency","attested",""),
("OS32","Abraham b. Joseph b. Anan ha-Levi","Witness","attested","mentioned as deceased in Rabbanite deed TS 13 J 1.18"),
("OS32","Alan b. Nahum","Witness","attested","here with honorific for the dead"),
("OS32","El'azar b. Samuel b. Sahl ha-Eved","Witness","attested","also OS01; here with honorific for the dead"),
("OS32","[...] b. Efraim","Witness","attested","deceased"),
("OS32","Sa'adya b. Razi'el","Witness","attested",""),
("OS32","Sedaqa b. Menashe","Witness","attested",""),
("OS32","Saul b. Abraham","Witness","attested",""),

# ---- OS33: ketubba of Sitt-al-Husn (widow) & Menashe, 1080s-90s, Fustat
("OS33","Menashe (groom, OS33)","Groom","attested","first cousin of the bride; son of the elder Aaron ha-Kohen"),
("OS33","Aaron ha-Kohen (father of Menashe)","GroomFather","attested","deceased"),
("OS33","Sitt-al-Husn bt. Moses ha-Kohen","Bride","attested","widow; first husband Abu Imran Moses b. Yefet"),
("OS33","Moses ha-Kohen b. Aaron","BrideFather","attested","'the mighty prince', prominent Karaite courtier of Fustat; d. 1085; will preserved"),
("OS33","Aaron ha-Kohen (grandfather, OS33)","BrideGrandfather","attested",""),
("OS33","Eli b. Hillel","Agent","attested","bride's agent"),
("OS33","Moses b. Yefet (Abu Imran)","Mentioned","contextual","first husband of Sitt-al-Husn; deceased"),
("OS33","Nasiya bt. Moses ha-Kohen","Mentioned","contextual","sister of bride; married David b. Daniel b. Azarya (Rabbanite Gaon family) in 1082 (TS 24.1)"),
("OS33","David b. Daniel b. Azarya","Mentioned","contextual","RABBANITE; controversial Gaon, of the Exilarch family; husband of Nasiya"),

# ---- OS34
("OS34","Jehuda (groom, OS34)","Groom","attested",""),
("OS34","Sitt-al-Fadl","Bride","attested",""),
("OS34","Solomon b. [...] (agent, OS34)","Agent","attested","name partly erased"),

# ---- OS35: ketubba of al-Tifrat & Ovadya, before 1087, Fustat
("OS35","Ovadya b. Sedaqa","Groom","attested",""),
("OS35","Sedaqa b. Halfon b. Elun","GroomFather","attested","deceased"),
("OS35","al-Tifrat bt. Tovya","Bride","attested",""),
("OS35","Tovya (father of al-Tifrat)","BrideFather","attested",""),
("OS35","Yefet b. Menashe","Agent","attested","bride's agent"),

# ---- OS37: ketubba of Ghaliya & Thabit, 11th c.
("OS37","Thabit b. Jacob","Groom","attested",""),
("OS37","Jacob (father of Thabit)","GroomFather","attested",""),
("OS37","Ghaliya bt. Joseph","Bride","attested","wealthy; dowry at least 374 dinars incl. house"),
("OS37","Joseph b. Abraham (father of Ghaliya)","BrideFather","attested","also her agent"),
("OS37","Joseph b. Abraham (father of Ghaliya)","Agent","attested",""),

# ---- OS38: ketubba of Sayyida & Jacob al-Shulhani, 1006, Ramle
("OS38","Jacob b. David al-Shulhani","Groom","attested","banker/money-changer family"),
("OS38","David al-Shulhani","GroomFather","attested",""),
("OS38","Sayyida bt. Wahb","Bride","attested","very wealthy; dowry incl. two houses in Ramle (400 dinars)"),
("OS38","Wahb al-Arri [?]","BrideFather","attested","deceased"),
("OS38","Menahem b. Job al-Halabi","Agent","attested","bride's agent; family from Aleppo"),
("OS38","David b. Isaac ha-Kohen (the scribe)","WitnessOfAgency","attested","also witness of court copy OS41 (Ramle)"),
("OS38","Khalaf [...] (OS38)","WitnessOfAgency","attested","name damaged"),
("OS38","Faraj b. Mevasser ha-Levi","Witness","attested",""),
("OS38","Semah [...] (OS38)","Witness","attested","name damaged"),
("OS38","Efraim b. Jehuda","Witness","attested",""),
("OS38","Joseph [...] (OS38)","Witness","attested","name damaged"),
("OS38","Jacob [...] (OS38)","Witness","attested","name damaged"),
("OS38","Solomon b. Hayyim (Ramle)","Mentioned","attested","owner of house next to the dowry houses in Ramle"),

# ---- OS39: ketubba of Sarwa & Hizkiyahu b. Benjamin, 1028, Jerusalem
("OS39","Hizkiyahu b. Benjamin","Groom","attested",""),
("OS39","Benjamin (father of Hizkiyahu, OS39)","GroomFather","attested",""),
("OS39","Sarwa bt. Sedaqa","Bride","attested",""),
("OS39","Sedaqa b. Jarir","BrideFather","attested",""),
("OS39","Joseph b. Abraham ha-Kohen","Agent","attested","bride's agent; tentatively identified with the Karaite philosopher Joseph al-Basir"),
("OS39","Mevorakh b. David","WitnessOfAgency","attested",""),
("OS39","Jacob b. Fadlan","WitnessOfAgency","attested",""),
("OS39","Solomon b. David ha-Kohen (the scholar)","Scribe","attested","scribe; signed first"),
("OS39","Solomon b. David ha-Kohen (the scholar)","Witness","attested",""),
("OS39","Yehoshua b. Eli ha-Kohen b. Zita","Witness","attested","descendant of the Karaite scholar Eli ha-Kohen b. Zita; brother of Yefet (OS03, OS57)"),
("OS39","Nathan ha-Kohen bar Yehai","Witness","attested","Aramaic bar - possibly Rabbanite"),
("OS39","Yehoshua b. Adiya ha-Kohen","Witness","attested",""),
("OS39","Bishr b. Abraham ha-Levi","Witness","attested","also witness of court copy OS41"),
("OS39","Nathan b. Nisan ha-Levi (the scholar)","Witness","attested","probably father of Mevorakh b. Nathan b. Nisan (letter of 1100)"),
("OS39","Eli b. Mu'ammar","Witness","attested","al-Sharabi; also witness OS15 (1002)"),
("OS39","Omar b. Yehoshua","Witness","attested",""),
("OS39","Joseph b. Samuel","Witness","attested",""),
("OS39","Sedaqa b. Zakharya","Witness","attested",""),

# ---- OS40: ketubba of Miriam (widow) & Jehuda b. Khalaf, 1037?, Fustat
("OS40","Jehuda b. Khalaf","Groom","attested","possibly = witness of OS46"),
("OS40","Khalaf (father of Jehuda, OS40)","GroomFather","attested",""),
("OS40","Miriam bt. Solomon","Bride","attested","widow"),
("OS40","Solomon (father of Miriam, OS40)","BrideFather","attested",""),
("OS40","Faraj b. Solomon","Agent","attested","bride's agent; possibly her brother"),
("OS40","Abraham al-Awalani","WitnessOfAgency","attested",""),
("OS40","Semah b. Asa (nasi)","Nasi","attested","nasi of Fustat, basis for dating to 1037"),

# ---- OS41: court copy of ketubba of Husn bt. David & Solomon b. Amram, 1010s-20s, Ramle
("OS41","Solomon b. Amram (OS41)","Groom","attested","husband"),
("OS41","Husn bt. David (OS41)","Bride","attested","wife"),
("OS41","Eli b. Isma'il al-Bairuti (the scholar)","Declarant","attested","declared the copy conforms to the original"),
("OS41","Yehai b. Eli ha-Kohen","Witness","attested","witness of original ketubba"),
("OS41","Yeshu'a b. Thabit ha-Levi ha-Shulhani","Witness","attested","witness of original; deceased"),
("OS41","[...] b. Isaac ha-Levi al-Qata'if","Witness","attested","witness of original; 'maker of almond cakes'"),
("OS41","Mahbub [?] (OS41)","Witness","attested","witness of original"),
("OS41","Efraim b. Moses","Witness","attested","witness of original"),
("OS41","Yeshu'a b. Khatim","Witness","attested","witness of original"),
("OS41","Menahem b. Isaac","Witness","attested","witness of original; beadle of the Middle Synagogue in Ramle; summoned to the court in Ramle to certify"),
("OS41","Menahem b. Isaac","Declarant","attested","certified correctness before the Ramle court"),
("OS41","David b. Isaac ha-Kohen (the scribe)","Scribe","attested","scribe & witness of the copy; also WitnessOfAgency in OS38"),
("OS41","David b. Isaac ha-Kohen (the scribe)","Witness","attested",""),
("OS41","Jehuda [?] (OS41)","Witness","attested","witness of copy"),
("OS41","Bishr b. Abraham ha-Levi","Witness","attested","witness of copy; also OS39"),
("OS41","Parhon b. Mevorakh ha-Levi","Witness","attested","witness of copy"),
("OS41","Mevorakh b. Nathan","Witness","attested","witness of copy"),
("OS41","Isaac b. [...] (OS41)","Witness","attested","witness of copy"),
("OS41","Habib b. David (Abu Ali)","Witness","attested","witness of copy"),

# ---- OS42: ketubba of Karima & Isaac b. Joseph, mid-11th c., Fustat
("OS42","Isaac b. Joseph (groom, OS42)","Groom","attested","named among those who came for the appointment of the bride's agent; he is a party to the act, not a witness to it"),
("OS42","Joseph (father of Isaac, OS42)","GroomFather","attested",""),
("OS42","Karima bt. Abraham","Bride","attested",""),
("OS42","Abraham (father of Karima)","BrideFather","attested","also her agent; received the mohar"),
("OS42","Abraham (father of Karima)","Agent","attested",""),
("OS42","Jacob b. Hillel b. Awkal","WitnessOfAgency","attested","descendant of the great RABBANITE merchant Joseph ibn Awkal"),

# ---- OS43: ketubba fragment of groom Sedaqa, 1020s-30s (before 1044), Fustat
("OS43","Sedaqa (groom, OS43)","Groom","attested","other names lost"),
("OS43","Abraham b. Musallam","Scribe","attested","wrote the deed; father of bride of OS14"),
("OS43","Abraham b. Musallam","Witness","attested",""),
("OS43","Abraham ha-Kohen b. Khalaf","Witness","attested",""),
("OS43","Nathana'el ha-Levi b. Rawh","Witness","attested","addressee of letters of Nathan b. Abraham (Rabbanite Gaon contender who courted Karaite support)"),
("OS43","Barakat b. Mubarak","Witness","attested",""),
("OS43","[...] ha-Kohen b. Joseph","Witness","attested",""),
("OS43","Levi ha-Levi bar Jacob","Witness","attested","RABBANITE (Aramaic bar); known from Fustat Rabbanite court documents; d. before 1044"),
("OS43","Barakat b. Benjamin","Witness","attested","per name index"),
("OS43","Berakha b. Rawh (Abu'l-Barakat)","Mentioned","contextual","brother of Nathana'el; also courted by Nathan b. Abraham"),

# ---- OS44
("OS44","David (groom, OS44)","Groom","reconstructed","identification uncertain"),
("OS44","Husn (bride, OS44)","Bride","attested",""),

# ---- OS46
("OS46","Husn (bride, OS46)","Bride","attested","only name preserved"),
("OS46","[...] ha-Kohen (OS46)","Witness","attested",""),
("OS46","Jehuda b. Khalaf","Witness","reconstructed","probably; possibly = groom of OS40"),

# ---- formularies with nasi names
("OS52","Semah b. Asa (nasi)","Nasi","attested","'Semah the nasi, son of the nasi Asa'; formula for Karaite woman + Rabbanite man"),
("OS53","Yedidya (nasi)","Nasi","attested","replaced name Anan; not in known nasi lists; perhaps son of Hizkiyahu or Joshya"),

# ---- OS56: mixed ketubba of Rayyisa (Karaite) & Yehya b. Abraham (Rabbanite), 1117, Fustat
("OS56","Yehya b. Abraham","Groom","attested","RABBANITE; son of the physician Abraham; remarriage after divorce"),
("OS56","Abraham (physician, father of Yehya)","GroomFather","attested","'the esteemed physician'"),
("OS56","Rayyisa bt. Sa'adya","Bride","attested","KARAITE; widow, then divorcee remarrying same husband; dowry 719 dinars; had daughter from first marriage"),
("OS56","Sa'adya b. David (father of Rayyisa)","BrideFather","attested","deceased"),
("OS56","Yehoshua ha-Kohen b. Sedaqa ha-Kohen","Agent","attested","bride's agent; 'our Great Prince'; grandfather Yehoshua ha-Kohen the esteemed prince"),
("OS56","Nathan b. Joseph b. Nahorai","WitnessOfAgency","attested","deceased when signed? honorific for dead"),
("OS56","Isaac ha-Parnas b. Sedaqa","WitnessOfAgency","attested",""),
("OS56","David ha-Kohen b. Sedaqa ha-Kohen","Witness","attested","probably brother of the agent"),
("OS56","Sedaqa ha-Levi b. Efraim","Witness","attested",""),
("OS56","Mevorakh b. El'azar b. [...] Yehoshua","Witness","attested",""),
("OS56","Hasdai b. Hizkiyahu (nasi)","Nasi","attested","acting nasi in Fustat 1117"),
("OS56","Hizkiyahu b. Solomon (nasi)","Mentioned","attested","deceased father in nasi clause ('chief of the exile')"),

# ---- OS57: mixed betrothal of Karima bt. Hasan (Karaite) & [...] b. Mansur (Rabbanite), 1030s, Fustat
("OS57","[...] b. Mansur (groom, OS57)","Groom","attested","RABBANITE; first name lost"),
("OS57","Mansur (father of groom, OS57)","GroomFather","attested",""),
("OS57","Karima bt. Hasan","Bride","attested","KARAITE"),
("OS57","Hasan b. Moses","BrideFather","attested","also her agent"),
("OS57","Hasan b. Moses","Agent","attested",""),
("OS57","Sedaqa b. Nahum ha-Kohen","WitnessOfAgency","attested","also witness in Karaite bill of divorce TS 10 J 2.4 (Fustat 1029)"),
("OS57","Moses b. Siba'a","WitnessOfAgency","attested","travelled between Tyre and Fustat; agent in Tyre deed 1019 (PER H 83); witness in Karaite deed of appointment for daughter of David b. Isaac ha-Levi"),
("OS57","Yefet ha-Kohen b. Eli b. Zita","Witness","attested","also witness OS03"),
("OS57","Isaac b. Jehuda ha-Levi","Witness","attested","possibly brother of Joseph b. Jehuda ha-Levi (OS03)"),
("OS57","Sahlawaya b. Hayyim","Witness","attested","the Fustat Karaite banker; ancestor name Abda in signature decoration"),
("OS57","David b. Moses (OS57)","Witness","attested",""),
("OS57","Sa'id b. [...] (OS57)","Witness","attested",""),
("OS57","Efraim b. Mevasser b. Solomon","Scribe","attested","identified as scribe by handwriting"),
("OS57","Efraim b. Mevasser b. Solomon","Witness","attested",""),
("OS57","Mu'ammar b. S[edaqa]","Witness","attested",""),
("OS57","David b. Isaac ha-Levi (Abu Nasr)","Mentioned","contextual","prominent Karaite courtier; his daughter's deed of appointment witnessed by Moses b. Siba'a"),

# ---- Z01: joint Karaite-Rabbanite court session, 13 July 1055, Fustat
("Z01","Eli b. Amram (he-haver)","Judge","attested","RABBANITE judge ('bet din') appointed by the Palestinian yeshiva; leader of Palestinian congregation in Fustat; writer of draft A"),
("Z01","Josiah b. Solomon (nasi)","Judge","attested","KARAITE nasi; the session held at his majlis (moshav); brother of Hizkiyahu b. Solomon"),
("Z01","Josiah b. Solomon (nasi)","Nasi","attested",""),
("Z01","Solomon b. David (nasi)","Mentioned","attested","deceased father of Josiah in the protocol"),
("Z01","Mevorakh b. Israel (heir)","Party","attested","heir, parallel cousin of Samuel; accepted jurisdiction of Jewish courts by qinyan"),
("Z01","Samuel b. Yehuda (the orphan)","Party","attested","minor heir"),
("Z01","Umm Samuel bt. Aaron","Party","attested","mother of Samuel, divorcee of Yehuda b. Tammam; guaranteed not to seek Muslim courts"),
("Z01","Aaron b. Isaac","Guarantor","attested","maternal grandfather of the orphan; stands surety (daman al-darak) for his daughter"),
("Z01","Yehuda b. Tammam","Mentioned","attested","deceased father of Samuel"),
("Z01","Rayyisa bt. Tammam","Mentioned","attested","deceased aunt; apparently a pawnbroker"),
("Z01","Rahma bt. Tammam","Mentioned","attested","deceased aunt; left real estate incl. a new house; gave deed of gift to Mevorakh"),
("Z01","Israel b. Tammam [?]","Mentioned","reconstructed","father of Mevorakh; presumed son of Tammam (parallel cousins)"),
("Z01","Tammam","Mentioned","attested","deceased grandfather; the inheritance is of 'the children of Tammam'"),
("Z01","Abraham b. Solomon (Abu Kathir)","Trustee","attested","RABBANITE court trustee"),
("Z01","Nahray b. Nissim","Trustee","attested","RABBANITE; the famous merchant-scholar of Fustat"),
("Z01","Eli ha-Kohen ha-parnas b. Ya'ish","Trustee","attested","RABBANITE parnas; this document extends his attested activity back to 1055"),
("Z01","David b. Josiah","Mentioned","contextual","son of the nasi Josiah; lived in Fustat; betrothed Bahiyya bt. Solomon b. Sa'adya (L-G Glass 40v)"),
]
