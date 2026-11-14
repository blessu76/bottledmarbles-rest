#!/usr/bin/env python3
"""Builds the journal: /journal/ (en) + /ko/journal/, one page per post, and the sitemap rows — stdlib only (Python 3.9+).

  python3 scripts/build_journal.py            # write into this repo
  python3 scripts/build_journal.py --check    # fail if the committed pages differ from the build
  python3 scripts/build_journal.py --root DIR

Source: content/journal/<slug>/<lang>.md for the 12 site languages (LANGS)  =
"---\\ntitle: ..\\ndate: YYYY-MM-DD\\ntime: HH:MM\\nsummary: ..\\ncopy_review: iris YYYY-MM-DD\\n---\\n" + body.
Body subset: paragraphs, "## " headings, "- " lists, **bold**, `code`. en is required; a post is PUBLISHED (publish_next.py) only with all 12
files and copy_review in each. Pages exist only for the languages a post has; a language's journal index shows an untranslated
post as its English card (linking to /journal/<slug>/).
date/time = the real publish moment in KST (stamped by scripts/publish_next.py, never back-dated; the build refuses a future date).
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

import chrome

HERE = Path(__file__).resolve().parent
SITE = "https://bottledmarbles.ipe.rest"
ASSET_V = "20261114b"
LANGS = ("en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr")
REVIEW_RE = re.compile(r"^iris( \d{4}-\d{2}-\d{2})?$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KST = dt.timezone(dt.timedelta(hours=9))
UI = {
    "en": {"home": "Bottled Marbles", "lead": "How Bottled Marbles gets made: decisions, dead ends and fixes, one post a day.", "back": "All posts", "by": "Posted"},
    "ko": {"home": "구슬병", "lead": "구슬병(Bottled Marbles)을 만드는 과정 — 결정, 막힌 곳, 고친 방법을 하루 한 편씩.", "back": "전체 글", "by": "발행"},
    "ja": {"home": "ビー玉ボトル", "lead": "Bottled Marbles ができるまで：決めたこと、行き詰まったこと、直したことを一日一本ずつ。", "back": "すべての記事", "by": "公開"},
    "zh-Hant": {"home": "彈珠瓶", "lead": "Bottled Marbles 的製作過程：決定、卡關與修正，每天一篇。", "back": "所有文章", "by": "發布"},
    "es": {"home": "Bottled Marbles", "lead": "Cómo se hace Bottled Marbles: decisiones, callejones sin salida y arreglos, una entrada al día.", "back": "Todas las entradas", "by": "Publicado"},
    "pt-BR": {"home": "Bottled Marbles", "lead": "Como o Bottled Marbles é feito: decisões, becos sem saída e correções, um post por dia.", "back": "Todos os posts", "by": "Publicado"},
    "fr": {"home": "Bottled Marbles", "lead": "Comment Bottled Marbles se fabrique : décisions, impasses et corrections, un billet par jour.", "back": "Tous les billets", "by": "Publié"},
    "de": {"home": "Bottled Marbles", "lead": "Wie Bottled Marbles entsteht: Entscheidungen, Sackgassen und Korrekturen, ein Beitrag pro Tag.", "back": "Alle Beiträge", "by": "Veröffentlicht"},
    "id": {"home": "Bottled Marbles", "lead": "Bagaimana Bottled Marbles dibuat: keputusan, jalan buntu, dan perbaikan, satu tulisan per hari.", "back": "Semua tulisan", "by": "Diterbitkan"},
    "th": {"home": "Bottled Marbles", "lead": "เบื้องหลังการสร้าง Bottled Marbles: การตัดสินใจ ทางตัน และการแก้ไข วันละหนึ่งโพสต์", "back": "โพสต์ทั้งหมด", "by": "เผยแพร่"},
    "vi": {"home": "Bottled Marbles", "lead": "Bottled Marbles được làm ra thế nào: quyết định, ngõ cụt và cách sửa, mỗi ngày một bài.", "back": "Tất cả bài viết", "by": "Đăng"},
    "tr": {"home": "Bottled Marbles", "lead": "Bottled Marbles nasıl yapılıyor: kararlar, çıkmaz sokaklar ve düzeltmeler, günde bir yazı.", "back": "Tüm yazılar", "by": "Yayınlandı"},
}
_LANDING = {}


def _strings(root):
    """content/landing.json strings (name, lang_label, journal, privacy, terms per language), cached per root."""
    root = str(root)
    if root not in _LANDING:
        _LANDING[root] = json.loads((Path(root) / "content" / "landing.json").read_text(encoding="utf-8"))["strings"]
    return _LANDING[root]


def _e(s):
    return html.escape(s, quote=True)


def jpath(lang, slug=None):
    base = "/journal/" if lang == "en" else "/%s/journal/" % lang
    return base if slug is None else "%s%s/" % (base, slug)


def parse(text, where="?"):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit("build_journal: %s has no front matter" % where)
    meta = {}
    for line in m.group(1).split("\n"):
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    for k in ("title", "date", "time", "summary"):
        if not meta.get(k):
            raise SystemExit("build_journal: %s front matter missing %s" % (where, k))
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", meta["date"]) or not re.match(r"^([01]\d|2[0-3]):[0-5]\d$", meta["time"]):
        raise SystemExit("build_journal: %s bad date/time (%s %s)" % (where, meta["date"], meta["time"]))
    if meta.get("copy_review") and not REVIEW_RE.match(meta["copy_review"]):
        raise SystemExit("build_journal: %s copy_review must look like 'iris YYYY-MM-DD'" % where)
    return meta, m.group(2).strip()


def _inline(s):
    s = _e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)


def body_html(body):
    out, para, items = [], [], []

    def flush():
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            para.clear()
        if items:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline(i) for i in items))
            items.clear()

    for line in body.split("\n"):
        if not line.strip():
            flush()
        elif line.startswith("## "):
            flush()
            out.append("<h2>%s</h2>" % _inline(line[3:].strip()))
        elif line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def load(root):
    """-> list of posts (newest first): {slug, date, time, langs:[...], <lang>:{meta,body}} — only the languages a post has; en is required."""
    root = Path(root)
    posts = []
    base = root / "content" / "journal"
    now = dt.datetime.now(KST)
    for d in sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []:
        if not SLUG_RE.match(d.name):
            raise SystemExit("build_journal: bad slug %r" % d.name)
        extra = sorted(f.name for f in d.iterdir() if f.name not in ["%s.md" % l for l in LANGS])
        if extra:
            raise SystemExit("build_journal: %s has unexpected files %s (only <lang>.md for the 12 languages)" % (d.name, extra))
        post = {"slug": d.name, "langs": []}
        for l in LANGS:
            f = d / ("%s.md" % l)
            if f.is_file():
                meta, body = parse(f.read_text(encoding="utf-8"), "%s/%s.md" % (d.name, l))
                post[l] = {"meta": meta, "body": body}
                post["langs"].append(l)
        if "en" not in post["langs"]:
            raise SystemExit("build_journal: %s/en.md missing (en is required)" % d.name)
        e = post["en"]["meta"]
        for l in post["langs"]:
            if (post[l]["meta"]["date"], post[l]["meta"]["time"]) != (e["date"], e["time"]):
                raise SystemExit("build_journal: %s %s/en date+time differ" % (d.name, l))
        stamp = dt.datetime.strptime("%s %s" % (e["date"], e["time"]), "%Y-%m-%d %H:%M").replace(tzinfo=KST)
        if stamp > now + dt.timedelta(minutes=1):
            raise SystemExit("build_journal: %s is dated in the future (%s %s KST)" % (d.name, e["date"], e["time"]))
        post["date"], post["time"] = e["date"], e["time"]
        posts.append(post)
    posts.sort(key=lambda p: (p["date"], p["time"], p["slug"]), reverse=True)
    return posts


def _head(lang, title, desc, canon, alts, jsonld=None):
    alt = "\n".join('<link rel="alternate" hreflang="%s" href="%s%s">' % (l, SITE, p) for l, p in alts)
    alt += '\n<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, alts[0][1])
    ld = ""
    if jsonld:
        ld = '\n<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")
    return """<!doctype html>
<html lang="{lang}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{alt}{ld}
<link rel="stylesheet" href="/assets/landing.css?v={v}">
<script src="/assets/landing.js?v={v}" defer></script>
</head>
""".format(lang=lang, title=_e(title), desc=_e(desc), canon=canon, alt=alt, ld=ld, v=ASSET_V)


def _top(root, lang, slug=None, have=LANGS):
    """Header: home + journal links and the language select (all 12; a language without this post points to its journal index)."""
    st = _strings(root)
    home = "/" if lang == "en" else "/%s/" % lang
    opts = [(l, jpath(l, slug if l in have else None), st[l]["name"]) for l in LANGS]
    sel = chrome.lang_select(opts, lang, st[lang]["lang_label"])
    return chrome.header([(home, UI[lang]["home"], False), (jpath(lang), st[lang]["journal"], True)], sel) + "\n"


def _foot(root, lang):
    st = _strings(root)[lang]
    return '<footer>%s<p>ipe() 2026</p></footer>\n</body>\n</html>\n' % chrome.legal_links(st["privacy"], st["terms"])


def index_page(lang, posts, root):
    u, st = UI[lang], _strings(root)[lang]
    alts = [(l, jpath(l)) for l in LANGS]
    cards = []
    for p in posts:
        cl = lang if lang in p["langs"] else "en"   # untranslated posts show the English card
        m = p[cl]["meta"]
        cards.append('<li><a href="{href}"{la}><span class="when">{date} {time} KST</span><strong>{title}</strong>'
                     '<span class="sum">{sum}</span></a></li>'.format(
                         href=jpath(cl, p["slug"]), la="" if cl == lang else ' hreflang="en" lang="en"', date=p["date"],
                         time=p["time"], title=_e(m["title"]), sum=_e(m["summary"])))
    title = "%s — %s" % (st["journal"], "Bottled Marbles")
    return (_head(lang, title, u["lead"], SITE + jpath(lang), alts) + "<body>\n" + _top(root, lang)
            + '<main class="journal">\n<h1>%s</h1>\n<p class="lead">%s</p>\n<ul class="posts">\n%s\n</ul>\n</main>\n'
            % (_e(st["journal"]), _e(u["lead"]), "\n".join(cards)) + _foot(root, lang))


def post_page(lang, post, root):
    u = UI[lang]
    m = post[lang]["meta"]
    have = post["langs"]
    alts = [(l, jpath(l, post["slug"])) for l in LANGS if l in have]
    canon = SITE + jpath(lang, post["slug"])
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"], "description": m["summary"],
          "inLanguage": lang, "datePublished": "%sT%s:00+09:00" % (post["date"], post["time"]),
          "mainEntityOfPage": canon, "author": {"@type": "Organization", "name": "ipe Studio"}}
    return (_head(lang, "%s — Bottled Marbles" % m["title"], m["summary"], canon, alts, ld)
            + "<body>\n" + _top(root, lang, post["slug"], have)
            + '<main class="journal">\n<article>\n<h1>%s</h1>\n<p class="when">%s: %s %s KST</p>\n%s\n</article>\n'
              '<p class="back"><a href="%s">&larr; %s</a></p>\n</main>\n' % (
                  _e(m["title"]), _e(u["by"]), post["date"], post["time"], body_html(post[lang]["body"]),
                  jpath(lang), _e(u["back"])) + _foot(root, lang))


def sitemap_rows(root):
    """Sitemap <url> rows for the journal: 12 index pages + each post in the languages it has (hreflang pairs + x-default)."""
    posts = load(root)
    rows = []
    for slug, have in [(None, LANGS)] + [(p["slug"], p["langs"]) for p in posts]:
        links = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l, SITE, jpath(l, slug)) for l in have)
        links += '<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, jpath("en", slug))
        for l in have:
            rows.append("<url><loc>%s%s</loc>%s</url>" % (SITE, jpath(l, slug), links))
    return rows


def render(root):
    posts = load(root)
    out = {}
    for l in LANGS:
        out[jpath(l).strip("/") + "/index.html"] = index_page(l, posts, root)
        for p in posts:
            if l in p["langs"]:
                out[jpath(l, p["slug"]).strip("/") + "/index.html"] = post_page(l, p, root)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the journal pages.")
    ap.add_argument("--root", default=str(HERE.parent))
    ap.add_argument("--check", action="store_true", help="fail if committed pages differ from the build")
    a = ap.parse_args(argv)
    root = Path(a.root)
    pages = render(root)
    if a.check:
        bad = [r for r, t in pages.items() if not (root / r).is_file() or (root / r).read_text(encoding="utf-8") != t]
        # journal pages on disk that no post produces (a removed post) are stale too
        for l in LANGS:
            jd = root / jpath(l).strip("/")
            if jd.is_dir():
                for f in jd.rglob("index.html"):
                    rel = f.relative_to(root).as_posix()
                    if rel not in pages:
                        bad.append(rel)
        if bad:
            print("build_journal --check: out of date: %s" % ", ".join(sorted(bad)[:6]), file=sys.stderr)
            return 1
        print("journal up to date: %d pages" % len(pages))
        return 0
    for rel, text in pages.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print("journal built: %d pages" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
