import pygame, sys, random
from constants.strings import (GameState)
from constants.settings import (
    WindowSettings,
    SoundSettings,
    InteractionSettins
)
from constants.physics import (
    PipePhysics,
    FloorPhysics,
)
from core.entities.bird import (
    Bird,
    BirdEvents,
)

def draw_floor(): 
    screen.blit(
        floor_surface,
        (floor_x_pos, FloorPhysics.FLOOR_Y_POSITION)
    )

    screen.blit(
        floor_surface,
        (floor_x_pos + WindowSettings.SCREEN_WIDTH, FloorPhysics.FLOOR_Y_POSITION)
    )


def create_pipe():
    random_pipe_positon = random.choice(pipe_height)

    bottom_pipe = pipe_surface.get_rect(
        midtop = (PipePhysics.PIPE_X_POSITION, random_pipe_positon)
    )
    
    top_pipe = pipe_surface.get_rect(
        midbottom = (PipePhysics.PIPE_X_POSITION, random_pipe_positon - 300)
    )

    return bottom_pipe, top_pipe


def move_pipes (pipes):
    for pipe in pipes:
        pipe.centerx -= PipePhysics.DISTANCE_BETWEEN_PIPES
    
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > WindowSettings.SCREEN_HEIGHT: 
            screen.blit(pipe_surface, pipe)
        else :
            flipes_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipes_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if (
            bird.rect.colliderect(pipe) or 
            bird.rect.top <= -100 or bird.rect.bottom >= 892
        ):
            DEATH_SOUND.play()
            return False     
    return True


def score_display(game_state):
    if game_state == GameState.MAIN:
        score_surface = game_font.render(
            str(round(score)),
            True, 
            (255,255,255)
        )
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)

    if game_state == GameState.GAME_OVER:
        score_surface = game_font.render(
            str(round(score)),
            True,
            (255,255,255)
        )

        score_rect = score_surface.get_rect(
            center = (288, 100)
        )

        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(
            str(round(sesstion_highest_score)), 
            True,
            (255,255,255)
        )

        high_score_rect = high_score_surface.get_rect(
            center = (288, 850)
        )

        screen.blit(high_score_surface, high_score_rect)


def update_the_highest_score(score, highest_score):
    if score > highest_score:
        highest_score = score
    
    return highest_score


pygame.mixer.pre_init(
    frequency = SoundSettings.FREQUENCY, 
    size = SoundSettings.SIZE, 
    channels = SoundSettings.CHANNELS, 
    buffer = SoundSettings.BUFFER,
)
pygame.init()

screen = pygame.display.set_mode(
    (WindowSettings.SCREEN_WIDTH, WindowSettings.SCREEN_HEIGHT)
)

window_favicon = pygame.image.load('assets/graphics/icon.png')
game_font = pygame.font.Font('assets/font/04B_19.ttf', 40)

clock = pygame.time.Clock()

pygame.display.set_icon(window_favicon)
pygame.display.set_caption(WindowSettings.WINDOW_NAME)

bird = Bird()

game_active = False
score = 0
sesstion_highest_score = 0 

green_pipe = pygame.image.load('assets/graphics/pipe-green.png').convert()
red_pipe = pygame.image.load('assets/graphics/pipe-red.png').convert()
pipe_assets = [green_pipe, red_pipe]

def randomize_pipe_asset():
    global pipe_surface
    pipe_surface = random.choice(pipe_assets)
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pygame.transform.scale2x(pipe_surface)

randomize_pipe_asset()

bg_surface = pygame.image.load('assets/graphics/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface) 

floor_surface = pygame.image.load('assets/graphics/base.png').convert() 
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0;

pipe_list = [] 
spawn_pipe = pygame.USEREVENT

pygame.time.set_timer(spawn_pipe, 1000)
pipe_height = [400,600,800]

game_over_surface = pygame.image.load('assets/graphics/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)

game_over_rect = game_over_surface.get_rect(center = (288,512))

# * Sounds
FLAP_SOUND = pygame.mixer.Sound('assets/sound/sfx_wing.wav')
DEATH_SOUND = pygame.mixer.Sound('assets/sound/sfx_die.wav')

def init_game_state():
    global pipe_list, score, game_active

    pipe_list.clear()
    bird.init_state()
    score = 0
    randomize_pipe_asset()
    game_active = True


# * Game working
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
 
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                bird.flap()

        if game_active == False:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                init_game_state()

        if event.type == spawn_pipe:
            pipe_list.extend(
                create_pipe()
            )

        if event.type == BirdEvents.BIRD_FLAP:
            bird.bird_animation_flap()

    screen.blit(bg_surface,(0,0))

    if game_active == True:
        bird.apply_gravity()
        rotated_bird = bird.align_hitbox()
        screen.blit(rotated_bird, bird.rect)
        game_active = check_collision(pipe_list)
        
        # * Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # * Score
        score_display(GameState.MAIN) 
        score += 0.008
    else:
        sesstion_highest_score = update_the_highest_score(
            score,
            sesstion_highest_score
        )
        
        score_display(GameState.GAME_OVER)

        screen.blit(game_over_surface, game_over_rect)
        
    # * floor
    floor_x_pos -= 1 

    draw_floor()

    if floor_x_pos <= -WindowSettings.SCREEN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(InteractionSettins.FPS)
