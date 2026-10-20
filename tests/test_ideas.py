"""Fikir mode: an idea kept word for word in the day's inbox file."""

import re
import time
import unittest

from dikte import config as cfg
from dikte import ideas
from tests.support import DikteTest
from tests import test_worker
from tests.support import make_wav, speech

NOW = time.strptime("2026-10-20 23:05:09", "%Y-%m-%d %H:%M:%S")


class Line(DikteTest):
    def test_the_capture_id_has_the_vault_s_shape(self):
        self.assertRegex(ideas.capture_id(NOW), r"^yk-20261020-230509-[0-9a-f]{4}$")

    def test_the_line_keeps_the_words_and_says_where_they_came_from(self):
        line = ideas.line("suyun  kandırma\nkuvveti", NOW, "yk-x")
        self.assertEqual(line, "- [23:05] (fikir) suyun kandırma kuvveti "
                               "<!-- yk:yk-x kanal:Bilgisayar dikte kaynak:Dikte -->")

    def test_ideas_are_appended_to_the_day_s_file(self):
        conf = cfg.Config()
        conf["idea_dir"] = str(self.path("inbox"))
        first = ideas.save("bir", conf, NOW)
        ideas.save("iki", conf, NOW)
        self.assertEqual(first.name, "2026-10-20.md")
        lines = first.read_text(encoding="utf-8").splitlines()
        self.assertEqual([re.search(r"\(fikir\) (\S+)", x).group(1) for x in lines],
                         ["bir", "iki"])

    def test_an_empty_setting_means_the_documents_folder(self):
        self.assertEqual(ideas.folder(cfg.Config()), ideas.default_dir())


class FikirChain(DikteTest):
    # The worker tests' chain, borrowed rather than inherited, so that their
    # own tests are not run again here in Fikir mode.
    run_chain = test_worker.Chain.run_chain

    def setUp(self):
        super().setUp()
        self.conf = self.config(openai_api_key="sk-test",
                                openrouter_api_key="sk-or-test")
        self.wav = make_wav(self.path("clip.wav"), speech(2.0))
        self.rms = [0.0005] * 40 + [0.2] * 20
        self.conf["dictation_mode"] = "fikir"
        self.conf["idea_dir"] = str(self.path("inbox"))

    def test_an_idea_is_saved_as_heard_and_never_pasted(self):
        run = self.run_chain()
        self.assertEqual(run["failures"], [])
        run["cleanup"].assert_not_called()
        run["copy"].assert_not_called()
        run["press"].assert_not_called()
        saved = list(self.path("inbox").glob("*.md"))
        self.assertEqual(len(saved), 1)
        self.assertIn("(fikir) uh, book it for Thursday <!-- yk:",
                      saved[0].read_text(encoding="utf-8"))

    def test_the_history_says_it_was_an_idea(self):
        self.run_chain()
        self.assertEqual(cfg.read_history()[-1]["mode"], "fikir")


if __name__ == "__main__":
    unittest.main()
