import json
import unittest

from helpers import REPO
import build_site as bs
import check_sitemap as cs


class SiteTests(unittest.TestCase):
    def test_games_json_drives_names(self):
        g = json.loads((REPO / "games.json").read_text(encoding="utf-8"))
        self.assertEqual(bs.DOMAIN, g["domain"])
        self.assertEqual((REPO / "CNAME").read_text().strip(), g["domain"])

    def test_game_langs_come_from_kit_languages(self):
        from ipe_web_kit import languages as kl
        g = json.loads((REPO / "games.json").read_text(encoding="utf-8"))
        for l in g["langs"] + g["main_langs"]:
            self.assertIn(l, kl.SUPPORTED)
        for l, (name, _, _) in bs.LANGS.items():
            self.assertEqual(name, kl.NAMES[l])
        self.assertEqual(bs.kl.hreflang("pt-BR"), "pt-BR")

    def test_unsupported_game_lang_fails_build(self):
        with self.assertRaises(SystemExit):
            bs.check_game_langs({"langs": ["en", "ru"], "main_langs": ["en"]})

    def test_all_languages_complete(self):
        ctx = bs.make_ctx(REPO, require_all=True)[0]
        self.assertEqual(set(ctx.langs), set(bs.LANGS))

    def test_build_has_required_files(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for want in ("index.html", "404.html", "sitemap.xml", "robots.txt", "llms.txt"):
            self.assertIn(want, files)
        for slug in bs.PAGE_SLUGS:
            self.assertTrue(any(k.endswith("%s/index.html" % slug) for k in files), slug)
        for l in bs.LANGS:
            self.assertIn(bs.path_release(l).lstrip("/") + "index.html", files, l)

    def test_release_notes_page(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for key, canon in (("release-notes/index.html", bs.url(bs.path_release("en"))),
                           ("ko/release-notes/index.html", bs.url(bs.path_release("ko")))):
            html = files[key]
            for want in ('<link rel="canonical" href="%s">' % canon,
                         '<link rel="alternate" hreflang="en" href="%s/release-notes/">' % bs.SITE,
                         '<link rel="alternate" hreflang="ko" href="%s/ko/release-notes/">' % bs.SITE,
                         '<link rel="alternate" hreflang="x-default" href="%s/release-notes/">' % bs.SITE,
                         'href="/assets/site.css?v=%s"' % bs.ASSET_V, 'src="/assets/site.js?v=%s"' % bs.ASSET_V,
                         'class="ipe-rel" id="1.0.0-3"'):
                self.assertIn(want, html, key)
        en, ko = files["release-notes/index.html"], files["ko/release-notes/index.html"]
        # both builds, both notes languages
        for s in ("1.0.0 (3)", "1.0.0 (2)", "1.0.0 (1)", "2026-11-11", "The dew total", "First TestFlight build"):
            self.assertIn(s, en)
        for s in ("1.0.0 (3)", "1.0.0 (2)", "1.0.0 (1)", "2026-11-11", "이슬 합계", "첫 TestFlight 빌드"):
            self.assertIn(s, ko)
        # newest first: build 2 section before build 1
        self.assertLess(en.index("The dew total"), en.index("First TestFlight build"))
        self.assertLess(ko.index("이슬 합계"), ko.index("첫 TestFlight 빌드"))

    def test_release_notes_order_newest_first(self):
        import sys
        sys.path.insert(0, str(REPO / "vendor"))
        from ipe_web_kit import releases as kr
        site = kr.load_site(REPO / "content" / "releases.json")
        builds = [r.build_int for r in kr.visible(site)]
        self.assertEqual(builds, sorted(builds, reverse=True))
        self.assertEqual(builds[:3], [3, 2, 1])

    def test_release_notes_links_and_site_files(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for key, href in (("index.html", 'href="/release-notes/"'), ("ko/index.html", 'href="/ko/release-notes/"'),
                          ("contact/index.html", 'href="/release-notes/"'), ("ko/contact/index.html", 'href="/ko/release-notes/"'),
                          ("release-notes/index.html", 'href="/release-notes/"'), ("ko/release-notes/index.html", 'href="/ko/release-notes/"'),
                          ("404.html", 'href="/release-notes/"')):
            self.assertIn(href, files[key], key)  # nav + footer
        for u in (bs.url(bs.path_release("en")), bs.url(bs.path_release("ko"))):
            self.assertIn("<loc>%s</loc>" % u, files["sitemap.xml"])
        self.assertIn("[Release notes](%s/release-notes/)" % bs.SITE, files["llms.txt"])
        errs, urls = cs.check(REPO)  # committed sitemap + on-disk pages stay consistent
        self.assertEqual(errs, [])
        for u in (bs.url(bs.path_release("en")), bs.url(bs.path_release("ko"))):
            self.assertIn(u, urls)

    def test_sitemap_is_consistent(self):
        errs, urls = cs.check(REPO)
        self.assertEqual(errs, [])
        self.assertTrue(urls)

    def test_footer_privacy_link(self):
        # the privacy page exists (draft placeholder) — the footer slot became a real link
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for key, href in (("index.html", 'href="/privacy/"'), ("ko/index.html", 'href="/ko/privacy/"'),
                          ("contact/index.html", 'href="/privacy/"'), ("ko/contact/index.html", 'href="/ko/privacy/"'),
                          ("release-notes/index.html", 'href="/privacy/"'), ("ko/release-notes/index.html", 'href="/ko/privacy/"'),
                          ("404.html", 'href="/privacy/"')):
            self.assertIn(href, files[key], key)
            self.assertNotIn('class="foot-slot"', files[key], key)

    def test_privacy_page_is_a_marked_draft(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for key, lang, notice in (("privacy/index.html", "en", "not a final policy"),
                                  ("ko/privacy/index.html", "ko", "확정되지 않은")):
            html = files[key]
            self.assertIn(notice, html, key)
            self.assertIn('<link rel="canonical" href="%s">' % bs.url(bs.path_page(lang, "privacy")), html, key)
            self.assertIn('<link rel="alternate" hreflang="en" href="%s/privacy/">' % bs.SITE, html, key)
            self.assertIn('<link rel="alternate" hreflang="ko" href="%s/ko/privacy/">' % bs.SITE, html, key)
        for l in bs.LANGS:
            self.assertIn("<loc>%s</loc>" % bs.url(bs.path_page(l, "privacy")), files["sitemap.xml"])
        self.assertIn("[Privacy Policy](%s/privacy/)" % bs.SITE, files["llms.txt"])
        self.assertIn('<a href="/privacy/">Privacy Policy</a>', files["index.html"])
        self.assertIn('<a href="/ko/privacy/">개인정보 처리방침</a>', files["ko/index.html"])

    def test_ko_pages_use_korean_brand(self):
        # ko pages carry the Korean name in the brand header, its aria-label and the page titles (consistent with the ko home title)
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        brand = bs.brand_name("ko")
        self.assertIn("이끼정원", brand)
        for key in ("ko/index.html", "ko/contact/index.html", "ko/privacy/index.html", "ko/release-notes/index.html"):
            self.assertIn('<a class="brand" href="/ko/" aria-label="%s">' % brand, files[key], key)
            self.assertIn("<span>%s</span>" % brand, files[key], key)
        self.assertIn("<title>문의 — %s</title>" % brand, files["ko/contact/index.html"])
        self.assertIn("<title>개인정보 처리방침 — %s</title>" % brand, files["ko/privacy/index.html"])
        # en pages keep the English name
        self.assertIn('<a class="brand" href="/" aria-label="%s">' % bs.NAME, files["index.html"])
        self.assertIn("<title>Contact — %s</title>" % bs.NAME, files["contact/index.html"])

    def test_no_store_or_price_claims_in_copy(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        blob = "\n".join(files.values()).lower()
        for bad in ("android", "admob", "download", "app store", "google play", "free to play", "in-app purchase", "iap"):
            self.assertNotIn(bad, blob, bad)


if __name__ == "__main__":
    unittest.main()
