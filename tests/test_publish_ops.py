"""ops/install_launchd.sh and ops/publish_daily.sh: install checks (KST, publish clone) and the publish path against a throw-away bare origin (no network, no real push)."""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import helpers
from helpers import REPO

OPS = REPO / "ops"
JOURNAL_LANGS = json.loads((REPO / "games.json").read_text(encoding="utf-8"))["langs"]
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def git(*args, cwd, env=None):
    r = subprocess.run(["git", *args], cwd=cwd, env={**os.environ, **GIT_ENV, **(env or {})}, capture_output=True, text=True)
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout.strip()


class InstallLaunchd(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.agents = self.tmp / "agents"

    def run_install(self, **extra):
        env = helpers.isolated_env(self.home, MOSSGARDEN_LAUNCH_AGENTS_DIR=str(self.agents), **extra)
        return sh(["bash", str(OPS / "install_launchd.sh")], env=env)

    def make_clone(self, branch="main"):
        clone = self.home / "ipe-publish" / "mossgarden-rest"
        clone.mkdir(parents=True)
        git("init", "-q", "-b", branch, cwd=clone)
        return clone

    def test_refuses_non_kst(self):
        self.make_clone()
        r = self.run_install(MOSSGARDEN_LOCAL_UTC_OFFSET="-0800")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not KST", r.stderr)
        self.assertFalse(self.agents.exists())

    def test_refuses_without_publish_clone(self):
        r = self.run_install(MOSSGARDEN_LOCAL_UTC_OFFSET="+0900")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("publish clone missing", r.stderr)
        self.assertFalse((self.agents / "rest.ipe.mossgarden-publish.plist").exists())

    def test_refuses_clone_not_on_main(self):
        self.make_clone(branch="feature/x")
        r = self.run_install(MOSSGARDEN_LOCAL_UTC_OFFSET="+0900")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not on main", r.stderr)

    def test_renders_plist_for_the_publish_clone_and_marks_it(self):
        clone = self.make_clone()
        r = self.run_install(MOSSGARDEN_LOCAL_UTC_OFFSET="+0900")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = (self.agents / "rest.ipe.mossgarden-publish.plist").read_text()
        self.assertNotIn("__HOME__", text)
        self.assertIn("%s/ipe-publish/mossgarden-rest/ops/journal_gate.sh" % self.home, text)
        self.assertIn("<key>MOSSGARDEN_PUBLISH_DIR</key><string>%s/ipe-publish/mossgarden-rest</string>" % self.home, text)
        self.assertNotIn("Developer/mossgarden-rest", text.split("<plist", 1)[1])
        self.assertEqual(git("config", "--local", "ipe.publishClone", cwd=clone), "true")
        if shutil.which("plutil"):
            self.assertEqual(sh(["plutil", "-lint", str(self.agents / "rest.ipe.mossgarden-publish.plist")]).returncode, 0)

    def test_rejects_unsafe_home(self):
        r = self.run_install(MOSSGARDEN_HOME="/tmp/a&b", MOSSGARDEN_LOCAL_UTC_OFFSET="+0900", MOSSGARDEN_SKIP_CLONE_CHECK="1")
        self.assertNotEqual(r.returncode, 0)


# Frozen copies of a real post (they satisfy the build_site content rules); the tests plant them under TODAY.
POST_KO = '---\ntitle: "첫 TestFlight 빌드가 올라간 과정"\ndescription: "MVP를 끝내고 내부 테스트용 첫 빌드를 올리기까지, 배포 스크립트가 한 번 멈춘 이야기입니다."\n---\niOS용 방치형 게임 이끼정원의 첫 MVP를, 배포 스크립트가 첫 시도를 한 번 멈춰 세운 뒤에 내부 테스트용 TestFlight 1.0.0(1)로 올렸습니다. 처리에 3분쯤 걸렸고, 심사 제출이나 외부 공개는 하지 않았습니다.\n\n## MVP에 담은 것\n\n첫 MVP는 식물 8종, 오프라인 정산, 계절, 도감, 저장, 설정까지 담아 한 덩어리로 맞췄습니다. 그리고 내부 테스트용 TestFlight 1.0.0(1)로 올렸습니다. 업로드가 처리되는 데 3분쯤 걸렸고, 심사 제출이나 외부 공개는 하지 않았습니다.\n\n## 첫 시도는 실패했습니다\n\n배포 스크립트 안에서 테스트 통과 검사(그린 게이트)를 돌릴 때, 「번호를 올리지 않는다」는 환경 변수가 테스트 쪽으로 새어 들어가 테스트가 깨졌고, 스크립트는 그 자리에서 멈췄습니다. 멈춰 준 덕분에 잘못된 빌드는 올라가지 않았습니다. 하위 프로세스가 바깥 환경을 물려받지 않도록 고친 뒤에 다시 올렸습니다.\n\n배포가 번거로워도 테스트가 그린이 아니면 올리지 않는 규칙은 계속 가져갑니다.\n\n## 자주 묻는 질문\n\n### 이끼정원의 첫 TestFlight 빌드에는 무엇이 들어 있나요?\n식물 8종, 오프라인 정산, 계절, 도감, 저장, 설정이며 내부 테스트용 1.0.0(1)로 올렸습니다.\n\n### 이끼정원은 App Store 심사에 제출됐나요?\n아니요. 이 빌드는 내부 테스트용으로만 올렸고, 심사 제출은 하지 않았습니다.\n'
POST_EN = '---\ntitle: "How the first TestFlight build went up"\ndescription: "After finishing the MVP, the first internal build went up, but the deploy script stopped us once along the way."\n---\nThe first MVP of Moss Garden, an idle game for iOS, went up to TestFlight as 1.0.0 (1) for internal testing after a deploy script stopped the first attempt. Processing took about three minutes, and the build was not submitted for review or opened to external testers.\n\n## What was in the MVP\n\nThe first MVP came together with eight plants, offline settlement, seasons, a collection book, saving and settings. We then uploaded it to TestFlight as 1.0.0 (1) for internal testing. Processing took about three minutes, and we did not submit it for review or open it to external testers.\n\n## The first attempt failed\n\nWhen the deploy script ran the green gate, an environment variable meaning "don\'t bump the build number" leaked into the tests and broke them, and the script stopped right there. Thanks to that stop, no bad build was uploaded. We fixed it so child processes no longer inherit the outer environment, then uploaded again.\n\nDeploys can be a hassle, but we keep the rule: if the tests aren\'t green, nothing ships.\n\n## FAQ\n\n### What was in the first Moss Garden TestFlight build?\nEight plants, offline settlement, seasons, a collection book, saving and settings, uploaded as 1.0.0 (1) for internal testing.\n\n### Has Moss Garden been submitted for App Store review?\nNo. This build was only uploaded for internal testing, and we did not submit it for review.\n'


@unittest.skipUnless((REPO / "vendor" / "ipe_web_kit").is_dir(), "vendor/ipe_web_kit not installed")
class PublishDaily(unittest.TestCase):
    # A synthetic post dated this day is planted in the seed (see seed_unbuilt_today): the tests must not depend on
    # which real posts the daily bot has already published, or on the wall clock (MOSSGARDEN_TODAY pins "today").
    TODAY = "2040-06-15"

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin = self.tmp / "origin.git"
        git("init", "-q", "--bare", "-b", "main", str(self.origin), cwd=self.tmp)
        # the committed state of this checkout is the "published" main
        # (seeded from a fresh single-commit repo of HEAD's tree: pushing from a shallow CI checkout is rejected)
        seed = self.tmp / "seed"
        seed.mkdir()
        subprocess.run(f"git archive HEAD | tar -x -C {seed}", shell=True, cwd=REPO, check=True)
        self.seed_unbuilt_today(seed)
        git("init", "-q", "-b", "main", cwd=seed)
        git("add", "-A", cwd=seed)
        git("commit", "-q", "-m", "seed", cwd=seed)
        git("push", "-q", str(self.origin), "HEAD:refs/heads/main", cwd=seed)
        self.clone = self.tmp / "ipe-publish" / "mossgarden-rest"
        git("clone", "-q", str(self.origin), str(self.clone), cwd=self.tmp)
        shutil.copytree(REPO / "vendor", self.clone / "vendor", dirs_exist_ok=True)
        git("config", "--local", "ipe.publishClone", "true", cwd=self.clone)
        self.add_translations_for_today()
        self.set_review(None)

    def seed_unbuilt_today(self, seed):
        """Make the seed's journal deterministic: drop real posts that are not built yet, add one unbuilt post dated TODAY (ko + en)."""
        journal = seed / "content" / "journal"
        for ko in journal.glob("????-??-??-*.md"):
            if ko.name.count(".") != 1:
                continue
            slug = ko.stem[len("2026-11-14-"):]
            if not (seed / "journal" / slug / "index.html").exists():
                for f in journal.glob(ko.stem + ".*md"):
                    f.unlink()
                ko.unlink(missing_ok=True)
        for suffix, text in (("", POST_KO), (".en", POST_EN)):
            (journal / ("%s-first-testflight%s.md" % (self.TODAY, suffix))).write_text(text, encoding="utf-8")

    def add_translations_for_today(self):
        journal = self.clone / "content" / "journal"
        en = (journal / ("%s-first-testflight.en.md" % self.TODAY)).read_text(encoding="utf-8")
        for lang in JOURNAL_LANGS:
            if lang in ("ko", "en"):
                continue
            (journal / ("%s-first-testflight.%s.md" % (self.TODAY, lang))).write_text(en, encoding="utf-8")

    def push_journal(self, msg):
        git("add", "content/journal", cwd=self.clone)
        if sh(["git", "diff", "--cached", "--quiet"], cwd=self.clone).returncode:
            git("commit", "-q", "-m", msg, cwd=self.clone)
            git("push", "-q", "origin", "HEAD:main", cwd=self.clone)

    def run_publish(self, **extra):
        opts = {"MOSSGARDEN_PUBLISH_DIR": str(self.clone), "MOSSGARDEN_SKIP_NET": "1", "MOSSGARDEN_CHECK_CMD": "true",
                "MOSSGARDEN_TODAY": self.TODAY, **GIT_ENV, **extra}
        env = helpers.isolated_env(self.tmp / "home", **opts)
        return sh(["bash", str(OPS / "publish_daily.sh")], env=env)

    def head(self, repo):
        return git("rev-parse", "HEAD" if repo == self.clone else "main", cwd=repo)

    def set_review(self, value, en=True):
        """Set (or with value=None clear) today's copy_review line in the clone and push that to origin: the review state is part of the published main."""
        for f in sorted((self.clone / "content" / "journal").glob("%s-*.md" % self.TODAY)):
            if not en and f.name.endswith(".en.md"):
                continue
            text = re.sub(r"^copy_review:.*\n", "", f.read_text(encoding="utf-8"), flags=re.M)
            if value:
                text = text.replace("\n---\n", "\ncopy_review: %s\n---\n" % value, 1)
            f.write_text(text, encoding="utf-8")
        self.push_journal("test: copy review")

    def mark_reviewed(self, value=None, en=True):
        self.set_review(value or "iris %s" % self.TODAY, en=en)

    def pending_count(self, r):
        return int(re.search(r"COPY_REVIEW_PENDING (\d+)", r.stdout).group(1))

    def test_publishes_todays_post_and_pushes_to_origin(self):
        self.mark_reviewed()
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("publish_daily: pushed ", r.stdout.strip().splitlines()[-1])
        after = self.head(self.origin)
        self.assertNotEqual(before, after)
        self.assertEqual(after, self.head(self.clone))
        self.assertEqual(git("diff", "--name-only", "--diff-filter=D", before, after, cwd=self.origin), "")
        self.assertIn("journal: publish", git("log", "-1", "--format=%s", cwd=self.origin))
        self.assertEqual(git("status", "--porcelain", cwd=self.clone), "")
        self.assertFalse((self.clone / ".git" / "publish.lock").exists())
        r2 = self.run_publish()           # second run the same day: nothing new
        self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)
        self.assertIn("nothing to publish", r2.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), after)

    def test_post_without_copy_review_is_skipped(self):
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("NO_COPY_REVIEW content/journal/%s-" % self.TODAY, r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), before)
        self.assertEqual(git("status", "--porcelain", cwd=self.clone), "")

    def test_english_version_without_copy_review_is_skipped(self):
        self.mark_reviewed(en=False)
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertIn("NO_COPY_REVIEW content/journal/%s-" % self.TODAY, r.stdout)
        self.assertIn(".en.md", r.stdout)
        self.assertEqual(self.head(self.origin), before)

    def test_malformed_copy_review_does_not_count(self):
        self.mark_reviewed(value="iris 2026/11/14")
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertIn("NO_COPY_REVIEW", r.stdout)
        self.assertEqual(self.head(self.origin), before)

    def test_all_twelve_languages_reviewed_publishes(self):
        self.mark_reviewed()
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("LANG_MISSING", r.stdout)
        self.assertNotIn("NO_COPY_REVIEW", r.stdout)
        self.assertIn("publish_daily: pushed ", r.stdout.strip().splitlines()[-1])

    def test_missing_language_file_skips(self):
        self.mark_reviewed()
        (self.clone / "content" / "journal" / ("%s-first-testflight.ja.md" % self.TODAY)).unlink()
        self.push_journal("test: drop ja")
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("LANG_MISSING content/journal/%s-first-testflight.ja.md" % self.TODAY, r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), before)

    def test_one_language_without_copy_review_skips(self):
        self.mark_reviewed()
        ja = self.clone / "content" / "journal" / ("%s-first-testflight.ja.md" % self.TODAY)
        ja.write_text(re.sub(r"^copy_review:.*\n", "", ja.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
        self.push_journal("test: ja not reviewed")
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("NO_COPY_REVIEW content/journal/%s-first-testflight.ja.md" % self.TODAY, r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), before)

    def test_already_published_post_is_not_blocked_by_missing_languages(self):
        journal = self.clone / "content" / "journal"
        self.assertTrue((journal / ("%s-first-testflight.md" % self.TODAY)).exists())
        files = {"2026-11-12-old-post%s.md" % suffix: (journal / ("%s-first-testflight%s.md" % (self.TODAY, suffix))).read_text(encoding="utf-8")
                 for suffix in ("", ".en")}
        self.add_posts_to_origin(files)
        (self.clone / "journal" / "old-post").mkdir(parents=True)
        (self.clone / "journal" / "old-post" / "index.html").write_text("<!doctype html>", encoding="utf-8")
        git("add", "journal", cwd=self.clone)
        git("commit", "-q", "-m", "test: old post published", cwd=self.clone)
        git("push", "-q", "origin", "HEAD:main", cwd=self.clone)
        self.mark_reviewed()
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("LANG_MISSING content/journal/2026-11-12", r.stdout)
        self.assertIn("publish_daily: pushed ", r.stdout.strip().splitlines()[-1])

    def add_posts_to_origin(self, files):
        for name, text in files.items():
            (self.clone / "content" / "journal" / name).write_text(text, encoding="utf-8")
        self.push_journal("test: journal posts")

    def unreviewed_copy_of(self, src, dst_name):
        text = re.sub(r"^copy_review:.*\n", "", src.read_text(encoding="utf-8"), flags=re.M)
        return {dst_name: text}

    def test_yesterdays_unreviewed_post_blocks_todays_reviewed_post(self):
        files = {}
        for src in sorted((self.clone / "content" / "journal").glob("2026-11-13-*.md")):
            files.update(self.unreviewed_copy_of(src, src.name.replace("2026-11-13-", "2026-11-13-unreviewed-")))
        self.add_posts_to_origin(files)
        self.mark_reviewed()
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("NO_COPY_REVIEW content/journal/2026-11-13-unreviewed-", r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), before)

    def test_future_unreviewed_post_does_not_block(self):
        files = {}
        for src in sorted((self.clone / "content" / "journal").glob("%s-*.md" % self.TODAY)):
            files.update(self.unreviewed_copy_of(src, "2099-01-01-future-" + src.name[len(self.TODAY) + 1:]))
        self.add_posts_to_origin(files)
        self.mark_reviewed()
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("NO_COPY_REVIEW", r.stdout)
        self.assertIn("publish_daily: pushed ", r.stdout.strip().splitlines()[-1])

    def test_copy_review_line_with_cr_and_trailing_space_counts(self):
        for f in sorted((self.clone / "content" / "journal").glob("%s-*.md" % self.TODAY)):
            text = f.read_text(encoding="utf-8").replace("\n---\n", "\ncopy_review: iris %s \r\n---\n" % self.TODAY, 1)
            f.write_bytes(text.encode("utf-8"))
        git("add", "content/journal", cwd=self.clone)
        git("commit", "-q", "-m", "test: CRLF review line", cwd=self.clone)
        git("push", "-q", "origin", "HEAD:main", cwd=self.clone)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("NO_COPY_REVIEW", r.stdout)
        self.assertIn("publish_daily: pushed ", r.stdout.strip().splitlines()[-1])

    def test_counts_unreviewed_future_posts(self):
        n = self.pending_count(self.run_publish())
        journal = self.clone / "content" / "journal"
        shutil.copy(journal / ("%s-first-testflight.md" % self.TODAY), journal / "2099-01-01-pending-check.md")
        self.push_journal("test: future post")
        self.assertEqual(self.pending_count(self.run_publish()), n + 1)

    def test_no_post_today_is_nothing_to_publish(self):
        r = self.run_publish(MOSSGARDEN_TODAY="2030-01-01")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("NO_POST", r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])

    def test_unmarked_clone_is_refused(self):
        git("config", "--local", "--unset", "ipe.publishClone", cwd=self.clone)
        r = self.run_publish()
        self.assertEqual(r.returncode, 0)
        self.assertIn("SKIP", r.stdout)
        self.assertIn("publish clone", r.stdout)

    def test_dirty_tree_and_wrong_branch_skip_without_touching_anything(self):
        (self.clone / "scratch.txt").write_text("wip")
        r = self.run_publish()
        self.assertIn("SKIP — working tree is not clean", r.stdout)
        self.assertEqual((self.clone / "scratch.txt").read_text(), "wip")
        (self.clone / "scratch.txt").unlink()
        git("checkout", "-q", "-b", "feature/x", cwd=self.clone)
        self.assertIn("not main", self.run_publish().stdout)

    def test_failed_green_gate_rolls_back_and_pushes_nothing(self):
        self.mark_reviewed()
        before, base = self.head(self.origin), self.head(self.clone)
        r = self.run_publish(MOSSGARDEN_CHECK_CMD="false")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ROLLBACK", r.stdout)
        self.assertEqual(self.head(self.origin), before)
        self.assertEqual(self.head(self.clone), base)
        self.assertEqual(git("status", "--porcelain", cwd=self.clone), "")

    def test_default_dir_is_the_publish_clone_not_the_work_clone(self):
        text = (OPS / "publish_daily.sh").read_text()
        self.assertIn("$HOME/ipe-publish/mossgarden-rest", text)
        self.assertNotIn("$HOME/Developer/mossgarden-rest", text)


if __name__ == "__main__":
    unittest.main()
