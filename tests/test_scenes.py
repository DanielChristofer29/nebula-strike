from pathlib import Path
import os
import tempfile
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from game.audio import ProceduralAudio
from game.config import HEIGHT, WIDTH
from game.entities import Enemy
from game.scenes import DifficultyScene, GameScene, MenuScene
from game.storage import SaveSystem


class SceneSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        cls.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        cls.audio = ProceduralAudio(enabled=False)

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.saves = SaveSystem(Path(self.temporary_directory.name))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_menu_and_gameplay_render(self) -> None:
        menu = MenuScene(self.screen, self.audio, self.saves)
        menu.draw()
        self.assertGreater(self.screen.get_bounding_rect().width, 0)

        scene = GameScene(self.screen, self.audio, seed=29)
        scene.prepare_preview(boss=True)
        scene.draw()
        self.assertIsNotNone(scene.boss)
        self.assertGreater(self.screen.get_bounding_rect().height, 0)

    def test_loaded_lives_reach_player(self) -> None:
        progress = {"score": 120, "lives": 1, "elapsed_seconds": 23}
        scene = GameScene(self.screen, self.audio, progress=progress, seed=29)

        self.assertEqual(scene.score, 120)
        self.assertEqual(scene.player.lives, 1)
        self.assertEqual(scene.elapsed_offset, 23)
        self.assertEqual(scene.difficulty.key, "normal")

    def test_difficulty_selection_renders(self) -> None:
        scene = DifficultyScene(self.screen, self.audio)
        scene.draw()

        self.assertEqual(len(scene.buttons), 3)
        self.assertGreater(self.screen.get_bounding_rect().width, 0)

    def test_hard_mode_spawns_more_enemies(self) -> None:
        easy = GameScene(self.screen, self.audio, seed=29, difficulty="easy")
        hard = GameScene(self.screen, self.audio, seed=29, difficulty="hard")
        easy.elapsed_seconds = 24
        hard.elapsed_seconds = 24

        for now_ms in range(1_000, 15_000, 1_000):
            easy._spawn_enemies(now_ms)
            hard._spawn_enemies(now_ms)

        self.assertEqual(len(easy.enemies), 2)
        self.assertEqual(len(hard.enemies), 6)

    def test_close_event_exits_menu(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        menu = MenuScene(self.screen, self.audio, self.saves)
        self.assertEqual(menu.run(), "quit")

    def test_close_event_exits_gameplay(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        scene = GameScene(self.screen, self.audio, seed=29)
        self.assertEqual(scene.run()["status"], "quit")

    def test_boss_appears_after_thirty_seconds(self) -> None:
        scene = GameScene(self.screen, self.audio, seed=29)
        scene.session_started_at = 0
        scene.update(0.016, 30_100)
        self.assertIsNotNone(scene.boss)

    def test_hard_mode_builds_reinforced_boss(self) -> None:
        scene = GameScene(self.screen, self.audio, seed=29, difficulty="hard")
        scene.session_started_at = 0
        scene.update(0.016, 30_100)

        self.assertIsNotNone(scene.boss)
        self.assertEqual(scene.boss.max_hp, 48)
        self.assertEqual(scene.result()["difficulty"], "hard")

    def test_hard_mode_caps_enemy_projectiles(self) -> None:
        scene = GameScene(self.screen, self.audio, seed=29, difficulty="hard")
        scene.session_started_at = 90_000
        scene.enemies = [Enemy("striker", scene.rng) for _ in range(10)]
        for index, enemy in enumerate(scene.enemies):
            enemy.position.update(780, 80 + index * 32)
            enemy.last_shot_at = 0
            enemy.shot_interval_ms = 350
            enemy.sync_rect()

        for now_ms in range(100_000, 118_001, 2_000):
            scene.update(0.0, now_ms)

        self.assertLessEqual(
            len(scene.enemy_shots),
            scene.difficulty.max_enemy_projectiles,
        )


if __name__ == "__main__":
    unittest.main()
