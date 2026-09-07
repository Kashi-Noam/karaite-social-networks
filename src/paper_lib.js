// Shared helpers and numbers for the Hebrew paper (make_paper_v7.js).
// Every figure comes from src/figures.py and every number from
// networks/paper_numbers.json, which src/backbone.py writes.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, LevelFormat, PageBreak,
  Footer, PageNumber, FootnoteReferenceRun
} = require("docx");

const N = JSON.parse(fs.readFileSync("../networks/paper_numbers.json", "utf8"));
const FIG = "../figures/";
const FONT = "David";
const SZ = 24;      // 12pt
const LINE = 360;   // 1.5

const T = (t, o = {}) => new TextRun({ text: t, rightToLeft: true, font: FONT, size: SZ, ...o });
const B = (t, o = {}) => T(t, { bold: true, ...o });
const L = (t, o = {}) => new TextRun({ text: t, rightToLeft: false, font: "Cambria", size: SZ - 2, ...o });
const M = (t, o = {}) => new TextRun({ text: t, rightToLeft: false, font: "Consolas", size: SZ - 6, ...o });
const FN = n => new FootnoteReferenceRun(n);

const P = (c, o = {}) => new Paragraph({
  children: Array.isArray(c) ? c : [T(c)], bidirectional: true,
  alignment: AlignmentType.JUSTIFIED, spacing: { after: 110, line: LINE }, ...o
});
const H1 = t => new Paragraph({
  children: [T(t, { bold: true, size: 30, color: "1F3864" })], bidirectional: true,
  alignment: AlignmentType.RIGHT, spacing: { before: 300, after: 130 }, outlineLevel: 0
});
const H2 = t => new Paragraph({
  children: [T(t, { bold: true, size: 26, color: "2E5C8A" })], bidirectional: true,
  alignment: AlignmentType.RIGHT, spacing: { before: 220, after: 100 }, outlineLevel: 1
});
const fnp = c => new Paragraph({ children: c, bidirectional: true, alignment: AlignmentType.JUSTIFIED });

function pngSizePx(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }
const fig = (file, caption, w = 600) => {
  const buf = fs.readFileSync(FIG + file);
  const { w: pw, h: ph } = pngSizePx(buf);
  return [
    new Paragraph({
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: w, height: Math.round(w * ph / pw) } })],
      alignment: AlignmentType.CENTER, spacing: { before: 150, after: 50 }
    }),
    new Paragraph({
      children: [T(caption, { size: 19, italics: true })], bidirectional: true,
      alignment: AlignmentType.CENTER, spacing: { after: 190 }
    })
  ];
};

function tbl(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (c, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: "E8EEF7", color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 20 },
      children: [typeof c === "string" ? (head ? B(c, { size: 20 }) : T(c, { size: 20 })) : c]
    })]
  });
  return new Table({
    columnWidths: widths, width: { size: total, type: WidthType.DXA }, visuallyRightToLeft: true,
    rows: [new TableRow({ tableHeader: true, cantSplit: true, children: headers.map((h, i) => cell(h, i, true)) }),
    ...rows.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, i, false)) }))]
  });
}
const CAP = t => new Paragraph({
  children: [T(t, { size: 19, italics: true })], bidirectional: true,
  alignment: AlignmentType.CENTER, spacing: { before: 60, after: 190 }
});
const REF = c => new Paragraph({
  children: Array.isArray(c) ? c : [c], bidirectional: false, alignment: AlignmentType.LEFT,
  spacing: { after: 70, line: 300 }, indent: { left: 420, hanging: 420 }
});
// The page-number field docx-js builds here is packed into one run, which Word
// rejects; src/fix_docx.py splits it after the file is written.
const makeFooter = () => new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })]
  })]
});

// ---------------------------------------------------------------- numbers
const net = N.networks.presence;
const netN = N.networks.presence_plus_nasi;
const bb = N.backbone;
const ep = N.eligible_pairs;
const pool = N.pool;
const tit = N.titles;
const reg = N.attesters_by_region.summary;
const regC = N.attesters_by_region.excluding_court_copies;
const kv = N.ketubka_vs_betrothal || N.ketubba_vs_betrothal;
const wm = N.women;
const kin = N.kinship;
const sect = N.sects;
const ag = N.agents;
const out = N.outside_corpus;
const brk = N.brokers.presence;
const brkN = N.brokers.presence_plus_nasi;
const he = n => String(n);

module.exports = { T, B, L, M, FN, P, H1, H2, fnp, fig, tbl, CAP, REF, makeFooter,
  N, net, netN, bb, ep, pool, tit, reg, regC, kv, wm, kin, sect, ag, out, brk, brkN, he,
  Document, Packer, Paragraph, TextRun, AlignmentType, PageBreak, LevelFormat, fs };
