# mossgarden-rest

Intro site for **Moss Garden / 이끼정원** (F-027). Static site, GitHub Pages, Python 3.8+ stdlib only, English + Korean.

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{contact}.md`.
- Copy is intentionally pre-launch: no store links, release dates, prices, ad or download promises. iOS first — Android not mentioned.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Privacy/terms pages once the app exists and the legal review is done (then add the slugs to `PAGE_SLUGS`).
- After publish: `python3 scripts/indexnow.py` (key file already in the repo root).
