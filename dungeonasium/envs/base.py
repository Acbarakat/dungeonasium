import os
from functools import cached_property
from typing import Tuple

import pygame
from gymnasium import Env

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

class BaseWorldEnv(Env):
    def __init__(self,
                 render_mode: str | None = None) -> None:
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode


class World2dEnv(BaseWorldEnv):
    def __init__(self,
                 filepath: str,
                 size: Tuple[int, int],
                 rotate: float = 0.0,
                 scale: float = 0.0,
                 render_mode: str | None = None) -> None:
        super().__init__(render_mode)

        self.bg_surface = pygame.image.load(filepath)
        if rotate != 0.0:
            self.bg_surface = pygame.transform.rotate(self.bg_surface, rotate)
        if scale != 0.0:
            self.bg_surface = pygame.transform.scale_by(self.bg_surface, scale)
        self.size = size
        self.metadata["size"] = size

    @cached_property
    def window_size(self):
        return self.bg_surface.get_size()
