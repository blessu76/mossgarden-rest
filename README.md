# mossgarden-rest

Intro site for **Moss Garden / 이끼정원** (F-027). Static site, GitHub Pages, Python 3.8+ stdlib only, 12 languages (en ko ja zh-Hant es pt-BR fr de id th vi tr; en + ko by hand, the rest machine-translated drafts).

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Release notes live only in the app (Settings); the site has no release-notes page. `content/releases.json` + `scripts/check_release.py` are the TestFlight data gate the app's deploy script calls (`--build N [--latest]`).
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{contact,privacy}.md`.
- Copy is intentionally pre-launch: no store links, release dates, prices, ad or download promises. iOS first — other platforms not mentioned yet.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Final privacy wording once legal review is done — a clearly marked draft placeholder lives at `/privacy/` · `/ko/privacy/` until then. Terms page later.
- After publish: `python3 scripts/indexnow.py` (key file already in the repo root).
