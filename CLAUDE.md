# mossgarden-rest
See README.md. Run `bash scripts/check.sh` (must print GREEN) before every commit. Never push / touch DNS until the owner approves. Docs go in `_ipe/foundry/F-027_mossgarden/`, not here.
Release notes are managed only inside the app (decision 0143): no web release-notes page, menu, link, or sitemap entry.
Journal standing rule: every journal post is translated into all 12 languages (ko original + 11 `.<lang>.md`), Iris reviews all 12 (`copy_review: iris YYYY-MM-DD` in each), then it goes to the publish queue. The publish gate skips a post with a missing or unreviewed language file (LANG_MISSING / NO_COPY_REVIEW). Do not change ops/journal_gate.* to get around it.
