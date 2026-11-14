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
1. 글 작성: `content/journal/<YYYY-MM-DD>-<slug>.md`(한국어 원문, ko) 를 쓴다. front matter 는 title·description.
2. 번역 12개: 같은 폴더에 `<YYYY-MM-DD>-<slug>.<lang>.md` 를 games.json 의 langs 중 ko 를 뺀 11개 언어(en ja zh-Hant es pt-BR fr de id th vi tr)로 만든다. 글 하나당 파일은 ko 1 + 11 = 12개다. 파일명 언어 코드는 games.json 과 같아야 한다.
3. Iris 검수: 12개 파일 전부를 본다(문장·톤·사실·과장·브랜드 용어). 통과한 파일마다 front matter 에 한 줄을 넣는다: `copy_review: iris YYYY-MM-DD`
4. 발행 큐: `ops/publish_daily.sh` 는 오늘까지 날짜가 된, 아직 발행되지 않은 ko 글마다 12개 파일이 모두 있고 전부 `copy_review` 줄이 있는지 본다. 이미 발행된 글(`journal/<slug>/index.html` 이 main 에 있는 글)은 막지 않는다.
   - 언어 파일이 없으면 「LANG_MISSING content/journal/…」 를 로그한다.
   - 파일은 있는데 줄이 없거나 형식(`iris YYYY-MM-DD`)이 틀리면 「NO_COPY_REVIEW content/journal/…」 를 로그한다.
   - 하나라도 걸리면 아무것도 발행하지 않고 「nothing to publish」 로 끝난다(빌드는 오늘 이전 글을 전부 포함하므로 과거 미검수 글도 같이 나가기 때문). 로그 `COPY_REVIEW_PENDING n` 은 검수 안 된 미래 글 수다.
5. 게이트는 CR(\r)과 값 뒤 공백을 무시하고 비교한다. `scripts/build_site.py` 는 같은 형식을 검증한다.

## TODO
- Real art (assets/ are brand-neutral placeholders).
- Final privacy wording once legal review is done — a clearly marked draft placeholder lives at `/privacy/` · `/ko/privacy/` until then. Terms page later.
- After publish: `python3 scripts/indexnow.py` (key file already in the repo root).
