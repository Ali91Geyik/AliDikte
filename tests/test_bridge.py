"""The Claude bridge: a command rewritten as a prompt, answered in a panel."""

import unittest
from unittest import mock

from PyQt6.QtWidgets import QApplication

from dikte import answer_panel
from dikte import assistant
from dikte import config as cfg
from tests import test_worker
from tests.support import DikteTest, make_wav, speech

_app = QApplication.instance() or QApplication([])


class BridgeChain(DikteTest):
    run_chain = test_worker.Chain.run_chain

    def setUp(self):
        super().setUp()
        self.conf = self.config(openai_api_key="sk-test",
                                openrouter_api_key="sk-or-test")
        self.wav = make_wav(self.path("clip.wav"), speech(2.0))
        self.rms = [0.0005] * 40 + [0.2] * 20
        self.conf["claude_bridge"] = True

    def test_the_command_goes_as_a_prompt_and_nothing_is_pasted(self):
        run = self.run_chain(ask=True)
        self.assertEqual(run["failures"], [])
        prompt = run["cleanup"].call_args.args[3]
        self.assertEqual(prompt, self.conf.cleanup_prompt(speech="en", mode="prompt"))
        self.assertEqual(run["ask"].call_args.args[0], "Book it for Thursday.")
        run["press"].assert_not_called()

    def test_off_it_is_the_command_as_before(self):
        self.conf["claude_bridge"] = False
        run = self.run_chain(ask=True)
        run["cleanup"].assert_not_called()
        run["press"].assert_called_once()

    def test_a_dictation_is_not_touched_by_it(self):
        run = self.run_chain()
        prompt = run["cleanup"].call_args.args[3]
        self.assertEqual(prompt, self.conf.cleanup_prompt(speech="en"))
        run["press"].assert_called_once()


class Terminal(DikteTest):
    def conf(self, **values):
        conf = cfg.Config()
        conf["assistant_provider"] = "claude"
        conf["assistant_dir"] = str(self.root)
        for key, value in values.items():
            conf[key] = value
        return conf

    def which(self, *found):
        return mock.patch.object(assistant.shutil, "which",
                                 side_effect=lambda name: name if name in found else None)

    def test_the_conversation_is_resumed_in_windows_terminal(self):
        with self.which("claude", "wt"), \
                mock.patch.object(assistant, "read_session", return_value="abc"):
            self.assertEqual(assistant.terminal_command(self.conf()),
                             ["wt", "-d", str(self.root), "claude", "--resume", "abc"])

    def test_without_one_claude_runs_in_a_console_of_its_own(self):
        with self.which("claude"), \
                mock.patch.object(assistant, "read_session", return_value=""):
            self.assertEqual(assistant.terminal_command(self.conf()), ["claude"])

    def test_another_agent_has_no_claude_conversation_to_open(self):
        with self.which("claude", "wt"):
            self.assertIsNone(assistant.terminal_command(
                self.conf(assistant_provider="codex")))


class Panel(DikteTest):
    def test_the_answer_is_shown_with_the_question_and_its_buttons(self):
        continued = []
        panel = answer_panel.AnswerPanel(on_continue=lambda: continued.append(1))
        self.addCleanup(panel.deleteLater)
        panel.show_answer("yarın üçe toplantı ekle", "**Eklendi.**", "")
        self.assertEqual(panel.answer.toPlainText(), "Eklendi.")
        self.assertTrue(panel.warning.isHidden())
        panel.continue_button.click()
        self.assertEqual(continued, [1])
        self.assertFalse(panel.isVisible())

    def test_copy_takes_the_plain_text(self):
        panel = answer_panel.AnswerPanel()
        self.addCleanup(panel.deleteLater)
        panel.show_answer("soru", "*cevap*")
        panel.copy()
        self.assertEqual(QApplication.clipboard().text(), "cevap")


if __name__ == "__main__":
    unittest.main()
