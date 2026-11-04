import os
import unittest

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game.audio import ProceduralAudio


class ProceduralAudioTests(unittest.TestCase):
    def test_laser_uses_expected_mixer_format_and_duration(self) -> None:
        pygame.init()
        audio = ProceduralAudio()

        self.assertTrue(audio.enabled)
        self.assertEqual(pygame.mixer.get_init(), (22_050, -16, 1))
        self.assertAlmostEqual(audio.sounds["shoot"].get_length(), 0.105, places=2)
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
