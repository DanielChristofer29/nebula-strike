from collections import defaultdict
import os
import random
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from game.config import HEIGHT, WIDTH
from game.entities import Boss, Enemy, Player, Projectile


class EntityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT))

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def test_player_stays_inside_screen(self) -> None:
        player = Player()
        keys = defaultdict(bool)
        keys[pygame.K_LEFT] = True
        keys[pygame.K_UP] = True
        for _ in range(100):
            player.update(keys, 0.1, 0)

        self.assertEqual(player.rect.left, 0)
        self.assertEqual(player.rect.top, 0)

    def test_player_accepts_wasd_movement(self) -> None:
        player = Player()
        start = player.position.copy()
        keys = defaultdict(bool, {pygame.K_d: True, pygame.K_s: True})

        player.update(keys, 0.1, 100)

        self.assertGreater(player.position.x, start.x)
        self.assertGreater(player.position.y, start.y)

    def test_shield_absorbs_one_hit(self) -> None:
        player = Player()
        player.activate_powerup("shield", now_ms=1_000)

        self.assertEqual(player.take_damage(1_100), "shielded")
        self.assertEqual(player.lives, 3)
        self.assertEqual(player.take_damage(1_500), "damaged")
        self.assertEqual(player.lives, 2)

    def test_enemy_uses_configured_speed(self) -> None:
        enemy = Enemy("scout")
        enemy.speed = 200
        start_x = enemy.position.x
        enemy.update(0.5, elapsed_seconds=0)
        self.assertAlmostEqual(enemy.position.x, start_x - 100, places=4)

    def test_enemy_accepts_mode_multipliers(self) -> None:
        normal = Enemy("scout", random.Random(7))
        hard = Enemy(
            "scout",
            random.Random(7),
            speed_multiplier=1.2,
            shot_interval_multiplier=0.7,
        )

        self.assertAlmostEqual(hard.speed, normal.speed * 1.2)
        self.assertLess(hard.shot_interval_ms, normal.shot_interval_ms)

    def test_boss_never_leaves_vertical_bounds(self) -> None:
        boss = Boss()
        for _ in range(500):
            boss.update(0.05)
            self.assertGreaterEqual(boss.rect.top, 30)
            self.assertLessEqual(boss.rect.bottom, HEIGHT - 24)

    def test_boss_accepts_mode_configuration(self) -> None:
        boss = Boss(max_hp=48, vertical_speed=155, shot_interval_ms=560)

        self.assertEqual(boss.hp, 48)
        self.assertEqual(boss.max_hp, 48)
        self.assertEqual(boss.shot_interval_ms, 560)

    def test_projectile_reports_when_off_screen(self) -> None:
        projectile = Projectile((WIDTH + 30, 20), friendly=True)
        self.assertTrue(projectile.off_screen)


if __name__ == "__main__":
    unittest.main()
