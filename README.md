# bottledmarbles-rest

Static site for Bottled Marbles (bottledmarbles.ipe.rest). Generated HTML is committed; stdlib-only Python builds it.

## Build / check

```
python3 scripts/build_landing.py   # 12 landing pages + sitemap.xml
python3 scripts/build_journal.py   # journal indexes + post pages (12 languages)
bash scripts/check.sh              # gate: unit tests, landing match, journal up to date
```

Languages (fixed): en (/), ko, ja, zh-Hant, es, pt-BR, fr, de, id, th, vi, tr.
The header holds the language `<select>` and the Journal link; the footer holds only privacy/terms and the journal link.
`assets/landing.js` picks the language: saved `ipe_lang` (localStorage) wins; otherwise, only on the language-less roots (`/`, `/journal/…`), `navigator.languages` decides and redirects. `/<lang>/…` URLs and bots are never redirected.

## Journal procedure (standing rules)

1. **Write** the post (English original).
2. **Translate** into all 12 languages.
3. **Iris copy review** of every language file.
4. **Record** `copy_review: iris YYYY-MM-DD` in each file's frontmatter.
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

`scripts/publish_next.py` (run by `ops/gate_publish.py`) publishes the head of the queue only when all 12 files exist and each has `copy_review`. Otherwise it prints a `WARNING`, exits with code 4, and does **not** skip ahead to the next queue post (0 published, 3 queue empty, 4 not ready, 1 failure).
