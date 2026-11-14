# Changelog

## Unreleased
- Web release notes removed (decision 0143): release-notes pages, nav/footer links, sitemap/llms entries. `/release-notes/` and `/releases/` (12 languages) now redirect to the home page and are not in the sitemap. Release notes are managed in the app.
- Footer: reserved link slot for the future privacy policy page (text placeholder, i18n; no URL until the page exists).
- Full intro site (English + Korean): build_site.py + i18n/page sources, moss-themed assets (brand-neutral placeholders), CNAME (mossgarden.ipe.rest), IndexNow key file, sitemap/robots/llms, check.sh green gate (kit, sources, tests, up-to-date build, sitemap).
- Initial skeleton (copied from tilttower-rest layout): games.json, placeholder index/404, kit lock, check.sh, Pages deploy workflow.
