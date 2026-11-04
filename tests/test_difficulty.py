import unittest

from game.difficulty import DIFFICULTIES, get_difficulty, normalize_difficulty


class DifficultyTests(unittest.TestCase):
    def test_invalid_mode_falls_back_to_normal(self) -> None:
        self.assertEqual(normalize_difficulty("unknown"), "normal")
        self.assertEqual(get_difficulty(None).key, "normal")

    def test_modes_scale_enemy_pressure(self) -> None:
        easy = DIFFICULTIES["easy"]
        normal = DIFFICULTIES["normal"]
        hard = DIFFICULTIES["hard"]

        self.assertLess(easy.max_enemy_count, normal.max_enemy_count)
        self.assertLess(normal.max_enemy_count, hard.max_enemy_count)
        self.assertGreater(easy.spawn_delay_ms, normal.spawn_delay_ms)
        self.assertGreater(normal.spawn_delay_ms, hard.spawn_delay_ms)
        self.assertLess(easy.enemy_projectile_speed, normal.enemy_projectile_speed)
        self.assertLess(normal.enemy_projectile_speed, hard.enemy_projectile_speed)

    def test_modes_scale_boss_and_shot_patterns(self) -> None:
        easy = DIFFICULTIES["easy"]
        normal = DIFFICULTIES["normal"]
        hard = DIFFICULTIES["hard"]

        self.assertLess(easy.boss_hp, normal.boss_hp)
        self.assertLess(normal.boss_hp, hard.boss_hp)
        self.assertLess(
            len(easy.boss_shot_vertical_speeds),
            len(normal.boss_shot_vertical_speeds),
        )
        self.assertLess(
            len(normal.boss_shot_vertical_speeds),
            len(hard.boss_shot_vertical_speeds),
        )


if __name__ == "__main__":
    unittest.main()
