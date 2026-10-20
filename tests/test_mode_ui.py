"""The fork's mode chips on the dictation indicator."""

import unittest
from unittest import mock

from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication

from dikte import overlay
from tests.support import DikteTest

_app = QApplication.instance() or QApplication([])


class ModeChips(DikteTest):
    def make(self, **kwargs):
        heard = []
        box = overlay.Overlay(mode_buttons=True, on_mode=heard.append, **kwargs)
        self.addCleanup(box.deleteLater)
        return box, heard

    def click(self, box, point):
        event = mock.Mock()
        event.position.return_value = point
        box.mousePressEvent(event)

    def test_a_dictation_ribbon_is_wider_by_the_chips(self):
        plain = overlay.Overlay()
        self.addCleanup(plain.deleteLater)
        box, _ = self.make()
        plain.show_recording()
        box.show_recording()
        self.assertEqual(box.width() - plain.width(), int(overlay.CHIPS_W))

    def test_clicking_a_chip_picks_its_mode(self):
        box, heard = self.make()
        box.show_recording()
        for mode, _letter, rect in box._chip_rects():
            self.click(box, rect.center())
            self.assertEqual(box.mode, mode)
        self.assertEqual(heard, ["imla", "prompt", "raw"])

    def test_a_click_beside_the_chips_changes_nothing(self):
        box, heard = self.make()
        box.show_recording()
        self.click(box, QPointF(5, 5))
        self.assertEqual((box.mode, heard), ("imla", []))

    def test_the_agent_ribbon_has_no_chips(self):
        box, _ = self.make()
        box.show_recording(asking=True)
        self.assertFalse(box._chips_shown())

    def test_chips_stay_clear_of_the_waveform(self):
        box, _ = self.make()
        box.show_recording()
        left, bar_w, step = box._bars()
        last_bar = left + (overlay.BARS - 1) * step + bar_w
        self.assertLess(last_bar, box._chip_rects()[0][2].left())


if __name__ == "__main__":
    unittest.main()
