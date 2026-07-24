#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 1 of the pipeline: extract machine-readable text from the two source PDFs
and split the book's document-edition section into per-document files.

Sources (NOT included in this repository for copyright reasons):
  - Olszowy-Schlanger, Judith. "Karaite Marriage Documents from the Cairo Geniza"
    (Brill, 1998). Scanned PDF with an OCR text layer, 554 pages.
  - Zinger, Oded. "A Karaite-Rabbanite Court Session in mid-Eleventh Century Egypt",
    Ginzei Qedem 13 (2017). Born-digital PDF.

Usage:
    python3 extraction/extract_texts.py /path/to/book.pdf /path/to/zinger.pdf

Output (git-ignored, since the text is copyrighted):
    text/book.txt          full book text (pdftotext -layout)
    text/zinger.txt        full article text
    text/docs/doc_NN.txt   one file per edited document (n. 1-57), with the
                           Hebrew transcription blocks stripped (OCR noise);
                           what remains is the English description, translation
                           and the editor's commentary - the harvesting sources.

Requires poppler-utils (pdftotext).
"""
import os, re, subprocess, sys

def main(book_pdf, zinger_pdf, outdir="text"):
    os.makedirs(f"{outdir}/docs", exist_ok=True)
    subprocess.run(["pdftotext", "-layout", book_pdf, f"{outdir}/book.txt"], check=True)
    subprocess.run(["pdftotext", "-layout", zinger_pdf, f"{outdir}/zinger.txt"], check=True)

    lines = open(f"{outdir}/book.txt", encoding="utf-8").read().split("\n")

    # The edition section ("TEXTS: N 1 TO 57") spans lines ~12578-21897 in the
    # -layout extraction of the 1998 print. Locate it dynamically:
    start = next(i for i, l in enumerate(lines) if re.search(r"^\s*TEXTS\s*$", l))
    end = next(i for i, l in enumerate(lines) if re.search(r"^\s*ABBREVIATIONS\s*$", l.strip()) and i > start)
    sec = lines[start:end]

    # Document boundaries: standalone "N X" headers and "TEXTS: N X" page headers.
    pat_stand = re.compile(r"^\s*[NW][°o0\"']?\s*(\d+)\s*$")
    pat_page = re.compile(r"TEXTS:\s*N[°oO0]?\s*(\d+)")
    docnum, docs = None, {}
    for ln in sec:
        m = pat_stand.match(ln) or pat_page.search(ln)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 57:
                docnum = n
        if docnum:
            docs.setdefault(docnum, []).append(ln)

    # Strip the Hebrew transcription blocks (between a standalone "Text" line
    # and the next "Textual notes"/"Translation" heading) - they are OCR noise.
    for n, dl in docs.items():
        out, skip = [], False
        for ln in dl:
            s = ln.strip()
            if s in ("Text", "Texts"):
                skip = True
                continue
            if s.lower().startswith("textual notes") or s == "Translation":
                skip = False
            if not skip:
                out.append(ln)
        txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
        open(f"{outdir}/docs/doc_{n:02d}.txt", "w", encoding="utf-8").write(txt)

    print(f"book: {len(lines)} lines; documents split: {sorted(docs)}")
    missing = [i for i in range(1, 58) if i not in docs]
    if missing:
        print(f"NOTE: page headers for docs {missing} were not detected; "
              f"their text is embedded in the neighbouring file (e.g. n.10 in doc_09) - "
              f"harvested manually.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
