# bottledmarbles-rest

Static site for Bottled Marbles (bottledmarbles.ipe.rest). Generated HTML is committed; stdlib-only Python builds it.

## Build / check

```
python3 scripts/build_landing.py   # 12 landing pages + sitemap.xml
python3 scripts/build_journal.py   # journal indexes + post pages (12 languages)
python3 scripts/build_redirects.py # 10 redirect stubs for retired languages
python3 scripts/build_legal.py     # /privacy/ /terms/ (en) + /ko/privacy/ /ko/terms/ from content/legal/<doc>/<lang>.md
bash scripts/check.sh              # gate: unit tests, landing match, journal up to date
```

Languages (fixed): en (/), ko, ja, zh-Hant, es, pt-BR, fr, de, id, th, vi, tr.
The header holds the language `<select>` and the Journal link; the footer holds only privacy/terms and the journal link.
`assets/landing.js` picks the language: saved `ipe_lang` (localStorage) wins; otherwise, only on the language-less roots (`/`, `/journal/…`), `navigator.languages` decides and redirects. `/<lang>/…` URLs and bots are never redirected.

**Retired-language stubs** (`scripts/build_redirects.py`, kit v0.7.0 rules): `/pt`→`/pt-BR/` · `/zh`→`/zh-Hant/` · `/ar` `/hi` `/ru`→`/` (home and `/journal/` only). GitHub Pages cannot 301, so each stub is meta refresh + `location.replace` (query/hash kept) + canonical + `noindex,follow` + visible link; never in sitemap/hreflang (tested).

**Privacy / terms**: sources are `content/legal/{privacy,terms}/{en,ko}.md` (Korean is the operator's jurisdiction; operator and contact copied from Claimball). The footer of `ko` links `/ko/privacy/`·`/ko/terms/`; the other 10 languages link the English pages until they are translated and reviewed (`chrome.LEGAL_LANGS`). Facts stated: no accounts, no ads, no analytics, no cookies, age 16+; update the text first if any of that changes (e.g. AdMob).

## Journal procedure (standing rules)

1. **Write** the post (English original).
2. **Translate** into all 12 languages.
3. **Iris copy review** of every language file.
4. **Record** `copy_review: iris [YYYY-MM-DD]` in each of the 10 translation files' frontmatter (the en/ko originals are ours and need none).
5. **Publish queue**: put the folder in `~/.ipe/queue/bottledmarbles/NN-slug/`.

File naming: one folder per post, `NN-slug/{lang}.md` × 12 — `en.md ko.md ja.md zh-Hant.md es.md pt-BR.md fr.md de.md id.md th.md vi.md tr.md`.

Frontmatter of every file:

```
---
title: ...
date: YYYY-MM-DD      # stamped by publish_next (KST)
time: HH:MM
summary: ...
copy_review: iris YYYY-MM-DD
---
```

`scripts/publish_next.py` (run by `ops/gate_publish.py`) publishes the head of the queue only when all 12 files exist and the 10 translations have `copy_review` (en/ko originals exempt). Otherwise it prints a `WARNING`, exits with code 4, and does **not** skip ahead to the next queue post (0 published, 3 queue empty, 4 not ready, 1 failure).
