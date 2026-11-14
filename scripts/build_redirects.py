#!/usr/bin/env python3
"""Builds static redirect stubs for retired-language addresses — /pt /zh /ar /hi /ru — stdlib only.

  python3 scripts/build_redirects.py            # write into this repo
  python3 scripts/build_redirects.py --root DIR # write into DIR

Rules follow ipe_web_kit redirects.py v0.7.0 (Davy-confirmed): pt→/pt-BR/ · zh→/zh-Hant/ · ar·hi·ru→/ (English is the site root).
GitHub Pages has no server redirects, so every stub is meta refresh + location.replace (query and hash kept) + canonical
+ noindex,follow + a visible link. Stubs cover the home and /journal/ of each retired language; they are never in sitemap/hreflang.
"""
import argparse
import html
import sys
from pathlib import Path

SITE = "https://bottledmarbles.ipe.rest"
LEGACY = {"pt": "pt-BR", "zh": "zh-Hant", "ar": "en", "hi": "en", "ru": "en"}
PATHS = ("", "journal/")


def target(old, rest):
    new = LEGACY[old]
    return "/" + rest if new == "en" else "/%s/%s" % (new, rest)


def stub(old, rest):
    dest = target(old, rest)
    url = html.escape(SITE + dest, quote=True)
    new = LEGACY[old]
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
        % (html.escape(new), url, url, html.escape(dest, quote=True), url, url)
    )


def render():
    """-> {relative path: html} e.g. 'pt/index.html', 'ru/journal/index.html'."""
    return {"%s/%sindex.html" % (old, rest): stub(old, rest) for old in LEGACY for rest in PATHS}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build redirect stubs for retired-language addresses.")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    root = Path(ap.parse_args(argv).root)
    out = render()
    for rel, text in out.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print("redirect stubs built: %d pages" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
