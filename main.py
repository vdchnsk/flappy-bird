import pygame , sys , random

def draw_floor(): #Повторная отрисовка пола
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576 ,900))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe , top_pipe
def move_pipes (pipes):
    for pipe in pipes:
        pipe.centerx -= 5    #5 -easy mode,10 -hard , 15 -insane
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >1024: #Если труба ниже 1024px,отрисовывается обычна текстура трубы
            screen.blit(pipe_surface,pipe)
        else : #Если труба не ниже 1024px,значит она вверху,и мы ее переварачиваем
            flipes_pipe = pygame.transform.flip(pipe_surface,False,True) #вообще хз ,что значат аргументы True и False,но это работает
            screen.blit(flipes_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):#проверяем,сталкнулись ли хитбоксы птички и трубы (True или False)
            death_sound.play()
            return False #Если мы возвращаем False,то это значение принимает переменная game_active, см. ниже

        elif bird_rect.top <= -100 or bird_rect.bottom >= 892:
            death_sound.play()
            return False        
    return True
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2 , 1) #Агрумнты:что перевырачиваем, как переварачиваем, как приближаем
    return new_bird
def bird_animation(): #Анимация крыльев
    new_bird = bird_frames[bird_index] #смена картинки на bird_index
    new_bird_rect = new_bird.get_rect(center =(100,bird_rect.centery))#хитбокс каждой картинки и ее расположение.Делаем все кадры анимации наложенными друг на друга и постоянно друг друга сменяющимися
    return new_bird , new_bird_rect

pygame.mixer.pre_init(frequency = 44100, size = 32, channels = 1, buffer = 512)#инициализация микшера звука заранее,для большей производительности
pygame.init()

def score_display(game_state):
    if game_state =="main_game":
        score_surface = game_font.render(str(round(score)), True ,(255,255,255)) #Font settings(text,anti-alised or not, color)
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
    elif game_state =="game_over":
        score_surface = game_font.render(str(round(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(str(round(the_highest_score)), True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface,high_score_rect)
def update_the_highest_score(score,the_highest_score):
    if score > the_highest_score:
        the_highest_score = score
    return the_highest_score

#Screen settings
screen = pygame.display.set_mode((576,1024))#Screen - окно ,его размещение и размер (576-w,1024-h)
clock = pygame.time.Clock()#счетчик каждров или типа того
programIcon = pygame.image.load('assets/icon.png') #favivon
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Flappy Bird by DuckoMan')
game_font = pygame.font.Font("04B_19.ttf",40)

#Ojects & their settings
gravity = 0.25
bird_movement = 0 # 0+gravity
game_active = False
score = 0
the_highest_score = 0 
random_pipe_color = random.randint(1,2)

bg_surface = pygame.image.load("assets/background-day.png").convert() #bg ;convert() конвертирует изображение из src в формат,который болле удобен pygame (необязательно)
bg_surface = pygame.transform.scale2x(bg_surface) #Увеличиваем разрещение изображения (bg) вдвое

floor_surface = pygame.image.load("assets/base.png").convert() #floor;
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0; #Начальная координата floor(нужно для анимации движения пола)

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap] #анимация птички из 3 объектов (см выше)
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))
BIRDFLAP = pygame.USEREVENT + 1 #USEREVENT может быть только один,чтобы создать несколько ,прописываем USEREVENT +1,..+2,..+3 и т.д.
pygame.time.set_timer(BIRDFLAP,200) #вся анимация проходит за 200 мс, запуск ,при событии BIRDFLAP

if random_pipe_color == 1:
        pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
elif random_pipe_color ==2:
    pipe_surface = pygame.image.load("assets/pipe-red.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] 
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [400,600,800]

game_over_surface = pygame.image.load("./assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (288,512))

#sounds
flap_sound = pygame.mixer.Sound("./sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("./sound/sfx_die.wav")

#Game working
while True:
    if random_pipe_color == 1:
        pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
    elif random_pipe_color ==2:
        pipe_surface = pygame.image.load("assets/pipe-red.png").convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    #Отслеживание событий со стороны пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #если тип события = QUIT(пользователь нажал на крестик вверху окна),то происходит закрытие окна
            pygame.quit() 
            sys.exit() #При закрытии окна пользвователем,процесс работы программы не прекращается,поэтому пользуемся библиотекой sys для прекращенеия этого самого процесса
        elif event.type == pygame.KEYDOWN : #отслеживаем нажатие любой клавиши
            if event.key == pygame.K_SPACE and game_active == True: #на пробел
                bird_movement = 0
                bird_movement = bird_movement-10
                flap_sound.play() #Звук взмаха крыльями
            elif event.key == pygame.K_SPACE and game_active == False:#Работает только тогда,когда игра окончена
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)
                score = 0
                game_active = True
                random_pipe_color = random.randint(1,2)
                game_started = False
        elif event.type == pygame.MOUSEBUTTONDOWN:# на ЛКМ
            if game_active == True: #Если клик осуществелн во время игры,то происходит прыждок
                bird_movement = 0
                bird_movement = bird_movement-10
                flap_sound.play() #Звук взмаха крыльями
                game_started = True
            elif game_active == False: #Если клик осуществелн после окончания игры,то игра начинается заново
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)
                score = 0
                random_pipe_color = random.randint(1,2)
                game_active = True 
                game_started = False
        elif event.type == SPAWNPIPE: #каждый раз ,при созданном нами событии SPAWNPIPE, выполняется функция create_pipe и координаты создания трубы записываются в массив pipe_list
            pipe_list.extend(create_pipe())
        elif event.type == BIRDFLAP:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
    #Вызов и расположение объектов
        # bg
    screen.blit(bg_surface,(0,0))

    if game_active == True:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement #настройка смещения хитбокса вместе с текстурой птички(centery ,потому что птичка падает центрально вертикально вниз(по прямой))
        screen.blit(rotated_bird,bird_rect) #размещаем птичку в своем хитбоксе
        game_active = check_collision(pipe_list)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #Score
        score_display("main_game") #см функцию выше
        score+=0.00833333333
    else :
        the_highest_score = update_the_highest_score(score,the_highest_score)
        score_display("game_over")
        screen.blit(game_over_surface, game_over_rect)
        
    # floor
    floor_x_pos -= 1 #т.к. у нас цикл while true :каждый раз к расположению по X прибавляется 1,что обеспечивает движением объект floor
    draw_floor()
    if floor_x_pos <= -576: #Когда щирина оставшейся можельки floor становется меньши или равна -576(конец экрана) ,она становится равна 0 и отрисовывается повтороно,см функцию выше
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) #ограничение fps

