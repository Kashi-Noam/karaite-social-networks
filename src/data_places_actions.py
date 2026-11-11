# -*- coding: utf-8 -*-
"""Closed place list + closed action vocabulary."""

# PLACES: place_id -> (name_en, name_he, category, pgp_name_override_or_None)
# category: document_place = a place where a corpus document was written
#           gazetteer      = origin / activity place referenced in the data
PLACES = {
 "PL00": ("Unknown","לא ידוע","document_place",None),
 "PL01": ("Fustat","פוסטאט","document_place","Fustat"),
 "PL02": ("Cairo","קהיר","document_place","Cairo"),
 "PL03": ("Jerusalem","ירושלים","document_place","Jerusalem"),
 "PL04": ("Ramle","רמלה","document_place","al-Ramla"),
 "PL05": ("Tyre","צור","document_place","Tyre"),
 "PL06": ("Egypt (region)","מצרים (אזור)","document_place","Egypt (region)"),
 "PL07": ("Palestine (region)","ארץ ישראל (אזור)","document_place",None),
 "PL08": ("Acre","עכו","gazetteer","Acre"),
 "PL09": ("Damascus","דמשק","gazetteer","Damascus"),
 "PL10": ("Baghdad","בגדאד","gazetteer","Baghdād"),
 "PL11": ("Aleppo","חלב","gazetteer","Aleppo"),
 "PL12": ("Basra","בצרה","gazetteer","Baṣra"),
 "PL13": ("Tinnis","תניס","gazetteer","Tinnīs"),
 "PL14": ("Ahwaz","אהוואז","gazetteer","Ahwāz"),
 "PL15": ("Tustar (Shustar)","תוסתר","gazetteer",None),
 "PL16": ("Byzantium (region)","ביזנטיון","gazetteer","Byzantium (region)"),
 "PL17": ("Tabaristan","טברסתאן","gazetteer","Ṭabaristān"),
 "PL18": ("Khurasan","ח'וראסאן","gazetteer","Khorasan"),
 "PL19": ("Qirqisiya","קרקיסיה","gazetteer",None),
 "PL20": ("Shiniz","שיניז","gazetteer",None),
 "PL21": ("Zoar","צוער","gazetteer",None),
 "PL22": ("Ana (Euphrates)","ענה","gazetteer",None),
 "PL23": ("Alexandria","אלכסנדריה","gazetteer","Alexandria"),
 "PL24": ("Beirut","ביירות","gazetteer",None),
 "PL25": ("Gaza","עזה","document_place","Gaza"),
}

# raw document place string -> (place_id, certainty, place_id2, note)
DOC_PLACE = {
 "Fustat":       ("PL01","certain",None,""),
 "Fustat [?]":   ("PL01","probable",None,"editors' suggestion"),
 "Cairo":        ("PL02","certain",None,""),
 "Cairo [?]":    ("PL02","probable",None,""),
 "Jerusalem":    ("PL03","certain",None,""),
 "Jerusalem/Ramle": ("PL03","certain","PL04","formulary intended for Jerusalem and for Ramle"),
 "Ramle":        ("PL04","certain",None,""),
 "Ramle [?]":    ("PL04","probable",None,""),
 "Tyre [?]":     ("PL05","probable",None,""),
 "Egypt":        ("PL06","certain",None,"country only"),
 "Egypt [?]":    ("PL06","probable",None,""),
 "Palestine [?]":("PL07","probable",None,""),
 "Gaza":         ("PL25","certain",None,""),
 "n.p.":         ("PL00","unknown",None,"place not preserved"),
 "":             ("PL00","unknown",None,""),
}

# person -> origin/nisba place (only where the sources state it explicitly)
PERSON_ORIGIN = {
 "Yefet b. Abraham al-Tustari": "PL15",
 "Abraham (Abu Sa'ad) b. Sahl al-Tustari": "PL15",
 "Hesed (Abu Nasr) b. Sahl al-Tustari": "PL15",
 "Aaron b. Sahl al-Tustari": "PL15",
 "Sahl (Yashar) b. Israel al-Tustari": "PL15",
 "Israel b. Jacob al-Tustari": "PL15",
 "Joseph b. Israel al-Tustari": "PL15",
 "Sa'id b. Israel al-Tustari": "PL15",
 "Hana bt. Israel al-Tustari": "PL14",
 "Samuel b. Joseph al-Basri": "PL12",
 "Shela b. Amram al-Qirqisani": "PL19",
 "Amram al-Qirqisani": "PL19",
 "Hiba b. Khalaf al-Shinizi": "PL20",
 "Menahem b. Job al-Halabi": "PL11",
 "Sahl b. Sa'adya al-Baghdadi": "PL10",
 "Solomon b. Aaron al-Baghdadi": "PL10",
 "Sedaqa b. Amram (Damascus)": "PL09",
 "Menashe b. Mahbub ha-Levi (of Acre)": "PL08",
 "Eli b. Isma'il al-Bairuti (the scholar)": "PL24",
 "Joseph (father of Rivqa)": "PL16",
 "Tovya b. Moses": "PL16",
 "Israel b. Simha of Basra": "PL12",
 "Samuel b. Sahl": "PL18",
 "Solomon b. Mevasser b. Sahl al-Ani": "PL22",
 "Yesha'ya b. Sahl al-Ani": "PL22",
 "Mevasser b. Sahl al-Ani": "PL22",
 "Sahl al-Ani": "PL22",
 "Yeshu'a b. Joseph (Alexandria)": "PL23",
 "Efraim b. Sa'id b. Malachi": "PL14",
 "Jabir b. Azhar ha-Kohen": "PL13",
}

# ACTIONS: closed vocabulary of what a person DOES in a document.
# action_id -> (en, he, definition, action_class)
ACTIONS = {
 "ACT01": ("Groom","חתן","contracts the betrothal/marriage as husband","Party"),
 "ACT02": ("Bride","כלה","is betrothed/married; accepts the marriage and its conditions","Party"),
 "ACT03": ("LegalParty","צד משפטי","litigant, heir or claimant in a legal proceeding","Party"),
 "ACT04": ("Guarantor","ערב","stands surety (daman al-darak) for another party","Party"),
 "ACT05": ("Agent","שליח (פקיד)","represents a party - receives the mohar, contracts on her/his behalf","Representation"),
 "ACT06": ("WitnessOfAgency","עד מינוי שליח","witnesses the appointment of the agent","Attestation"),
 "ACT07": ("Witness","עד חותם","signs the document as witness","Attestation"),
 "ACT08": ("Scribe","סופר","writes the document","Attestation"),
 "ACT09": ("Declarant","מצהיר בפני בית דין","declares/confirms before the court (court copies, certifications)","Attestation"),
 "ACT10": ("Judge","דיין / אב בית דין","presides over the session; examines and certifies deeds","Court"),
 "ACT11": ("Trustee","נאמן בית דין","court-appointed trustee over property","Court"),
 "ACT12": ("NamedNasi","נשיא מכהן","the reigning nasi named in the dating clause","Reference"),
 "ACT13": ("FamilyMention","נזכר כבן משפחה","parent/grandparent named in a party's genealogy","Reference"),
 "ACT14": ("DocumentMention","נזכר במסמך","any other person named in the document text","Reference"),
 "ACT15": ("ScholarlyMention","נזכר בהערות המהדיר","person known only from the editors' commentary/footnotes on this document","Reference"),
}

# role -> action_id (Mentioned is resolved by certainty at build time)
ROLE2ACTION = {
 "Groom":"ACT01","Bride":"ACT02","Party":"ACT03","Guarantor":"ACT04",
 "Agent":"ACT05","GroomAgent":"ACT05",
 "WitnessOfAgency":"ACT06","Witness":"ACT07","Scribe":"ACT08","Declarant":"ACT09",
 "Judge":"ACT10","Trustee":"ACT11","Nasi":"ACT12",
 "GroomFather":"ACT13","BrideFather":"ACT13","BrideGrandfather":"ACT13","GroomGrandfather":"ACT13",
 # "Mentioned": ACT14 if attested/reconstructed, ACT15 if contextual
}

# closed relation-type vocabulary (relations.csv)
RELATION_TYPES = {
 "married": "בני זוג נשואים",
 "betrothed": "מאורסים",
 "divorced": "גרושים",
 "first_husband_of": "בעל ראשון של",
 "father_of": "אב של",
 "mother_of": "אם של",
 "sibling_of": "אח/אחות של",
 "first_cousin_of": "בן/בת דוד של",
 "uncle_of": "דוד של",
 "ancestor_of": "אב קדמון של (סב ומעלה)",
 "son_in_law_of": "חתן של",
 "agent_for": "שליח של",
 "gave_gift_to": "העניק מתנה ל",
 "business_associate_of": "שותף עסקי של",
 "corresponded_with": "התכתב עם",
 "colleague_of": "עמית של",
 "rival_of": "יריב של",
 "patron_of": "פטרון של",
 "teacher_of": "מורה של",
 "associated_with": "קשור אל (קשר מתועד אחר)",
}
