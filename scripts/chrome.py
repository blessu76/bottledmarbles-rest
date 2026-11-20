"""Shared page chrome for the landing and the journal: the language <select> (+ no-JS link list) and the legal footer links.

Privacy / terms links live ONLY in the footer (never in the header nav). Language options keep the fixed order of games.json "langs".
Privacy / terms are owned by ipe.rest (https://ipe.rest/legal/…, Korean under /ko/legal/…); this site only keeps redirect stubs at /privacy/ /terms/ /ko/privacy/ /ko/terms/.
"""
import html
import json
from pathlib import Path

LEGAL_BASE = "https://ipe.rest"   # the policy source of truth (ipe.rest/legal/ is shared by the ipe apps and sites)
GA_ID = "G-XG4BH800J0"       # company-wide GA4 measurement ID (ipe) — the same ID for every ipe *-rest site; never create a new one here
SITE = "https://bottledmarbles.ipe.rest"


def _e(s):
    return html.escape(s, quote=True)


# Local hosts: localhost, loopback 127.x, IPv6 loopback, the unspecified 0.0.0.0, and private LAN IPs
# (10.x, 192.168.x, 172.16–31.x). The guard runs before the gtag loader is appended, so nothing is sent from a local preview.
LOCAL_HOST_JS = (r"if(!h||h==='localhost'||h==='0.0.0.0'||h==='[::1]'"
                 r"||/^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[01])\./.test(h))return;")


def ga_head():
    """GA4 gtag loader for <head> on every public page. Not loaded on local hosts (see LOCAL_HOST_JS)."""
    return ("<script>(function(){var h=location.hostname;"
            + LOCAL_HOST_JS +
            "var s=document.createElement('script');s.async=true;"
            "s.src='https://www.googletagmanager.com/gtag/js?id=%s';document.head.appendChild(s);"
            "window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};"
            "window.gtag('js',new Date());window.gtag('config','%s');})();</script>") % (GA_ID, GA_ID)


def og_tags(title, desc, url):
    """Open Graph basics for pages that do not write their own (journal, legal). Values are escaped."""
    return ('<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Bottled Marbles">\n'
            '<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">') % (_e(title), _e(desc), _e(url))


def lang_select(options, cur, label):
    """options = [(code, href, native name)] in display order -> <label>+<select> (JS navigates on change) + <noscript> links."""
    opts = "".join('<option value="%s" lang="%s"%s>%s</option>' % (_e(h), c, " selected" if c == cur else "", _e(n))
                   for c, h, n in options)
    nojs = "".join('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (_e(h), c, c, _e(n)) for c, h, n in options)
    return ('<div class="langs"><label for="langsel">%s</label>'
            '<select id="langsel" class="langsel" data-langsel>%s</select>'
            '<noscript><span class="langs-nojs">%s</span></noscript></div>') % (_e(label), opts, nojs)


def legal_path(doc, lang="en"):
    """ipe.rest address of the policy: Korean pages -> /ko/legal/<doc>/, every other language -> /legal/<doc>/ (English)."""
    return "%s%s/legal/%s/" % (LEGAL_BASE, "/ko" if lang == "ko" else "", doc)


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
