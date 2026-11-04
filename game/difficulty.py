"""Difficulty profiles shared by menus, gameplay, and persistence."""

from __future__ import annotations

from dataclasses import dataclass

from game.config import CYAN, GREEN, MAGENTA


@dataclass(frozen=True, slots=True)
class DifficultyProfile:
    """Tuning values for one complete game mode."""

    key: str
    label: str
    description: str
    color: tuple[int, int, int]
    base_enemy_count: int
    max_enemy_count: int
    enemy_growth_seconds: float
    spawn_delay_ms: int
    striker_unlock_seconds: float
    striker_chance: float
    enemy_speed_multiplier: float
    enemy_progression_seconds: float
    enemy_shot_interval_multiplier: float
    enemy_projectile_speed: float
    enemy_shot_vertical_speeds: tuple[float, ...]
    max_enemy_projectiles: int
    boss_hp: int
    boss_speed: float
    boss_shot_interval_ms: int
    boss_projectile_speed: float
    boss_shot_vertical_speeds: tuple[float, ...]


DIFFICULTIES: dict[str, DifficultyProfile] = {
    "easy": DifficultyProfile(
        key="easy",
        label="FÁCIL",
        description="Menos inimigos, tiros mais lentos e boss mais leve.",
        color=GREEN,
        base_enemy_count=1,
        max_enemy_count=4,
        enemy_growth_seconds=14.0,
        spawn_delay_ms=620,
        striker_unlock_seconds=18.0,
        striker_chance=0.20,
        enemy_speed_multiplier=0.82,
        enemy_progression_seconds=140.0,
        enemy_shot_interval_multiplier=1.40,
        enemy_projectile_speed=270.0,
        enemy_shot_vertical_speeds=(0.0,),
        max_enemy_projectiles=18,
        boss_hp=24,
        boss_speed=105.0,
        boss_shot_interval_ms=1_100,
        boss_projectile_speed=320.0,
        boss_shot_vertical_speeds=(0.0,),
    ),
    "normal": DifficultyProfile(
        key="normal",
        label="NORMAL",
        description="Ritmo equilibrado com progressão constante.",
        color=CYAN,
        base_enemy_count=2,
        max_enemy_count=7,
        enemy_growth_seconds=12.0,
        spawn_delay_ms=360,
        striker_unlock_seconds=12.0,
        striker_chance=0.34,
        enemy_speed_multiplier=1.0,
        enemy_progression_seconds=110.0,
        enemy_shot_interval_multiplier=1.0,
        enemy_projectile_speed=330.0,
        enemy_shot_vertical_speeds=(0.0,),
        max_enemy_projectiles=28,
        boss_hp=36,
        boss_speed=126.0,
        boss_shot_interval_ms=820,
        boss_projectile_speed=380.0,
        boss_shot_vertical_speeds=(-145.0, 0.0, 145.0),
    ),
    "hard": DifficultyProfile(
        key="hard",
        label="DIFÍCIL",
        description="Mais naves, rajadas duplas e boss reforçado.",
        color=MAGENTA,
        base_enemy_count=3,
        max_enemy_count=10,
        enemy_growth_seconds=8.0,
        spawn_delay_ms=220,
        striker_unlock_seconds=6.0,
        striker_chance=0.52,
        enemy_speed_multiplier=1.18,
        enemy_progression_seconds=90.0,
        enemy_shot_interval_multiplier=0.72,
        enemy_projectile_speed=410.0,
        enemy_shot_vertical_speeds=(-70.0, 70.0),
        max_enemy_projectiles=42,
        boss_hp=48,
        boss_speed=155.0,
        boss_shot_interval_ms=560,
        boss_projectile_speed=440.0,
        boss_shot_vertical_speeds=(-220.0, -110.0, 0.0, 110.0, 220.0),
    ),
}


def normalize_difficulty(value: object) -> str:
    """Return a supported key while keeping old save files compatible."""

    key = str(value).strip().lower()
    return key if key in DIFFICULTIES else "normal"


def get_difficulty(value: object) -> DifficultyProfile:
    return DIFFICULTIES[normalize_difficulty(value)]
