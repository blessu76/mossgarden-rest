import json
import shutil
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")

RUNNER = r"""
const fs = require('fs'), vm = require('vm');
const input = JSON.parse(process.argv[1]);
const calls = [];
const sandbox = {
  document: {
    documentElement: { lang: input.lang, getAttribute() { return null; } },
    currentScript: { getAttribute(n) { return input.redirect === false ? null : ''; } },
    getElementById() {
      const options = input.alts.map(([hl, href]) => ({ lang: hl, value: href }));
      const idx = Math.max(0, options.findIndex(o => o.lang === input.lang));
      return { options, selectedIndex: idx };
    },
    querySelectorAll() { return []; },
    querySelector() { return null; },
    addEventListener() {},
  },
  navigator: { userAgent: input.ua, languages: input.languages, language: input.languages[0] },
  localStorage: {
    getItem(k) { return input.stored === undefined ? null : input.stored; },
    setItem() {},
  },
  location: { replace(h) { calls.push(h); }, href: '' },
  console,
};
sandbox.window = sandbox;
vm.runInNewContext(fs.readFileSync(input.file, 'utf8'), sandbox);
process.stdout.write(JSON.stringify(calls));
"""

ALTS = [["en", "https://x/"], ["ko", "https://x/ko/"], ["ja", "https://x/ja/"], ["zh-Hant", "https://x/zh-Hant/"],
        ["pt-BR", "https://x/pt-BR/"], ["fr", "https://x/fr/"], ["id", "https://x/id/"]]
DESKTOP = "Mozilla/5.0 (Macintosh) Safari"


@unittest.skipUnless(NODE, "node not installed")
class SiteLangDetection(unittest.TestCase):
    def redirect(self, languages, stored=None, lang="en", ua=DESKTOP, alts=ALTS, redirect=True):
        payload = {"file": str(REPO / "assets" / "ipe-lang.js"), "lang": lang, "ua": ua, "languages": languages,
                   "stored": stored, "alts": alts, "redirect": redirect}
        out = subprocess.run([NODE, "-e", RUNNER, json.dumps(payload)], capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    def test_browser_language_redirects_root_to_matching_variant(self):
        self.assertEqual(self.redirect(["ja-JP", "en"]), ["https://x/ja/"])
        self.assertEqual(self.redirect(["ko-KR"]), ["https://x/ko/"])

    def test_region_and_legacy_codes_map_per_kit_rules(self):
        self.assertEqual(self.redirect(["zh-TW"]), ["https://x/zh-Hant/"])
        self.assertEqual(self.redirect(["zh-HK"]), ["https://x/zh-Hant/"])
        self.assertEqual(self.redirect(["zh-Hant-MO"]), ["https://x/zh-Hant/"])
        self.assertEqual(self.redirect(["pt-PT"]), ["https://x/pt-BR/"])
        self.assertEqual(self.redirect(["in-ID"]), ["https://x/id/"])

    def test_unmatched_languages_stay_on_english_root(self):
        self.assertEqual(self.redirect(["zh-CN"]), [])
        self.assertEqual(self.redirect(["xx-YY", "en-US"]), [])
        self.assertEqual(self.redirect(["ru"]), [])

    def test_first_match_wins_over_later_entries(self):
        self.assertEqual(self.redirect(["zh-CN", "fr-FR", "ja"]), ["https://x/fr/"])

    def test_stored_choice_wins_and_english_choice_stays(self):
        self.assertEqual(self.redirect(["ja"], stored="ko"), ["https://x/ko/"])
        self.assertEqual(self.redirect(["ja"], stored="en"), [])

    def test_language_bound_urls_never_redirect(self):
        self.assertEqual(self.redirect(["ja"], lang="ja", redirect=False), [])
        self.assertEqual(self.redirect(["ja"], stored="ko", lang="ja", redirect=False), [])

    def test_bots_never_redirect(self):
        self.assertEqual(self.redirect(["ja"], ua="Googlebot/2.1"), [])
        self.assertEqual(self.redirect(["ja"], ua="Lighthouse"), [])

    def test_missing_alternate_means_no_redirect(self):
        self.assertEqual(self.redirect(["th"], alts=ALTS), [])


if __name__ == "__main__":
    unittest.main()
