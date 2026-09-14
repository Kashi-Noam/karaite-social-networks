"""Repair the two things docx-js writes that Word refuses to open.

LibreOffice reads both without complaint, which is why they survive a
PDF proof; Word rejects the file outright ("Word found unreadable
content", then "Word experienced an error trying to open the file").

1. Drawing ids.  docx-js stamps every ImageRun with <wp:docPr id="1">,
   so a document with ten figures has ten objects claiming id 1.
   Word requires them to be unique.

2. Complex fields.  docx-js packs a whole PAGE field into a single run:

       <w:r><w:rPr/>
         <w:fldChar w:fldCharType="begin"/>
         <w:instrText>PAGE</w:instrText>
         <w:fldChar w:fldCharType="separate"/>
         <w:fldChar w:fldCharType="end"/>
       </w:r>

   ECMA-376 puts each of those in a run of its own.  This splits them,
   copying the run properties onto each piece.

Both fixes rewrite word/*.xml in place and leave every other part of the
package byte-identical.

Usage:  python3 fix_docx.py "../docs/<name>.docx"
"""

import copy
import sys
import zipfile

import lxml.etree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
PIC = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"
FIELD = (W + "fldChar", W + "instrText")

PARTS = ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml",
         "word/comments.xml")

CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"
MEDIA_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
               "gif": "image/gif", "bmp": "image/bmp", "tiff": "image/tiff",
               "svg": "image/svg+xml", "emf": "image/x-emf",
               "wmf": "image/x-wmf"}


def declare_missing_content_types(parts):
    """Every part in the package needs a content type, by extension Default or
    by PartName Override.  Word refuses to open a package where one is missing,
    and an editing round-trip can silently drop a Default that is momentarily
    unused - which is how a JPEG added later ends up breaking the file."""
    ctypes = next(d for i, d in parts if i.filename == "[Content_Types].xml")
    root = ET.fromstring(ctypes)
    defaults = {e.get("Extension", "").lower() for e in root.iter(CT + "Default")}
    overrides = {e.get("PartName") for e in root.iter(CT + "Override")}
    added = []
    for info, _ in parts:
        name = info.filename
        if name.endswith("/") or "/" + name in overrides:
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        if ext in defaults or ext not in MEDIA_TYPES:
            continue
        el = ET.SubElement(root, CT + "Default")
        el.set("Extension", ext)
        el.set("ContentType", MEDIA_TYPES[ext])
        defaults.add(ext)
        added.append(ext)
    if not added:
        return None, []
    return ET.tostring(root, xml_declaration=True, encoding="UTF-8",
                       standalone=True), added


def number_drawings(root):
    """Give every drawing object a unique id.  Returns how many."""
    total = 0
    for tag in (WP + "docPr", PIC + "cNvPr"):
        n = 0
        for el in root.iter(tag):
            n += 1
            el.set("id", str(n))
            el.set("name", "Picture %d" % n)
        total = max(total, n)
    return total


def split_field_runs(root):
    """Put each fldChar / instrText in a run of its own.  Returns how many."""
    fixed = 0
    for run in list(root.iter(W + "r")):
        pieces = [k for k in run if k.tag in FIELD]
        if len(pieces) < 2:
            continue
        parent = run.getparent()
        at = list(parent).index(run)
        props = run.find(W + "rPr")
        for offset, piece in enumerate(pieces):
            new = ET.SubElement(parent, W + "r")
            if props is not None:
                new.append(copy.deepcopy(props))
            run.remove(piece)
            new.append(piece)
            parent.remove(new)
            parent.insert(at + offset, new)
        parent.remove(run)
        fixed += 1
    return fixed


def fix(path):
    src = zipfile.ZipFile(path)
    parts = [(info, src.read(info.filename)) for info in src.infolist()]
    src.close()

    report, rebuilt = {}, {}
    for info, data in parts:
        name = info.filename
        if not (name in PARTS or name.startswith("word/footer")
                or name.startswith("word/header")):
            continue
        root = ET.fromstring(data)
        drawings = number_drawings(root)
        fields = split_field_runs(root)
        if drawings or fields:
            report[name] = (drawings, fields)
            rebuilt[name] = ET.tostring(root, xml_declaration=True,
                                        encoding="UTF-8", standalone=True)

    ct, added = declare_missing_content_types(parts)
    if ct is not None:
        rebuilt["[Content_Types].xml"] = ct
        report["[Content_Types].xml"] = (0, 0, added)

    if not rebuilt:
        return report

    out = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED)
    for info, data in parts:
        item = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        item.compress_type = info.compress_type
        item.external_attr = info.external_attr
        out.writestr(item, rebuilt.get(info.filename, data))
    out.close()
    return report


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        for name, entry in sorted(fix(arg).items()):
            if len(entry) == 3:
                print("fix_docx: %s  %s  content types declared: %s"
                      % (arg, name, ", ".join(entry[2])))
            else:
                print("fix_docx: %s  %s  %d drawings numbered, %d field runs split"
                      % (arg, name, entry[0], entry[1]))
