#!/usr/bin/env python3
"""Builds the 12-language landing: index.html (en) + <lang>/index.html, and sitemap.xml — stdlib only.

  python3 scripts/build_landing.py            # write into this repo
  python3 scripts/build_landing.py --root DIR # write into DIR

Inputs: games.json "langs" (order = picker order, first = default) and content/landing.json "strings".
Language rules follow ipe_web_kit languages.py v0.5.1 (kit-0029): resolve() below is a port of it.
"""
import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_journal  # noqa: E402
import chrome  # noqa: E402

HERE = Path(__file__).resolve().parent
SITE = "https://bottledmarbles.ipe.rest"
DEFAULT = "en"
ASSET_V = "20261114a"
KEYS = ("name", "genre", "tagline", "body", "f1", "f2", "f3", "store", "lang_label", "journal", "privacy", "terms")
MARBLES = ("c1", "c2", "c3", "c4", "c5", "c6")
BOTTLES = (("c1", "c2", "c3"), ("c4", "c5", "c6"), ())

_ZH_HANT_REGIONS = {"tw", "hk", "mo"}


def _split(tag):
    return [p for p in str(tag or "").strip().lower().replace("_", "-").split("-") if p]


def resolve(tag, supported):
    parts = _split(tag)
    if not parts:
        return DEFAULT
    code = "id" if parts[0] == "in" else parts[0]
    rest = parts[1:]
    if code == "zh":
        script = next((p for p in rest if len(p) == 4 and p.isalpha()), None)
        region = next((p for p in rest if len(p) == 2 and p.isalpha()), None)
        hant = script == "hant" or (script is None and region in _ZH_HANT_REGIONS)
        return "zh-Hant" if hant else DEFAULT
    if code == "pt":
        return "pt-BR"
    for lang in supported:
        if lang.lower() == code:
            return lang
    return DEFAULT


def load(root):
    root = Path(root)
    games = json.loads((root / "games.json").read_text(encoding="utf-8"))
    langs = tuple(games["langs"])
    strings = json.loads((root / "content" / "landing.json").read_text(encoding="utf-8"))["strings"]
    if not langs or langs[0] != DEFAULT or len(set(langs)) != len(langs):
        raise SystemExit("build_landing: games.json langs must be unique and start with %s" % DEFAULT)
    for l in langs:
        missing = [k for k in KEYS if not strings.get(l, {}).get(k)]
        if missing:
            raise SystemExit("build_landing: %s missing %s" % (l, ", ".join(missing)))
    return langs, strings


def ppath(lang):
    return "/" if lang == DEFAULT else "/%s/" % lang


def _e(s):
    return html.escape(s, quote=True)


def _picker(langs, strings, cur):
    return chrome.lang_select([(l, ppath(l), strings[l]["name"]) for l in langs], cur, strings[cur]["lang_label"])


def _alternates(langs):
    out = ['<link rel="alternate" hreflang="%s" href="%s%s">' % (l, SITE, ppath(l)) for l in langs]
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, ppath(DEFAULT)))
    return "\n".join(out)


def _page(lang, langs, strings):
    s = strings[lang]
    bottles = "".join('<span class="bottle">%s</span>' % "".join('<i class="%s"></i>' % c for c in b)
                      for b in BOTTLES)
    feats = "".join("<li>%s</li>" % _e(s[k]) for k in ("f1", "f2", "f3"))
    return """<!doctype html>
<html lang="{lang}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bottled Marbles: {genre}</title>
<meta name="description" content="{body}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="Bottled Marbles: {genre}">
<meta property="og:description" content="{body}">
<meta property="og:url" content="{canon}">
{alts}
<link rel="stylesheet" href="/assets/landing.css?v={v}">
<script src="/assets/landing.js?v={v}" defer></script>
</head>
<body>
<header class="top">{picker}</header>
<main>
<section class="hero">
<div class="bottles" aria-hidden="true">{bottles}</div>
<h1>Bottled Marbles</h1>
<p class="genre">{genre}</p>
<p class="tagline">{tagline}</p>
<p class="body">{body}</p>
</section>
<ul class="features">{feats}</ul>
<div class="cta">
<span class="store" aria-disabled="true">{store}</span>
<a class="rel" href="{jhref}">{journal}</a>
</div>
</main>
<footer>{legal}<p><a href="{jhref}">{journal}</a> · ipe() 2026</p></footer>
</body>
</html>
""".format(
        lang=lang,
        genre=_e(s["genre"]),
        body=_e(s["body"]),
        tagline=_e(s["tagline"]),
        canon=SITE + ppath(lang),
        alts=_alternates(langs),
        v=ASSET_V,
        legal=chrome.legal_links(s["privacy"], s["terms"]),
        picker=_picker(langs, strings, lang),
        bottles=bottles,
        feats=feats,
        store=_e(s["store"]),
        journal=_e(s["journal"]),
        jhref=build_journal.jpath("ko" if lang == "ko" else "en"),
    )


def _sitemap(langs, extra=()):
    rows = []
    for l in langs:
        links = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (k, SITE, ppath(k)) for k in langs)
        links += '<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, ppath(DEFAULT))
        rows.append("<url><loc>%s%s</loc>%s</url>" % (SITE, ppath(l), links))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n') % "\n".join(list(rows) + list(extra))


def render(root):
    """-> {relative path: text} for every generated file."""
    langs, strings = load(root)
    out = {"sitemap.xml": _sitemap(langs, build_journal.sitemap_rows(root))}
    for l in langs:
        rel = "index.html" if l == DEFAULT else "%s/index.html" % l
        out[rel] = _page(l, langs, strings)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the landing pages from games.json and content/landing.json.")
    ap.add_argument("--root", default=str(HERE.parent), help="site repo root (default: this repo)")
    a = ap.parse_args(argv)
    root = Path(a.root)
    for rel, text in render(root).items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print("landing built: %d pages" % len(load(root)[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
