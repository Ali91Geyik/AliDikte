"""The fork's dictation modes: imla, prompt and raw, and the speaker's style."""

import unittest

from dikte import config as cfg
from dikte import i18n
from tests.support import DikteTest


class Modes(DikteTest):
    def test_settings_decide_unless_the_shortcut_asked_for_one(self):
        conf = cfg.Config()
        self.assertEqual(conf.dictation_mode(), "imla")
        conf["dictation_mode"] = "prompt"
        self.assertEqual(conf.dictation_mode(), "prompt")
        self.assertEqual(conf.dictation_mode("raw"), "raw")

    def test_an_unknown_mode_falls_back_to_imla(self):
        conf = cfg.Config()
        conf["dictation_mode"] = "nonsense"
        self.assertEqual(conf.dictation_mode("other"), "imla")

    def test_prompt_mode_has_its_own_rules(self):
        conf = cfg.Config()
        self.assertEqual(conf.cleanup_prompt(speech="tr", mode="prompt"),
                         cfg.PROMPT_MODE_PROMPT_TR)
        self.assertEqual(conf.cleanup_prompt(speech="en", mode="prompt"),
                         cfg.PROMPT_MODE_PROMPT_EN)
        self.assertEqual(conf.cleanup_prompt(speech="tr"), cfg.CLEANUP_PROMPT_TR)

    def test_the_glossary_reaches_prompt_mode_too(self):
        conf = cfg.Config()
        conf["transcribe_prompt"] = "Schenefeld, TankTask"
        self.assertIn("TankTask", conf.cleanup_prompt(speech="tr", mode="prompt"))

    def test_the_style_is_added_to_dictation_but_not_to_subtitles(self):
        conf = cfg.Config()
        conf["personal_style"] = "\"kanka\" der, kısa cümle kurar"
        self.assertIn("kanka", conf.cleanup_prompt(speech="tr"))
        self.assertIn("kanka", conf.cleanup_prompt(speech="tr", mode="prompt"))
        self.assertNotIn("kanka", conf.cleanup_prompt(speech="tr", subtitles=True))

    def test_no_style_means_no_style_rule(self):
        conf = cfg.Config()
        self.assertNotIn("TABİRLERİ", conf.cleanup_prompt(speech="tr"))

    def test_imla_keeps_the_expression_and_prompt_mode_translates_it(self):
        conf = cfg.Config()
        conf["personal_style"] = "gulballig yapmak - garip, alışılmadık işler yapmak"
        self.assertIn("söylediği gibi", conf.cleanup_prompt(speech="tr"))
        self.assertIn("anlamını", conf.cleanup_prompt(speech="tr", mode="prompt"))


if __name__ == "__main__":
    unittest.main()
