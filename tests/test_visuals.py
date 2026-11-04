import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game.config import HEIGHT, WIDTH
from game.visuals import (
    build_background,
    heart_surface,
    projectile_surface,
    ship_surface,
)


class VisualCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT))

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def test_static_surfaces_are_reused(self) -> None:
        self.assertIs(build_background(), build_background())
        self.assertIs(ship_surface(), ship_surface())
        self.assertIs(heart_surface(True), heart_surface(True))
        self.assertIs(projectile_surface(True), projectile_surface(True))

    def test_new_ship_and_hearts_have_visible_pixels(self) -> None:
        self.assertGreater(ship_surface().get_bounding_rect().width, 50)
        self.assertGreater(heart_surface(True).get_bounding_rect().height, 20)
        self.assertGreater(heart_surface(False).get_bounding_rect().height, 20)


if __name__ == "__main__":
    unittest.main()
