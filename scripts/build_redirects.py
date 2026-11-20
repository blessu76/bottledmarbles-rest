#!/usr/bin/env python3
"""Builds static redirect stubs — stdlib only.

  python3 scripts/build_redirects.py            # write into this repo
  python3 scripts/build_redirects.py --check    # fail if the committed stubs differ from the build
  python3 scripts/build_redirects.py --root DIR # write into DIR

Two groups:
- Retired-language addresses — /pt /zh /ar /hi /ru. Rules follow ipe_web_kit redirects.py v0.7.0 (Davy-confirmed):
  pt→/pt-BR/ · zh→/zh-Hant/ · ar·hi·ru→/ (English is the site root). Stubs cover the home and /journal/ of each retired language.
- Privacy / terms — /privacy/ /terms/ /ko/privacy/ /ko/terms/. ipe.rest/legal is the source of truth (Davy 2026-11-20, A안),
  so these stubs only hand the reader on to https://ipe.rest/legal/<doc>/ (ko: https://ipe.rest/ko/legal/<doc>/).

GitHub Pages has no server redirects, so every stub is meta refresh + location.replace (query and hash kept) + canonical
+ noindex,follow + a visible link, and no GA4 tag. Stubs are never in sitemap/hreflang (tested).
"""
import argparse
import html
import sys
from pathlib import Path

SITE = "https://bottledmarbles.ipe.rest"
IPE = "https://ipe.rest"
LEGACY = {"pt": "pt-BR", "zh": "zh-Hant", "ar": "en", "hi": "en", "ru": "en"}
PATHS = ("", "journal/")
LEGAL = ("privacy", "terms")


def target(old, rest):
    new = LEGACY[old]
    return "/" + rest if new == "en" else "/%s/%s" % (new, rest)


def legal_target(doc, lang):
    return "%s%s/legal/%s/" % (IPE, "/ko" if lang == "ko" else "", doc)


def stub(lang, dest):
    """dest = a site-relative path (retired languages) or an absolute ipe.rest URL (legal)."""
    url = dest if dest.startswith("http") else SITE + dest
    return (
        '<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Redirecting…</title>\n<meta name="robots" content="noindex,follow">\n'
        '<link rel="canonical" href="%s">\n<meta http-equiv="refresh" content="0; url=%s">\n'
        '<style>body{margin:0;padding:24px 16px;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;'
        'color:#1a1a1a;background:#fff;text-align:center;overflow-wrap:anywhere}a{color:#2f5d50}'
        '@media(prefers-color-scheme:dark){body{color:#ececec;background:#111214}a{color:#8cc7b4}}</style>\n'
        '<script>location.replace("%s"+location.search+location.hash)</script>\n'
        '</head>\n<body>\n<p><a href="%s">%s</a></p>\n</body>\n</html>\n'
        % (html.escape(lang), html.escape(url, quote=True), html.escape(url, quote=True),
           html.escape(dest, quote=True), html.escape(url, quote=True), html.escape(url, quote=True))
    )


def render():
    """-> {relative path: html} e.g. 'pt/index.html', 'ru/journal/index.html', 'ko/privacy/index.html'."""
    out = {"%s/%sindex.html" % (old, rest): stub(LEGACY[old], target(old, rest)) for old in LEGACY for rest in PATHS}
    for doc in LEGAL:
        for lang, rel in (("en", "%s/" % doc), ("ko", "ko/%s/" % doc)):
            out[rel + "index.html"] = stub(lang, legal_target(doc, lang))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build redirect stubs (retired languages, legal pages).")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--check", action="store_true", help="fail if committed stubs differ from the build")
    a = ap.parse_args(argv)
    root = Path(a.root)
    out = render()
    if a.check:
        bad = [r for r, t in out.items() if not (root / r).is_file() or (root / r).read_text(encoding="utf-8") != t]
        if bad:
            print("build_redirects --check: out of date: %s" % ", ".join(sorted(bad)), file=sys.stderr)
            return 1
        print("redirect stubs up to date: %d pages" % len(out))
        return 0
    for rel, text in out.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print("redirect stubs built: %d pages" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
