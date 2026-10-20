"""Cleanup over Anthropic's own Messages API: the fork's direct Claude provider."""

import unittest
from unittest import mock

from dikte import api
from dikte import cleanup
from dikte import config as cfg
from tests.support import DikteTest, fake_urlopen, sent_json


def messages_reply(text, stop_reason="end_turn"):
    return {"content": [{"type": "text", "text": text}], "stop_reason": stop_reason}


class AnthropicCleanup(DikteTest):
    def call(self, *replies, **kwargs):
        with fake_urlopen(*replies) as calls:
            result = api.anthropic_cleanup("ıı merhaba", "sk-ant-test",
                                           "claude-haiku-5-5", "metni temizle",
                                           **kwargs)
        return result, calls

    def test_the_cleaned_text_comes_back(self):
        result, _ = self.call(messages_reply("  Merhaba.  "))
        self.assertEqual(result, "Merhaba.")

    def test_it_goes_to_messages_with_the_key_in_its_own_header(self):
        _, calls = self.call(messages_reply("Merhaba."))
        request = calls[0]
        self.assertEqual(request.full_url, "https://api.anthropic.com/v1/messages")
        self.assertEqual(request.unredirected_hdrs.get("X-api-key"), "sk-ant-test")
        self.assertNotIn("X-api-key", request.headers)
        self.assertEqual(request.headers.get("Anthropic-version"),
                         api.ANTHROPIC_VERSION)
        self.assertNotIn("Authorization", request.unredirected_hdrs)

    def test_the_prompt_and_the_transcript_are_kept_apart(self):
        _, calls = self.call(messages_reply("Merhaba."))
        payload = sent_json(calls[0])
        self.assertEqual(payload["system"], "metni temizle")
        self.assertEqual(payload["model"], "claude-haiku-5-5")
        self.assertEqual(payload["temperature"], 0)
        self.assertEqual(payload["messages"][0]["content"],
                         "<transcript>\nıı merhaba\n</transcript>")

    def test_an_empty_key_is_refused_before_any_request(self):
        with fake_urlopen(messages_reply("x")) as calls:
            with self.assertRaises(api.ApiError):
                api.anthropic_cleanup("x", "", "claude-haiku-5-5", "p")
        self.assertEqual(calls, [])

    def test_a_reply_cut_off_at_the_ceiling_is_refused(self):
        with self.assertRaises(api.ApiError):
            self.call(messages_reply("Yarım", stop_reason="max_tokens"))

    def test_an_empty_reply_is_refused(self):
        with self.assertRaises(api.ApiError):
            self.call({"content": [], "stop_reason": "end_turn"})


class Provider(DikteTest):
    def test_the_chain_reaches_it_with_the_stored_key_and_model(self):
        conf = cfg.Config()
        conf["cleanup_provider"] = "anthropic"
        conf["anthropic_api_key"] = "sk-ant-stored"
        with mock.patch.object(api, "anthropic_cleanup",
                               return_value="Tamam.") as call:
            self.assertEqual(cleanup.run("ıı tamam", conf, "kurallar"), "Tamam.")
        args = call.call_args
        self.assertEqual(args.args[:4],
                         ("ıı tamam", "sk-ant-stored", "claude-haiku-5-5", "kurallar"))
        self.assertEqual(cleanup.model(conf), "claude-haiku-5-5")
        self.assertEqual(cleanup.executable("anthropic"), "")

    def test_the_environment_variable_stands_in_for_an_empty_field(self):
        conf = cfg.Config()
        with mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-env"}):
            self.assertEqual(conf.anthropic_key(), "sk-ant-env")


if __name__ == "__main__":
    unittest.main()
