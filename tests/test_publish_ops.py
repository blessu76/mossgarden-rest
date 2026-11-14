"""ops/install_launchd.sh and ops/publish_daily.sh: install checks (KST, publish clone) and the publish path against a throw-away bare origin (no network, no real push)."""
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


@unittest.skipUnless((REPO / "vendor" / "ipe_web_kit").is_dir(), "vendor/ipe_web_kit not installed")
class PublishDaily(unittest.TestCase):
    TODAY = "2026-11-14"        # a post dated this day exists in content/journal/ but is not built into the committed site yet

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin = self.tmp / "origin.git"
        git("init", "-q", "--bare", "-b", "main", str(self.origin), cwd=self.tmp)
        # the committed state of this checkout is the "published" main
        git("push", "-q", str(self.origin), "HEAD:refs/heads/main", cwd=REPO)
        self.clone = self.tmp / "ipe-publish" / "mossgarden-rest"
        git("clone", "-q", str(self.origin), str(self.clone), cwd=self.tmp)
        shutil.copytree(REPO / "vendor", self.clone / "vendor", dirs_exist_ok=True)
        git("config", "--local", "ipe.publishClone", "true", cwd=self.clone)
        self.set_review(None)

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
        git("add", "content/journal", cwd=self.clone)
        if sh(["git", "diff", "--cached", "--quiet"], cwd=self.clone).returncode:
            git("commit", "-q", "-m", "test: copy review", cwd=self.clone)
            git("push", "-q", "origin", "HEAD:main", cwd=self.clone)

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
        self.assertIn("NO_COPY_REVIEW — content/journal/%s-" % self.TODAY, r.stdout)
        self.assertIn("nothing to publish", r.stdout.strip().splitlines()[-1])
        self.assertEqual(self.head(self.origin), before)
        self.assertEqual(git("status", "--porcelain", cwd=self.clone), "")

    def test_english_version_without_copy_review_is_skipped(self):
        self.mark_reviewed(en=False)
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertIn("NO_COPY_REVIEW — content/journal/%s-" % self.TODAY, r.stdout)
        self.assertIn(".en.md", r.stdout)
        self.assertEqual(self.head(self.origin), before)

    def test_malformed_copy_review_does_not_count(self):
        self.mark_reviewed(value="iris 2026/11/14")
        before = self.head(self.origin)
        r = self.run_publish()
        self.assertIn("NO_COPY_REVIEW", r.stdout)
        self.assertEqual(self.head(self.origin), before)

    def test_counts_unreviewed_future_posts(self):
        n = self.pending_count(self.run_publish())
        journal = self.clone / "content" / "journal"
        for src in sorted(journal.glob("%s-*.md" % self.TODAY)):
            suffix = ".en.md" if src.name.endswith(".en.md") else ".md"
            shutil.copy(src, journal / ("2099-01-01-pending-check" + suffix))
        git("add", "content/journal", cwd=self.clone)
        git("commit", "-q", "-m", "test: future post", cwd=self.clone)
        git("push", "-q", "origin", "HEAD:main", cwd=self.clone)
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
