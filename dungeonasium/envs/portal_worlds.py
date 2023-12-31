import os

import numpy as np
import pygame
from PIL import Image
from IPython.display import display
from gymnasium import spaces

from ..envs.base import World2dEnv, ASSET_DIR
from ..visuals.gif import GifSprite


class PortalWorldEnv(World2dEnv):
    metadata = {
        "render_modes": ["human", "jupyter"],
        "render_fps": 15
    }

    def __init__(self,
                 render_mode: str | None = None,
                 sparse_reward: bool = True) -> None:
        super().__init__(render_mode=render_mode,
                         size=(24, 18),
                         rotate=90.0,
                         scale=0.5,
                         filepath=os.path.join(ASSET_DIR,
                                               "giants-bane-min.jpg"))
        self.sparse_reward = sparse_reward

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    np.array([0, 0]),
                    np.array(self.size),
                    shape=(2,),
                    dtype=int
                ),
                "target": spaces.Box(
                    np.array([0, 0]),
                    np.array(self.size),
                    shape=(2,),
                    dtype=int
                ),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
        self.show_grid = False
        self.sprite_group = None
        self.portal = None

        if self.window is None and self.render_mode in ("human", "jupyter"):
            # pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(self.window_size)
            self.clock = pygame.time.Clock()

            self.sprite_group = pygame.sprite.Group()

    def _get_obs(self):
        return {
            "agent": self._agent_location,
            "target": self._target_location
        }

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self._agent_location = self.np_random.integers([0, 0], self.size, size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        # self._target_location = self._agent_location
        self._target_location = np.array((9, 3))
        # self._target_location = self.np_random.integers([0, 0], self.size, size=2, dtype=int)
        # self._target_location = np.random.choice([0, self.size - 1], 1)[0]
        # self._target_location = np.array((self._target_location, self._target_location))
        while np.array_equal(self._target_location, self._agent_location):
            self._agent_location = self.np_random.integers([0, 0], self.size, size=2, dtype=int)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode in ("human", "jupyter"):
            info["img"] = self._render_frame()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid
        new_loc = np.clip(
            self._agent_location + direction,
            np.array([0, 0]),
            self.size - np.array([1, 1])
        )
        if np.array_equal(new_loc, self._agent_location):
            reward, terminated = -1, True
        else:
            self._agent_location = new_loc
            # An episode is done iff the agent has reached the target
            terminated = np.array_equal(self._agent_location,
                                        self._target_location)
            if terminated:
                reward = 1
            elif self.sparse_reward:
                reward = 0  # Binary sparse rewards
            else:
                # x to 0.005 (norm == 1)
                reward = np.reciprocal(np.linalg.norm(
                    self._agent_location - self._target_location, ord=1
                )) / 100.0

        observation = self._get_obs()
        info = self._get_info()

        img = None
        if self.render_mode in ("human", "jupyter"):
            img = self._render_frame()
        info["img"] = img

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode is not None:
            return self._render_frame()

    def _render_frame(self):
        canvas = self.bg_surface.copy()
        # The size of a single grid square in pixels
        pix_square_size = np.array(self.window_size) / np.array(self.size)
        pix_radius = np.hypot(*self.size)

        if self.portal is None:
            self.portal = GifSprite(pix_square_size * self._target_location * 0.97,
                                    os.path.join(ASSET_DIR,
                                                 "portal.gif"),
                                    self.sprite_group)
            # self.portal.speed_up()
            self.portal.scale(max(pix_square_size / self.portal.image.get_size()) * 1.3)
        self.sprite_group.update(canvas)
        self.sprite_group.draw(canvas)

        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (self._agent_location + 0.5) * pix_square_size,
            pix_radius / 3,
        )

        if self.show_grid:
            # Horizontal lines
            for x in range(self.size[0] + 1):
                pygame.draw.line(
                    canvas,
                    255,
                    (pix_square_size[0] * x, 0),
                    (pix_square_size[0] * x, self.window_size[1]),
                    width=3,
                )
            # Vertical lines
            for y in range(self.size[1] + 1):
                pygame.draw.line(
                    canvas,
                    255,
                    (0, pix_square_size[1] * y),
                    (self.window_size[0], pix_square_size[1] * y),
                    width=3,
                )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])

        elif self.render_mode == "jupyter":
            data = pygame.image.tobytes(canvas, "RGB")
            data = Image.frombytes('RGB', self.window_size, data)
            display(data)
            self.clock.tick(self.metadata["render_fps"])
            return data

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
