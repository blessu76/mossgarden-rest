# mossgarden-rest

Intro site for **Moss Garden / 이끼정원** (F-027). Static site, GitHub Pages, Python 3.8+ stdlib only, 12 languages (en ko ja zh-Hant es pt-BR fr de id th vi tr; en + ko by hand, the rest machine-translated drafts).

- Game name / domain / operator live in ONE place: `games.json` (+ root `CNAME` must equal its `domain`).
- Build: `python3 scripts/build_site.py` — writes the generated pages, sitemap.xml, robots.txt, llms.txt.
- Green gate before every commit: `bash scripts/check.sh` (kit lock, sources, tests, build up to date, sitemap).
- Private `ipe_web_kit` is pinned by `vendor/ipe_web_kit.lock`; install with `python3 scripts/kit_lock.py sync --kit ~/Developer/ipe_web_kit`.
- Release notes live only in the app (Settings); the site has no release-notes page. `content/releases.json` + `scripts/check_release.py` are the TestFlight data gate the app's deploy script calls (`--build N [--latest]`).
- Page text: `content/i18n/<lang>.json` and `content/pages/<lang>/{contact,privacy}.md`.
- Copy is intentionally pre-launch: no store links, release dates, prices, ad or download promises. iOS first — other platforms not mentioned yet.

## 저널 발행 절차
1. 글 작성: `content/journal/<YYYY-MM-DD>-<slug>.md`(한국어) + `.en.md`(영어), front matter 는 title·description.
2. Iris 검수: 문장·톤·사실·과장·브랜드 용어를 KO·EN 전부 본다.
3. 검수 통과한 두 파일 모두의 front matter 에 한 줄 추가: `copy_review: iris YYYY-MM-DD`
4. 발행 큐: 날짜가 된 글만 `ops/publish_daily.sh` 가 발행한다. 줄이 없거나 형식이 틀리면(KO·EN 중 하나라도) 「NO_COPY_REVIEW」를 로그하고 건너뛴다. 로그 `COPY_REVIEW_PENDING n` 은 검수 안 된 미래 글 수다.
5. 과거 글은 줄이 없어도 빌드되지만, 줄이 있으면 형식(`iris YYYY-MM-DD`)을 `scripts/build_site.py` 가 검증한다.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Final privacy wording once legal review is done — a clearly marked draft placeholder lives at `/privacy/` · `/ko/privacy/` until then. Terms page later.
- After publish: `python3 scripts/indexnow.py` (key file already in the repo root).
