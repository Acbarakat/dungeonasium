import time
from functools import cached_property

# import numpy as np
import pygame
from PIL import Image
import pygame.gfxdraw
from pygame_animatedgif import AnimatedGifSprite


class GifSprite(AnimatedGifSprite):
    """A Sprite-derived class that handles animation of animated GIFs"""

    def __init__(self, position, filename, *groups):
        """
        Construct a GifSprite object.

        Args:
            position ((float, float)): A tuple with two elements
            specifying the x and y coordinates where the sprite will
            be placed.
            filename (str): Path to an animated GIF file
        """
        pygame.sprite.Sprite.__init__(self, *groups)

        self.__filename = filename

        self.playback_speed = 1
        self.scaling_factor = 1

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames) - 1
        self.startpoint = 1
        self.reversed = False

        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def __repr__(self) -> str:
        return f"<GifSprite (x: {self.rect.x}, y: {self.rect.y}, file: {self.__filename})"  # noqa: E501

    @cached_property
    def frames(self):
        return self.get_frames(self.__filename)

    @classmethod
    def get_frames(cls, filename, playback_speed=1.0):
        image = Image.open(filename)
        # base_palette = np.array(image.getpalette()).reshape((-1, 3))

        timeline = []
        all_tiles = set()
        for i in range(image.n_frames):
            image.seek(i)
            if image.tile:
                timeline.append(i)
                all_tiles.add(image.tile[0][3][0])
        all_tiles = tuple(all_tiles)

        frames = []
        duration = image.info.get("duration", 100)
        duration *= .001  # convert to milliseconds!
        duration *= playback_speed

        for frame in timeline:
            cons = False

            x0, y0, x1, y1 = (0, 0) + image.size
            image.seek(frame)

            if all_tiles in ((6,), (7,)):
                cons = True
            #     palette = np.array(image.getpalette()).reshape((-1, 3))
            # elif all_tiles in ((7, 8), (8, 7)):
            #     palette = np.array(image.getpalette()).reshape((-1, 3))
            # else:
            #     palette = base_palette

            pi = pygame.image.fromstring(image.tobytes(),
                                         image.size,
                                         image.mode)
            # pi.set_palette(palette)
            if "transparency" in image.info:
                pi.set_colorkey(image.info["transparency"])
            pi2 = pygame.Surface(image.size, pygame.SRCALPHA)
            if cons:
                for i in frames:
                    pi2.blit(i[0], (0, 0))
            pi2.blit(pi, (x0, y0), (x0, y0, x1 - x0, y1 - y0))

            frames.append([pi2, duration, playback_speed])

        return frames

    def speed_up(self):
        raise NotImplementedError()

    def slow_down(self):
        raise NotImplementedError()
