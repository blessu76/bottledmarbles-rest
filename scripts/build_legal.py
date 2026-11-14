#!/usr/bin/env python3
"""Builds /privacy/ and /terms/ (en) + /ko/privacy/ and /ko/terms/ — stdlib only.

  python3 scripts/build_legal.py            # write into this repo
  python3 scripts/build_legal.py --check    # fail if the committed pages differ from the build
  python3 scripts/build_legal.py --root DIR

Source: content/legal/<doc>/<lang>.md ("---\\ntitle: ..\\ndescription: ..\\neffective: YYYY-MM-DD\\n---\\n" + body; same body subset as the
journal, bare e-mail addresses become mailto links). Only the languages in chrome.LEGAL_LANGS have pages; the footer of every other
language links the English pages. The header is the journal's (home + journal links + language select), the footer is the shared legal footer.
"""
import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_journal as bj  # noqa: E402
import chrome  # noqa: E402

SITE = bj.SITE
DOCS = ("privacy", "terms")
LANGS = chrome.LEGAL_LANGS
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
EFFECTIVE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def lpath(doc, lang):
    return chrome.legal_path(doc, lang)


def load(root):
    out = {}
    for doc in DOCS:
        for lang in LANGS:
            f = Path(root) / "content" / "legal" / doc / ("%s.md" % lang)
            if not f.is_file():
                raise SystemExit("build_legal: %s missing" % f)
            meta, body = bj.parse_meta(f.read_text(encoding="utf-8"), ("title", "description", "effective"), "%s/%s.md" % (doc, lang))
            if not EFFECTIVE_RE.match(meta["effective"]):
                raise SystemExit("build_legal: %s/%s.md bad effective date" % (doc, lang))
            out[(doc, lang)] = (meta, body)
    return out


def _body(body):
    h = bj.body_html(body)
    return EMAIL_RE.sub(lambda m: '<a href="mailto:%s">%s</a>' % (m.group(0), m.group(0)), h)


def page(doc, lang, docs, root):
    st = bj._strings(root)
    meta, body = docs[(doc, lang)]
    other = "terms" if doc == "privacy" else "privacy"
    alts = [(l, lpath(doc, l)) for l in LANGS]
    canon = SITE + lpath(doc, lang)
    head = bj._head(lang, "%s — Bottled Marbles" % meta["title"], meta["description"], canon, alts)
    opts = [(l, lpath(doc, l), st[l]["name"]) for l in LANGS]
    home = "/" if lang == "en" else "/%s/" % lang
    header = chrome.header([(home, bj.UI[lang]["home"], False), (bj.jpath(lang), st[lang]["journal"], False)],
                           chrome.lang_select(opts, lang, st[lang]["lang_label"]))
    main = '<main class="journal">\n<article>\n<h1>%s</h1>\n%s\n</article>\n<p class="back"><a href="%s">%s</a></p>\n</main>\n' % (
        html.escape(meta["title"]), _body(body), lpath(other, lang), html.escape(st[lang][other]))
    return head + "<body>\n" + header + "\n" + main + bj._foot(root, lang)


def sitemap_rows(root):
    rows = []
    for doc in DOCS:
        links = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l, SITE, lpath(doc, l)) for l in LANGS)
        links += '<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, lpath(doc, "en"))
        for l in LANGS:
            rows.append("<url><loc>%s%s</loc>%s</url>" % (SITE, lpath(doc, l), links))
    return rows


def render(root):
    docs = load(root)
    return {lpath(d, l).strip("/") + "/index.html": page(d, l, docs, root) for d in DOCS for l in LANGS}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the privacy and terms pages.")
    ap.add_argument("--root", default=str(HERE.parent))
    ap.add_argument("--check", action="store_true", help="fail if committed pages differ from the build")
    a = ap.parse_args(argv)
    root = Path(a.root)
    pages = render(root)
    if a.check:
        bad = [r for r, t in pages.items() if not (root / r).is_file() or (root / r).read_text(encoding="utf-8") != t]
        if bad:
            print("build_legal --check: out of date: %s" % ", ".join(sorted(bad)), file=sys.stderr)
            return 1
        print("legal up to date: %d pages" % len(pages))
        return 0
    for rel, text in pages.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print("legal built: %d pages" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
