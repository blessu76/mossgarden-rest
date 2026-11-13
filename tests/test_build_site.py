import json
import re
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
        self.assertFalse(any("release-notes" in k for k in files))

    def test_sitemap_is_consistent(self):
        errs, urls = cs.check(REPO)
        self.assertEqual(errs, [])
        self.assertTrue(urls)

    def test_footer_privacy_link(self):
        # the privacy page exists (draft placeholder) — the footer slot became a real link
        files = bs.build_all(bs.make_ctx(REPO, require_all=True)[0])
        for key, href in (("index.html", 'href="/privacy/"'), ("ko/index.html", 'href="/ko/privacy/"'),
                          ("contact/index.html", 'href="/privacy/"'), ("ko/contact/index.html", 'href="/ko/privacy/"'),
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
        for key in ("ko/index.html", "ko/contact/index.html", "ko/privacy/index.html"):
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
        for bad in ("android", "admob", "download", "app store", "google play", "free to play", "in-app purchase"):
            self.assertNotIn(bad, blob, bad)
        self.assertIsNone(re.search(r"\biap\b", blob))  # word match — Indonesian "setiap" is fine


if __name__ == "__main__":
    unittest.main()


class TwelveLanguageTests(unittest.TestCase):
    ORDER = ["en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"]

    def files(self):
        return bs.build_all(bs.make_ctx(REPO, require_all=True)[0])

    def test_twelve_langs_in_kit_order_no_ended(self):
        self.assertEqual(list(bs.LANGS), self.ORDER)
        self.assertEqual(list(bs.MAIN_LANGS), self.ORDER)
        for dead in ("zh-Hans", "ru", "ar", "hi", "zh"):
            self.assertNotIn(dead, bs.LANGS)
        self.assertTrue(set(bs.LANGS) <= set(bs._OG_LOCALE))

    def test_every_lang_has_all_pages_and_hreflang_12(self):
        files = self.files()
        for l in self.ORDER:
            for slug in ("", "contact/", "privacy/"):
                key = (l + "/" if l != "en" else "") + slug + "index.html"
                self.assertIn(key, files, key)
            html = files[(l + "/" if l != "en" else "") + "index.html"]
            self.assertIn('<html lang="%s"' % l, html)
            self.assertEqual(html.count('rel="alternate" hreflang='), 13, l)  # 12 + x-default
        self.assertIn('hreflang="zh-Hant" href="%s/zh-Hant/"' % bs.SITE, files["index.html"])

    def test_sitemap_and_llms_list_12(self):
        files = self.files()
        for l in self.ORDER:
            self.assertIn("<loc>%s</loc>" % bs.url(bs.path_home(l)), files["sitemap.xml"])
        self.assertIn("12 languages", files["llms.txt"])

    def test_zh_hant_is_traditional(self):
        import json
        txt = (REPO / "content" / "i18n" / "zh-Hant.json").read_text(encoding="utf-8")
        for simp in "园这个们时会发长设选记问还对爱让给觉开关为".split():
            for ch in simp:
                self.assertNotIn(ch, txt, ch)
        json.loads(txt)

    def test_legal_pages_outside_en_ko_point_to_en_original(self):
        files = self.files()
        for l in self.ORDER[2:]:
            html = files[l + "/privacy/index.html"]
            self.assertIn('href="/privacy/"', html, l)
            self.assertIn('href="/ko/privacy/"', html, l)


class JournalTests(unittest.TestCase):
    def build(self, today):
        return bs.build_all(bs.make_ctx(REPO, require_all=True, today=today)[0])

    def test_future_posts_are_not_built(self):
        files = self.build("2026-11-13")
        self.assertIn("journal/dew-decimals/index.html", files)
        self.assertNotIn("journal/garden-redesign/index.html", files)
        self.assertIn("journal/garden-redesign/index.html", self.build("2026-11-14"))

    def test_ko_original_and_en_fallback(self):
        files = self.build("2026-11-13")
        self.assertIn('<html lang="ko"', files["ko/journal/dew-decimals/index.html"])
        self.assertIn('<div lang="ko">', files["ko/journal/dew-decimals/index.html"])
        self.assertIn('<div lang="en">', files["ja/journal/dew-decimals/index.html"])
        self.assertIn('class="note"', files["ja/journal/dew-decimals/index.html"])

    def test_nav_footer_sitemap_hreflang(self):
        files = self.build("2026-11-13")
        for l in bs.LANGS:
            home = files[(l + "/" if l != "en" else "") + "index.html"]
            self.assertIn('href="%s"' % bs.path_journal(l), home, l)
            self.assertIn("<loc>%s</loc>" % bs.url(bs.path_journal(l)), files["sitemap.xml"])
            self.assertIn("<loc>%s</loc>" % bs.url(bs.path_post(l, "dew-decimals")), files["sitemap.xml"])
            page = files[bs.path_post(l, "dew-decimals").strip("/") + "/index.html"]
            self.assertEqual(page.count('rel="alternate" hreflang='), 13, l)
        self.assertNotIn("release-notes", files["sitemap.xml"])
