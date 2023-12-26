import pygame as pg


class Bird:
    movement = 0
    movement_index = 0

    def __init__(self):
        bird_downflap = pg.transform.scale2x(pg.image.load(
            'assets/graphics/bluebird-downflap.png').convert_alpha()
        )
        bird_midflap = pg.transform.scale2x(pg.image.load(
            'assets/graphics/bluebird-midflap.png').convert_alpha()
        )
        bird_upflap = pg.transform.scale2x(pg.image.load(
            'assets/graphics/bluebird-upflap.png').convert_alpha()
        )

        self.frames = [bird_downflap, bird_midflap, bird_upflap]
        self.surface = self.frames[self.movement_index]
        self.rect = self.surface.get_rect(center=(100, 512))

        self.FLAP_SOUND = pg.mixer.Sound('assets/sound/sfx_wing.wav')

        pg.time.set_timer(BirdEvents.BIRD_FLAP, 200)

    def init_state(self):
        self.movement = 0
        self.rect.center = (100, 512)

    def rotate_bird(self):
        new_bird = pg.transform.rotozoom(
            self.surface, - self.movement * 2, 1
        )
        return new_bird

    def bird_animation(self, movement_index):
        new_bird = self.frames[movement_index]
        new_rect = new_bird.get_rect(
            center=(100, self.rect.centery)
        )
        return new_bird, new_rect

    def flap(self):
        self.movement = 0
        self.movement -= 10
        self.FLAP_SOUND.play()

    def bird_animation_flap(self):
        if self.movement_index < 2:
            self.movement_index += 1
        else:
            self.movement_index = 0

        self.surface, self.rect = self.bird_animation(self.movement_index)

    def align_hitbox(self):
        rotated_bird = self.rotate_bird()
        # setting the way how hitbox moves with the bird's texture
        self.rect.centery += self.movement
        return rotated_bird

    def apply_gravity(self):
        self.movement += BirdPhysics.GRAVITY_FACTOR


class BirdEvents:
    def __init__():
        pass

    BIRD_FLAP = pg.USEREVENT + 1


class BirdPhysics:
    def __init__():
        pass

    GRAVITY_FACTOR = 0.25
    MIN_EXISTING_HEIGHT = 0
    MSX_EXISTING_HEIGHT = 0
