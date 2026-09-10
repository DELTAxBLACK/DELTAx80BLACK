"""
Tests for scanner.py: wordlist validation/loading, and
enumerate_subdomains' error handling + counter safety under
concurrency.

Run from the project root:
    python3 -m unittest discover -s tests -v
or, if pytest is available:
    pytest tests/ -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import ScanConfig
from scanner import (
    SubdomainResult,
    _is_valid_subdomain_word,
    enumerate_subdomains,
    load_wordlist,
)


class TestIsValidSubdomainWord(unittest.TestCase):
    def test_valid_single_label(self):
        self.assertTrue(_is_valid_subdomain_word("admin"))
        self.assertTrue(_is_valid_subdomain_word("cloudflare-resolve-to"))
        self.assertTrue(_is_valid_subdomain_word("api2"))

    def test_valid_dotted_label(self):
        self.assertTrue(_is_valid_subdomain_word("dev.api"))

    def test_rejects_descriptive_text(self):
        # The exact string that broke the original scanner.
        self.assertFalse(
            _is_valid_subdomain_word(
                "A new wordlist will be automatically added here before "
                "the subdomain scan is initiated."
            )
        )

    def test_rejects_leading_or_trailing_hyphen(self):
        self.assertFalse(_is_valid_subdomain_word("-admin"))
        self.assertFalse(_is_valid_subdomain_word("admin-"))

    def test_rejects_empty_label(self):
        self.assertFalse(_is_valid_subdomain_word(""))
        self.assertFalse(_is_valid_subdomain_word("admin..api"))

    def test_rejects_label_over_63_chars(self):
        self.assertFalse(_is_valid_subdomain_word("a" * 64))
        self.assertTrue(_is_valid_subdomain_word("a" * 63))

    def test_rejects_whitespace(self):
        self.assertFalse(_is_valid_subdomain_word("admin panel"))
        self.assertFalse(_is_valid_subdomain_word("admin\tpanel"))


class TestLoadWordlist(unittest.TestCase):
    def _write(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        tmp.write(text)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)

    def test_normal_wordlist(self):
        result = load_wordlist(self._write("admin\napi\nwww\n"))
        self.assertEqual(result.valid, ["admin", "api", "www"])
        self.assertEqual(result.skipped_total, 0)
        self.assertEqual(result.total_lines, 3)

    def test_blank_lines_skipped(self):
        result = load_wordlist(self._write("admin\n\n\n   \napi\n"))
        self.assertEqual(result.valid, ["admin", "api"])
        self.assertEqual(result.skipped_blank, 3)

    def test_comments_skipped(self):
        result = load_wordlist(
            self._write("# common panel names\nadmin\n# another note\napi\n")
        )
        self.assertEqual(result.valid, ["admin", "api"])
        self.assertEqual(result.skipped_comment, 2)

    def test_descriptive_placeholder_text_skipped(self):
        # Regression test: this is the literal shipped wordlist.txt content.
        result = load_wordlist(
            self._write(
                "A new wordlist will be automatically added here before "
                "the subdomain scan is initiated.\n"
            )
        )
        self.assertEqual(result.valid, [])
        self.assertEqual(result.skipped_invalid, 1)
        self.assertEqual(result.total_lines, 1)

    def test_malformed_hostname_skipped(self):
        result = load_wordlist(
            self._write("admin\nadmin@panel\nvalid-one\nadmin..dup\n")
        )
        self.assertIn("admin", result.valid)
        self.assertIn("valid-one", result.valid)
        self.assertNotIn("admin@panel", result.valid)
        self.assertGreaterEqual(result.skipped_invalid, 2)

    def test_duplicate_entries_case_insensitive(self):
        result = load_wordlist(self._write("admin\nAdmin\nADMIN\napi\n"))
        # First-seen casing is kept, later case-variants are dropped.
        self.assertEqual(result.valid, ["admin", "api"])
        self.assertEqual(result.skipped_duplicate, 2)

    def test_valid_subdomains_pass_through_unchanged(self):
        result = load_wordlist(self._write("mail\nftp\nstaging\nvpn\n"))
        self.assertEqual(result.valid, ["mail", "ftp", "staging", "vpn"])

    def test_mixed_realistic_wordlist(self):
        result = load_wordlist(
            self._write(
                "# seclists-style subset\n"
                "\n"
                "admin\n"
                "api\n"
                "admin\n"
                "A new wordlist will be automatically added here before the subdomain scan is initiated.\n"
                "www\n"
            )
        )
        self.assertEqual(result.valid, ["admin", "api", "www"])
        self.assertEqual(result.skipped_comment, 1)
        self.assertEqual(result.skipped_blank, 1)
        self.assertEqual(result.skipped_duplicate, 1)
        self.assertEqual(result.skipped_invalid, 1)
        self.assertEqual(result.total_lines, 7)


class TestEnumerateSubdomains(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _wordlist(self, text: str) -> Path:
        path = Path(self.tmpdir.name) / "wordlist.txt"
        path.write_text(text)
        return path

    def test_placeholder_only_wordlist_raises_clear_actionable_error(self):
        path = self._wordlist(
            "A new wordlist will be automatically added here before "
            "the subdomain scan is initiated.\n"
        )
        cfg = ScanConfig(wordlist_path=path, max_concurrency=5)
        with self.assertRaises(ValueError) as ctx:
            enumerate_subdomains("katabump.com", cfg)
        self.assertIn("No usable subdomain entries", str(ctx.exception))
        self.assertIn("--update-wordlist", str(ctx.exception))

    def test_missing_wordlist_still_raises_file_not_found(self):
        cfg = ScanConfig(wordlist_path=Path(self.tmpdir.name) / "missing.txt")
        with self.assertRaises(FileNotFoundError):
            enumerate_subdomains("example.com", cfg)

    @patch("scanner._check_one")
    def test_valid_subdomains_found_are_collected(self, mock_check_one):
        path = self._wordlist("admin\napi\nmissing\n")

        def side_effect(session, word, domain, timeout):
            if word in ("admin", "api"):
                return SubdomainResult(
                    subdomain=word, url=f"https://{word}.{domain}", status_code=200
                )
            return None

        mock_check_one.side_effect = side_effect
        cfg = ScanConfig(wordlist_path=path, max_concurrency=3)
        found = []
        report = enumerate_subdomains("example.com", cfg, on_found=found.append)

        self.assertEqual({r.subdomain for r in report.results}, {"admin", "api"})
        self.assertEqual(len(found), 2)
        self.assertEqual(report.wordlist_valid_entries, 3)
        self.assertEqual(report.wordlist_skipped_entries, 0)

    @patch("scanner._check_one")
    def test_one_bad_worker_does_not_abort_the_whole_sweep(self, mock_check_one):
        # Simulates something slipping past validation and _check_one
        # raising mid-sweep -- the run must finish and count it, not crash.
        path = self._wordlist("good1\ngood2\nbad\n")

        def side_effect(session, word, domain, timeout):
            if word == "bad":
                raise ValueError("simulated worker failure")
            return None

        mock_check_one.side_effect = side_effect
        cfg = ScanConfig(wordlist_path=path, max_concurrency=3)
        report = enumerate_subdomains("example.com", cfg)

        self.assertEqual(report.subdomains_checked, 3)
        self.assertEqual(report.errors, 1)

    @patch("scanner._check_one")
    def test_counters_are_consistent_under_concurrency(self, mock_check_one):
        # 200 words at concurrency=40, deterministic outcome per word.
        # If report.errors/report.results were written from worker
        # threads instead of the main thread, this would flake.
        words_text = "\n".join(f"host{i}" for i in range(200))
        path = self._wordlist(words_text)

        def side_effect(session, word, domain, timeout):
            n = int(word.replace("host", ""))
            if n % 10 == 0:
                raise RuntimeError("simulated failure")
            if n % 3 == 0:
                return SubdomainResult(
                    subdomain=word, url=f"https://{word}.{domain}", status_code=200
                )
            return None

        mock_check_one.side_effect = side_effect
        expected_errors = len([i for i in range(200) if i % 10 == 0])
        expected_found = len(
            [i for i in range(200) if i % 3 == 0 and i % 10 != 0]
        )

        for _ in range(5):  # repeat to make a real race more likely to surface
            cfg = ScanConfig(wordlist_path=path, max_concurrency=40)
            report = enumerate_subdomains("example.com", cfg)
            self.assertEqual(report.subdomains_checked, 200)
            self.assertEqual(report.wordlist_valid_entries, 200)
            self.assertEqual(report.errors, expected_errors)
            self.assertEqual(len(report.results), expected_found)


if __name__ == "__main__":
    unittest.main()
