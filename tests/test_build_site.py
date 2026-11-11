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
                         'class="rel"'):
                self.assertIn(want, html, key)
        en, ko = files["release-notes/index.html"], files["ko/release-notes/index.html"]
        # both builds, both notes languages
        for s in ("1.0.0 · Build 2", "1.0.0 · Build 1", "2026-11-11", "The dew total", "First TestFlight build"):
            self.assertIn(s, en)
        for s in ("1.0.0 · 빌드 2", "1.0.0 · 빌드 1", "2026-11-11", "이슬 합계", "첫 TestFlight 빌드"):
            self.assertIn(s, ko)
        # newest first: build 2 section before build 1
        self.assertLess(en.index("The dew total"), en.index("First TestFlight build"))
        self.assertLess(ko.index("이슬 합계"), ko.index("첫 TestFlight 빌드"))

    def test_release_notes_order_newest_first(self):
        e = lambda b, d: {"build": str(b), "date": d}
        ordered = bs.sort_releases([e(1, "2026-11-11"), e(10, "2026-11-10"), e(2, "2026-11-11")])
        self.assertEqual([x["build"] for x in ordered], ["10", "2", "1"])
        self.assertEqual([x["build"] for x in bs.sort_releases([e(2, "2026-11-12"), e(2, "2026-11-10")])], ["2", "2"])

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

    def test_no_store_or_price_claims_in_copy(self):
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        blob = "\n".join(files.values()).lower()
        for bad in ("android", "admob", "download", "app store", "google play", "free to play", "in-app purchase", "iap"):
            self.assertNotIn(bad, blob, bad)


if __name__ == "__main__":
    unittest.main()
