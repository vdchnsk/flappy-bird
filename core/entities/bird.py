import pygame as pg
from typing import Tuple, List, Any

class Bird:
    movement: float = 0
    movement_index: int = 0

    def __init__(self) -> None:
        frame_downflap: pg.Surface = pg.transform.scale2x(pg.image.load('assets/graphics/bluebird-downflap.png').convert_alpha())
        frame_midflap: pg.Surface = pg.transform.scale2x(pg.image.load('assets/graphics/bluebird-midflap.png').convert_alpha())
        frame_upflap: pg.Surface = pg.transform.scale2x(pg.image.load('assets/graphics/bluebird-upflap.png').convert_alpha())

        self.frames: List[pg.Surface] = [frame_downflap, frame_midflap, frame_upflap]
        self.surface: pg.Surface = self.frames[self.movement_index]
        self.rect: pg.Rect = self.surface.get_rect(center=(100, 512))

        self.flap_sound: pg.mixer.Sound = pg.mixer.Sound('assets/sound/sfx_wing.wav')

        flap_animation_interval: int = 200
        pg.time.set_timer(BirdEvents.BIRD_FLAP, flap_animation_interval)

    def init_state(self) -> None:
        self.movement = 0
        self.rect.center = (100, 512)

    def rotate_bird(self) -> pg.Surface:
        new_bird: pg.Surface = pg.transform.rotozoom(self.surface, -self.movement * 2, 1)
        return new_bird

    def bird_animation(self, movement_index: int) -> Tuple[pg.Surface, pg.Rect]:
        new_bird: pg.Surface = self.frames[movement_index]
        new_rect: pg.Rect = new_bird.get_rect(center=(100, self.rect.centery))
        return new_bird, new_rect

    def flap(self) -> None:
        self.movement = 0
        self.movement -= 10
        self.flap_sound.play()

    def bird_animation_flap(self) -> None:
        if self.movement_index < 2:
            self.movement_index += 1
        else:
            self.movement_index = 0

        self.surface, self.rect = self.bird_animation(self.movement_index)

    def align_hitbox(self) -> pg.Surface:
        rotated_bird: pg.Surface = self.rotate_bird()
        self.rect.centery += self.movement
        return rotated_bird

    def apply_gravity(self) -> None:
        self.movement += BirdPhysics.GRAVITY_FACTOR


class BirdEvents:
    BIRD_FLAP: int = pg.USEREVENT + 1


class BirdPhysics:
    GRAVITY_FACTOR: float = 0.25
    MIN_EXISTING_HEIGHT: int = 0  # Assuming this should be an int, but you might need to adjust based on your use case
    MAX_EXISTING_HEIGHT: int = 0  # Fixed typo from MSX to MAX, adjust the type as necessary

