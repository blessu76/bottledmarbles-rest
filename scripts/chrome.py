"""Shared page chrome for the landing and the journal: the language <select> (+ no-JS link list) and the legal footer links.

Privacy / terms links live ONLY in the footer (never in the header nav). Language options keep the fixed order of games.json "langs".
"""
import html
import json
from pathlib import Path

PRIVACY_HREF = "/privacy/"
TERMS_HREF = "/terms/"
LEGAL_LANGS = ("en", "ko")   # languages that have their own /<lang>/privacy/ and /<lang>/terms/ (the rest link the English pages)


def _e(s):
    return html.escape(s, quote=True)


def lang_select(options, cur, label):
    """options = [(code, href, native name)] in display order -> <label>+<select> (JS navigates on change) + <noscript> links."""
    opts = "".join('<option value="%s" lang="%s"%s>%s</option>' % (_e(h), c, " selected" if c == cur else "", _e(n))
                   for c, h, n in options)
    nojs = "".join('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (_e(h), c, c, _e(n)) for c, h, n in options)
    return ('<div class="langs"><label for="langsel">%s</label>'
            '<select id="langsel" class="langsel" data-langsel>%s</select>'
            '<noscript><span class="langs-nojs">%s</span></noscript></div>') % (_e(label), opts, nojs)


def legal_path(doc, lang="en"):
    return "/%s/" % doc if lang not in LEGAL_LANGS or lang == "en" else "/%s/%s/" % (lang, doc)


def legal_links(privacy, terms, lang="en"):
    return '<p class="legal"><a href="%s">%s</a> · <a href="%s">%s</a></p>' % (
        legal_path("privacy", lang), _e(privacy), legal_path("terms", lang), _e(terms))


def legal_labels(root, lang):
    s = json.loads((Path(root) / "content" / "landing.json").read_text(encoding="utf-8"))["strings"][lang]
    return s["privacy"], s["terms"]


def header(nav, select_html):
    """Page header: nav = [(href, label, is_current)] then the language select. Privacy/terms never go here."""
    links = "".join('<a href="%s"%s>%s</a>' % (_e(h), ' aria-current="true"' if cur else "", _e(t)) for h, t, cur in nav)
    return '<header class="top"><nav class="topnav" aria-label="Site">%s</nav>%s</header>' % (links, select_html)
