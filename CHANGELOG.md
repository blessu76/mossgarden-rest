# Changelog

## Unreleased
- Web release notes removed: `/release-notes/` pages (12 languages), nav/footer links, sitemap/llms entries, `content/releases.json`, `scripts/check_release.py` and its tests. Release notes are managed in the app.
- Release notes page (`/release-notes/`, `/ko/release-notes/`): generated from `content/releases.json`, newest build first (version · build · date · notes), nav + footer links, sitemap/hreflang/llms entries, `.rel` styles (asset_version 20261111c).
- Release data: `content/releases.json` (TestFlight notes for builds 1–2, en/ko) + `scripts/check_release.py` gate (`--build N [--latest]` / `--all`) wired into check.sh — the app repo's `deploy_ios.sh` calls it before every upload, so a build can no longer go out without its note.
- Footer: reserved link slot for the future privacy policy page (text placeholder, i18n; no URL until the page exists).
- Full intro site (English + Korean): build_site.py + i18n/page sources, moss-themed assets (brand-neutral placeholders), CNAME (mossgarden.ipe.rest), IndexNow key file, sitemap/robots/llms, check.sh green gate (kit, sources, tests, up-to-date build, sitemap).
- Initial skeleton (copied from tilttower-rest layout): games.json, placeholder index/404, kit lock, check.sh, Pages deploy workflow.
