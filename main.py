import pygame, sys, random
from constants.Strings import (GameState)
from constants.Settings import (WindowSettings)
from constants.Physics import (PipePhysics)

def draw_floor(): 
    screen.blit(
        floor_surface,
        (floor_x_pos, FloorPhysics.FLOOR_Y_POSITION)
    )

    screen.blit(
        floor_surface,
        (
            floor_x_pos + WindowSettings.SCREEN_WIDTH, 
            FloorPhysics.FLOOR_Y_POSITION
        )
    )


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(
        midtop = (700, random_pipe_pos)
    )
    top_pipe = pipe_surface.get_rect(
        midbottom = (700, random_pipe_pos - 300)
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
        if bird_rect.colliderect(pipe):
            DEATH_SOUND.play()
            return False

        elif bird_rect.top <= -100 or bird_rect.bottom >= 892:
            DEATH_SOUND.play()
            return False        
    
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom( # args: what are we rotating, how we are doing that, scale level 
        bird, - bird_movement * 2, 1    
    )

    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(
        center = (100, bird_rect.centery)
    )

    return new_bird, new_bird_rect


pygame.mixer.pre_init(
    frequency = 44100, 
    size = 32, 
    channels = 1, 
    buffer = 512
)

pygame.init()

def score_display(game_state):
    if game_state == GameState.MAIN:
        score_surface = game_font.render(
            str(round(score)),
            True, 
            (255,255,255)
        )
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)

    elif game_state == GameState.GAME_OVER:
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

# * Screen settings
screen = pygame.display.set_mode(
    (WindowSettings.SCREEN_WIDTH, WindowSettings.SCREEN_HEIGHT)
)

windowFavicon = pygame.image.load('assets/icon.png') # * favicon
game_font = pygame.font.Font('04B_19.ttf',40)

clock = pygame.time.Clock()

pygame.display.set_icon(windowFavicon)
pygame.display.set_caption(WindowSettings.WINDOW_NAME)


# * Ojects & their settings
GRAVITY_FACTOR = 0.25
bird_movement = 0 
game_active = False
score = 0
sesstion_highest_score = 0 
random_pipe_color = random.randint(1,2)

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface) 

floor_surface = pygame.image.load('assets/base.png').convert() 
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0;

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())

bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]

bird_rect = bird_surface.get_rect(center = (100, 512))

bird_flap = pygame.USEREVENT + 1 

pygame.time.set_timer(bird_flap, 200) 

if random_pipe_color == 1:
        pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
elif random_pipe_color ==2:
    pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = [] 
spawn_pipe = pygame.USEREVENT

pygame.time.set_timer(spawn_pipe, 1000)
pipe_height = [400,600,800]

game_over_surface = pygame.image.load('./assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (288,512))

# * Sounds
FLAP_SOUND = pygame.mixer.Sound('./sound/sfx_wing.wav')
DEATH_SOUND = pygame.mixer.Sound('./sound/sfx_die.wav')

# * Game working
while True:
    for event in pygame.event.get():
        if random_pipe_color == 1:
            pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
        elif random_pipe_color ==2:
            pipe_surface = pygame.image.load('assets/pipe-red.png').convert()

        pipe_surface = pygame.transform.scale2x(pipe_surface)

        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

        elif event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_SPACE and game_active == True: 
                bird_movement = 0
                bird_movement = bird_movement-10
                FLAP_SOUND.play() 

            elif event.key == pygame.K_SPACE and game_active == False: # Works, when the game has been finished
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)
                score = 0
                game_active = True
                random_pipe_color = random.randint(1,2)
                game_started = False

        elif event.type == pygame.MOUSEBUTTONDOWN:# на ЛКМ
            if game_active == True:
                bird_movement = 0
                bird_movement = bird_movement-10
                FLAP_SOUND.play()
                game_started = True

            elif game_active == False: 
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)
                score = 0
                random_pipe_color = random.randint(1,2)
                game_active = True 
                game_started = False

        elif event.type == spawn_pipe:
            pipe_list.extend(create_pipe())

        elif event.type == bird_flap:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    screen.blit(bg_surface,(0,0))

    if game_active == True:
        # * bird
        bird_movement += GRAVITY_FACTOR
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement #setting the way how hitbox moves with the bird's texture
        screen.blit(rotated_bird,bird_rect) # setting the bird's texture inside of its texture
        game_active = check_collision(pipe_list)
        
        # * Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # * Score
        score_display('main_game') 
        score+=0.00833333333
    else :
        sesstion_highest_score = update_the_highest_score(score, sesstion_highest_score)
        score_display('game_over')
        screen.blit(game_over_surface, game_over_rect)
        
    # * floor
    floor_x_pos -= 1 
    draw_floor()
    if floor_x_pos <= - WindowSettings.SCREEN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) # * setting FPS 
