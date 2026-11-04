"""Original vector-like visuals drawn entirely with Pygame."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import random

import pygame

from game.config import (
    BLUE,
    CYAN,
    DARK,
    GREEN,
    HEIGHT,
    MAGENTA,
    ORANGE,
    VIOLET,
    WIDTH,
)


@lru_cache(maxsize=1)
def build_background() -> pygame.Surface:
    surface = pygame.Surface((WIDTH, HEIGHT))
    top = DARK
    bottom = (14, 12, 48)
    for y in range(HEIGHT):
        ratio = y / max(1, HEIGHT - 1)
        color = tuple(
            int(top[channel] + (bottom[channel] - top[channel]) * ratio)
            for channel in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

    haze = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(haze, (*VIOLET, 28), (770, 110), 210)
    pygame.draw.circle(haze, (*BLUE, 22), (190, 470), 240)
    surface.blit(haze, (0, 0))
    return surface


@lru_cache(maxsize=1)
def ship_surface() -> pygame.Surface:
    """Return the player's detailed twin-engine interceptor."""

    surface = pygame.Surface((72, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (*CYAN, 42), (10, 7, 58, 36))

    # Engine flames and nozzles.
    pygame.draw.polygon(surface, (*ORANGE, 100), [(16, 14), (0, 19), (16, 23)])
    pygame.draw.polygon(surface, (*ORANGE, 100), [(16, 28), (0, 33), (16, 37)])
    pygame.draw.polygon(surface, (255, 209, 92), [(14, 16), (5, 19), (14, 21)])
    pygame.draw.polygon(surface, (255, 209, 92), [(14, 30), (5, 33), (14, 35)])
    pygame.draw.rect(surface, (20, 38, 69), (13, 13, 10, 10), border_radius=3)
    pygame.draw.rect(surface, (20, 38, 69), (13, 27, 10, 10), border_radius=3)

    # Wings, armored hull, outline, and cockpit.
    pygame.draw.polygon(surface, (24, 43, 78), [(18, 16), (10, 2), (45, 17), (53, 25), (45, 33), (10, 48), (18, 34)])
    pygame.draw.polygon(surface, (41, 69, 111), [(18, 9), (68, 25), (18, 41), (29, 25)])
    pygame.draw.polygon(surface, CYAN, [(23, 12), (64, 25), (23, 38), (33, 25)], 3)
    pygame.draw.line(surface, BLUE, (21, 17), (43, 21), 2)
    pygame.draw.line(surface, BLUE, (21, 33), (43, 29), 2)
    pygame.draw.ellipse(surface, (8, 24, 51), (39, 17, 17, 16))
    pygame.draw.ellipse(surface, (151, 245, 255), (42, 19, 11, 11))
    pygame.draw.ellipse(surface, (245, 254, 255), (44, 20, 5, 4))
    pygame.draw.circle(surface, (112, 151, 203), (25, 25), 3)
    return surface


@lru_cache(maxsize=2)
def enemy_surface(kind: str) -> pygame.Surface:
    """Draw visually distinct scout and striker ships."""

    if kind == "striker":
        surface = pygame.Surface((62, 48), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (*MAGENTA, 35), (2, 5, 56, 38))
        pygame.draw.polygon(surface, (47, 27, 73), [(59, 4), (28, 10), (6, 1), (13, 17), (2, 24), (13, 31), (6, 47), (28, 38), (59, 44), (43, 24)])
        pygame.draw.polygon(surface, MAGENTA, [(54, 9), (28, 15), (13, 9), (19, 21), (8, 24), (19, 27), (13, 39), (28, 33), (54, 39), (38, 24)], 3)
        pygame.draw.circle(surface, (255, 226, 248), (29, 24), 6)
        pygame.draw.circle(surface, (119, 28, 98), (29, 24), 3)
        pygame.draw.line(surface, (255, 150, 220), (42, 16), (52, 12), 2)
        pygame.draw.line(surface, (255, 150, 220), (42, 32), (52, 36), 2)
        return surface

    surface = pygame.Surface((54, 42), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (*ORANGE, 32), (3, 4, 47, 34))
    pygame.draw.polygon(surface, (48, 38, 61), [(51, 5), (17, 9), (3, 21), (17, 33), (51, 37), (39, 21)])
    pygame.draw.polygon(surface, ORANGE, [(46, 10), (20, 13), (9, 21), (20, 29), (46, 32), (34, 21)], 3)
    pygame.draw.circle(surface, (255, 246, 219), (22, 21), 5)
    pygame.draw.circle(surface, (120, 64, 27), (22, 21), 2)
    pygame.draw.line(surface, (255, 204, 122), (35, 15), (44, 13), 2)
    pygame.draw.line(surface, (255, 204, 122), (35, 27), (44, 29), 2)
    return surface


@lru_cache(maxsize=1)
def boss_surface() -> pygame.Surface:
    surface = pygame.Surface((150, 108), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (*MAGENTA, 30), (4, 5, 141, 98))
    pygame.draw.polygon(
        surface,
        (45, 26, 73),
        [(145, 8), (60, 3), (20, 18), (3, 54), (20, 90), (60, 105), (145, 100), (116, 54)],
    )
    pygame.draw.polygon(
        surface,
        VIOLET,
        [(138, 16), (64, 11), (28, 25), (12, 54), (28, 83), (64, 97), (138, 92), (105, 54)],
        4,
    )
    pygame.draw.polygon(surface, (75, 38, 101), [(48, 22), (84, 15), (111, 33), (98, 54), (111, 75), (84, 93), (48, 86), (61, 54)])
    pygame.draw.line(surface, (213, 148, 255), (27, 35), (55, 30), 3)
    pygame.draw.line(surface, (213, 148, 255), (27, 73), (55, 78), 3)
    pygame.draw.circle(surface, MAGENTA, (82, 54), 20)
    pygame.draw.circle(surface, (96, 26, 112), (82, 54), 13)
    pygame.draw.circle(surface, (245, 250, 255), (82, 54), 7)
    pygame.draw.circle(surface, (255, 178, 229), (80, 51), 3)
    for y in (24, 43, 65, 84):
        pygame.draw.rect(surface, (21, 24, 55), (121, y - 4, 17, 8), border_radius=3)
        pygame.draw.line(surface, MAGENTA, (123, y), (136, y), 2)
    return surface


@lru_cache(maxsize=2)
def powerup_surface(kind: str) -> pygame.Surface:
    color = GREEN if kind == "repair" else CYAN
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surface, (11, 25, 50), (16, 16), 14)
    pygame.draw.circle(surface, color, (16, 16), 13, 3)
    if kind == "repair":
        pygame.draw.rect(surface, color, (13, 7, 6, 18), border_radius=2)
        pygame.draw.rect(surface, color, (7, 13, 18, 6), border_radius=2)
    else:
        pygame.draw.polygon(surface, color, [(17, 5), (9, 17), (15, 17), (13, 27), (24, 13), (18, 13)])
    return surface


@lru_cache(maxsize=4)
def projectile_surface(friendly: bool, boss_shot: bool = False) -> pygame.Surface:
    if friendly:
        surface = pygame.Surface((30, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (*CYAN, 48), (0, 0, 30, 12))
        pygame.draw.polygon(surface, (37, 145, 222), [(0, 6), (20, 2), (29, 6), (20, 10)])
        pygame.draw.ellipse(surface, (238, 254, 255), (14, 3, 14, 6))
        pygame.draw.line(surface, CYAN, (2, 6), (17, 6), 2)
        return surface

    size = (28, 16) if boss_shot else (22, 12)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (*MAGENTA, 55), surface.get_rect())
    pygame.draw.ellipse(surface, MAGENTA, surface.get_rect().inflate(-4, -4))
    core_x = 7 if boss_shot else 5
    pygame.draw.circle(surface, (255, 238, 250), (core_x, size[1] // 2), 3)
    pygame.draw.line(surface, (180, 45, 144), (core_x + 3, size[1] // 2), (size[0] - 2, size[1] // 2), 2)
    return surface


@lru_cache(maxsize=2)
def heart_surface(filled: bool) -> pygame.Surface:
    """Return a polished HUD heart without allocating every frame."""

    surface = pygame.Surface((31, 28), pygame.SRCALPHA)
    glow_color = (*MAGENTA, 42) if filled else (88, 98, 118, 24)
    pygame.draw.circle(surface, glow_color, (10, 10), 10)
    pygame.draw.circle(surface, glow_color, (21, 10), 10)
    pygame.draw.polygon(surface, glow_color, [(2, 10), (29, 10), (15, 27)])
    base = (255, 67, 105) if filled else (54, 65, 86)
    edge = (255, 174, 194) if filled else (92, 104, 126)
    pygame.draw.circle(surface, base, (10, 9), 8)
    pygame.draw.circle(surface, base, (21, 9), 8)
    pygame.draw.polygon(surface, base, [(2, 10), (29, 10), (15, 26)])
    pygame.draw.lines(surface, edge, False, [(4, 8), (8, 3), (14, 5)], 2)
    if filled:
        pygame.draw.circle(surface, (255, 226, 234), (8, 6), 3)
        pygame.draw.line(surface, (196, 38, 78), (15, 22), (25, 10), 2)
    return surface


@lru_cache(maxsize=2)
def power_aura_surface(kind: str) -> pygame.Surface:
    """Cache the player's shield/turbo aura to avoid frame-time allocations."""

    color = GREEN if kind == "shield" else CYAN
    surface = pygame.Surface((92, 70), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (*color, 32), (3, 3, 86, 64))
    pygame.draw.ellipse(surface, (*color, 105), (6, 6, 80, 58), 3)
    pygame.draw.ellipse(surface, (235, 255, 255, 50), (11, 10, 70, 48), 1)
    return surface


@dataclass(slots=True)
class Star:
    x: float
    y: float
    speed: float
    radius: int


class StarField:
    def __init__(self, count: int = 92, seed: int = 29):
        generator = random.Random(seed)
        self.stars = [
            Star(
                x=generator.uniform(0, WIDTH),
                y=generator.uniform(0, HEIGHT),
                speed=generator.uniform(18, 85),
                radius=generator.choice((1, 1, 1, 2)),
            )
            for _ in range(count)
        ]

    def update(self, dt: float) -> None:
        for star in self.stars:
            star.x -= star.speed * dt
            if star.x < -2:
                star.x = WIDTH + 2

    def draw(self, surface: pygame.Surface) -> None:
        for star in self.stars:
            brightness = min(255, int(125 + star.speed * 1.4))
            pygame.draw.circle(
                surface,
                (brightness, brightness, 255),
                (int(star.x), int(star.y)),
                star.radius,
            )
