#!/usr/bin/env python

import signal
import unittest


ON_RASPBERRY_PI = True
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # Not running on a raspberry pi with the RPi.GPIO module
    ON_RASPBERRY_PI = False

if ON_RASPBERRY_PI:
    import explorerhat


class Test_explorer(unittest.TestCase):

    @unittest.skip
    def test_touch_pressed(self):
        explorerhat.touch.pressed(lambda x,y:explorerhat.light.on())
        signal.pause()

    @unittest.skip
    def test_touch_released(self):
        explorerhat.touch.released(lambda x,y:explorerhat.light.off())
        signal.pause()


if __name__ == '__main__':
    unittest.main()