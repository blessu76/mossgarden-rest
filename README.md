# mossgarden-rest

Intro site for **Moss Garden / 이끼정원**. Static site (GitHub Pages), Python 3.8+ stdlib only. Content is empty — skeleton only (index.html is a "coming soon" page).

- Game name / domain / operator live in ONE place: `games.json` (domain is undecided; no `CNAME` until the owner approves).
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Deploy: `.github/workflows/deploy.yml` (green gate, then GitHub Pages). Needs secret `IPE_WEB_KIT_DEPLOY_KEY`.

## TODO
- Pages (home content, privacy/terms/contact), i18n, build script, sitemap, assets/art.
