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
        pipe.centerx -= 5
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
            return False #Если мы возвращаем False,то это значение принимает переменная game_active, см. ниже
        elif bird_rect.top <= -100 or bird_rect.bottom >= 902:
            return False
            
    return True

pygame.init()

#Screen settings
screen = pygame.display.set_mode((576,1024))#Screen - окно ,его размещение и размер (576-w,1024-h)
clock = pygame.time.Clock()#счетчик каждров или типа того

#Ojects & their settings
gravity = 0.25
bird_movement = 0
game_active = True


bg_surface = pygame.image.load("assets/background-day.png").convert() #bg ;convert() конвертирует изображение из src в формат,который болле удобен pygame (необязательно)
bg_surface = pygame.transform.scale2x(bg_surface) #Увеличиваем разрещение изображения (bg) вдвое

floor_surface = pygame.image.load("assets/base.png").convert() #floor;
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0; #Начальная координата floor(нужно для анимации движения пола)

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512)) #хитбокс птички

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] 
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [400,600,800]
#Game working
while True:
    #Отслеживание событий со стороны пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #если тип события = QUIT(пользователь нажал на крестик вверху окна),то происходит закрытие окна
            pygame.quit() 
            sys.exit() #При закрытии окна пользвователем,процесс работы программы не прекращается,поэтому пользуемся библиотекой sys для прекращенеия этого самого процесса
        elif event.type == pygame.KEYDOWN : #отслеживаем нажатие любой клавиши
            if event.key == pygame.K_SPACE and game_active == True: #на пробел
                bird_movement = 0
                bird_movement = bird_movement-10
            elif event.key == pygame.K_SPACE and game_active == False:#Работает только тогда,когда игра окончена
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (100,512)
                game_active = True
        elif event.type == pygame.MOUSEBUTTONDOWN:# на ЛКМ
            bird_movement = 0
            bird_movement = bird_movement-10
        elif event.type == SPAWNPIPE: #каждый раз ,при созданном нами событии SPAWNPIPE, выполняется функция create_pipe и координаты создания трубы записываются в массив pipe_list
            pipe_list.extend(create_pipe())
    #Вызов и расположение объектов
        # bg
    screen.blit(bg_surface,(0,0))
        # floor
    floor_x_pos -= 1 #т.к. у нас цикл while true :каждый раз к расположению по X прибавляется 1,что обеспечивает движением объект floor
    draw_floor()
    if floor_x_pos <= -576: #Когда щирина оставшейся можельки floor становется меньши или равна -576(конец экрана) ,она становится равна 0 и отрисовывается повтороно,см функцию выше
        floor_x_pos = 0
    if game_active == True:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement #настройка смещения хитбокса вместе с текстурой птички(ctntery ,потому что птичка падает центрально вертикально вниз(по прямой))
        screen.blit(bird_surface,bird_rect) #размещаем птичку в своем хитбоксе
        game_active = check_collision(pipe_list)
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    pygame.display.update()
    clock.tick(120) #ограничение fps

