#!/usr/bin/env python3
"""Builds the journal: /journal/ (en) + /ko/journal/, one page per post, and the sitemap rows — stdlib only (Python 3.9+).

  python3 scripts/build_journal.py            # write into this repo
  python3 scripts/build_journal.py --check    # fail if the committed pages differ from the build
  python3 scripts/build_journal.py --root DIR

Source: content/journal/<slug>/{en,ko}.md  =  "---\\ntitle: ..\\ndate: YYYY-MM-DD\\ntime: HH:MM\\nsummary: ..\\n---\\n" + body.
Body subset: paragraphs, "## " headings, "- " lists, **bold**, `code`. Both languages must exist (a post is published in en AND ko).
date/time = the real publish moment in KST (stamped by scripts/publish_next.py, never back-dated; the build refuses a future date).
"""
import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

import chrome

HERE = Path(__file__).resolve().parent
SITE = "https://bottledmarbles.ipe.rest"
ASSET_V = "20261114a"
LANGS = ("en", "ko")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KST = dt.timezone(dt.timedelta(hours=9))
UI = {
    "en": {"journal": "Journal", "home": "Bottled Marbles", "lead": "How Bottled Marbles gets made: decisions, dead ends and fixes, one post a day.",
           "back": "All posts", "read": "Read", "other": "한국어", "by": "Posted", "lang_label": "Language"},
    "ko": {"journal": "저널", "home": "구슬병", "lead": "구슬병(Bottled Marbles)을 만드는 과정 — 결정, 막힌 곳, 고친 방법을 하루 한 편씩.",
           "back": "전체 글", "read": "읽기", "other": "English", "by": "발행", "lang_label": "언어"},
}


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
    """-> list of posts (newest first): {slug, date, time, en:{meta,body}, ko:{meta,body}}."""
    root = Path(root)
    posts = []
    base = root / "content" / "journal"
    now = dt.datetime.now(KST)
    for d in sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []:
        if not SLUG_RE.match(d.name):
            raise SystemExit("build_journal: bad slug %r" % d.name)
        post = {"slug": d.name}
        for l in LANGS:
            f = d / ("%s.md" % l)
            if not f.is_file():
                raise SystemExit("build_journal: %s/%s.md missing (a post needs en and ko)" % (d.name, l))
            meta, body = parse(f.read_text(encoding="utf-8"), "%s/%s.md" % (d.name, l))
            post[l] = {"meta": meta, "body": body}
        e, k = post["en"]["meta"], post["ko"]["meta"]
        if (e["date"], e["time"]) != (k["date"], k["time"]):
            raise SystemExit("build_journal: %s en/ko date+time differ" % d.name)
        stamp = dt.datetime.strptime("%s %s" % (e["date"], e["time"]), "%Y-%m-%d %H:%M").replace(tzinfo=KST)
        if stamp > now + dt.timedelta(minutes=1):
            raise SystemExit("build_journal: %s is dated in the future (%s %s KST)" % (d.name, e["date"], e["time"]))
        post["date"], post["time"] = e["date"], e["time"]
        posts.append(post)
    posts.sort(key=lambda p: (p["date"], p["time"], p["slug"]), reverse=True)
    return posts


def _head(lang, title, desc, canon, alts):
    alt = "\n".join('<link rel="alternate" hreflang="%s" href="%s%s">' % (l, SITE, p) for l, p in alts)
    alt += '\n<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, alts[0][1])
    return """<!doctype html>
<html lang="{lang}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{alt}
<link rel="stylesheet" href="/assets/landing.css?v={v}">
<script src="/assets/landing.js?v={v}" defer></script>
</head>
""".format(lang=lang, title=_e(title), desc=_e(desc), canon=canon, alt=alt, v=ASSET_V)


NAMES = {"en": "English", "ko": "한국어"}


def _top(lang, slug=None):
    """Header: home + journal links and the language select (journal exists in en and ko only). No legal links here."""
    u = UI[lang]
    home = "/" if lang == "en" else "/%s/" % lang
    sel = chrome.lang_select([(l, jpath(l, slug), NAMES[l]) for l in LANGS], lang, u["lang_label"])
    return ('<header class="top"><nav class="topnav" aria-label="Journal"><a href="%s">%s</a>'
            '<a href="%s" aria-current="true">%s</a></nav>%s</header>\n') % (
        home, _e(u["home"]), jpath(lang), _e(u["journal"]), sel)


def _foot(root, lang):
    return '<footer>%s<p>ipe() 2026</p></footer>\n</body>\n</html>\n' % chrome.legal_links(*chrome.legal_labels(root, lang))


def index_page(lang, posts, root):
    u = UI[lang]
    alts = [(l, jpath(l)) for l in LANGS]
    cards = "\n".join(
        '<li><a href="{href}"><span class="when">{date} {time} KST</span><strong>{title}</strong>'
        '<span class="sum">{sum}</span></a></li>'.format(
            href=jpath(lang, p["slug"]), date=p["date"], time=p["time"], title=_e(p[lang]["meta"]["title"]),
            sum=_e(p[lang]["meta"]["summary"])) for p in posts)
    title = "%s — %s" % (u["journal"], "Bottled Marbles")
    return (_head(lang, title, u["lead"], SITE + jpath(lang), alts) + "<body>\n" + _top(lang)
            + '<main class="journal">\n<h1>%s</h1>\n<p class="lead">%s</p>\n<ul class="posts">\n%s\n</ul>\n</main>\n'
            % (_e(u["journal"]), _e(u["lead"]), cards) + _foot(root, lang))


def post_page(lang, post, root):
    u = UI[lang]
    m = post[lang]["meta"]
    alts = [(l, jpath(l, post["slug"])) for l in LANGS]
    return (_head(lang, "%s — Bottled Marbles" % m["title"], m["summary"], SITE + jpath(lang, post["slug"]), alts)
            + "<body>\n" + _top(lang, post["slug"])
            + '<main class="journal">\n<article>\n<h1>%s</h1>\n<p class="when">%s: %s %s KST</p>\n%s\n</article>\n'
              '<p class="back"><a href="%s">&larr; %s</a></p>\n</main>\n' % (
                  _e(m["title"]), _e(u["by"]), post["date"], post["time"], body_html(post[lang]["body"]),
                  jpath(lang), _e(u["back"])) + _foot(root, lang))


def sitemap_rows(root):
    """Sitemap <url> rows for the journal (index + posts, en and ko, with hreflang pairs)."""
    posts = load(root)
    rows = []
    pairs = [(None,)] + [(p["slug"],) for p in posts]
    for (slug,) in pairs:
        links = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l, SITE, jpath(l, slug)) for l in LANGS)
        links += '<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, jpath("en", slug))
        for l in LANGS:
            rows.append("<url><loc>%s%s</loc>%s</url>" % (SITE, jpath(l, slug), links))
    return rows


def render(root):
    posts = load(root)
    out = {}
    for l in LANGS:
        out[jpath(l).strip("/") + "/index.html"] = index_page(l, posts, root)
        for p in posts:
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
