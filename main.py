#!/usr/bin/env python3
"""
كِسرة (Kesra) — Infinite Egyptian Brick-Breaker
Python + Pygame edition

Run locally:   python main.py
Web (Pygbag):  pygbag main.py
"""
import asyncio
import pygame
from settings import W, H, FPS, TITLE
from state import GameState
from scenes import MenuScene, PlayScene, GameOverScene


async def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()

    gs     = GameState()
    scene_name = "menu"
    scene      = MenuScene(gs)

    running = True
    while running:
        dt     = clock.tick(FPS) / 1000.0
        dt     = min(dt, 0.05)   # cap at 50ms (avoid spiral-of-death on lag)
        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                running = False

        result = scene.update(dt, events)
        scene.draw(screen)
        pygame.display.flip()

        if result == "quit":
            running = False
        elif result == "play":
            scene_name = "play"
            scene      = PlayScene(gs)
        elif result == "menu":
            scene_name = "menu"
            scene      = MenuScene(gs)
        elif result == "game_over":
            scene_name = "game_over"
            scene      = GameOverScene(gs)
        elif result == "restart":
            scene_name = "play"
            scene      = PlayScene(gs)

        await asyncio.sleep(0)   # yield to browser event loop (Pygbag)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
