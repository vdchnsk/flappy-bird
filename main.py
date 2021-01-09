import pygame , sys

def draw_floor(): #Повторная отрисовка пола
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576 ,900))

pygame.init()
#Screen settings
screen = pygame.display.set_mode((576,1024))#Screen - окно ,его размещение и размер (576-w,1024-h)
clock = pygame.time.Clock()#счетчик каждров или типа того

#Ojects & their settings
gravity = 0.25
bird_movement = 0

bg_surface = pygame.image.load("assets/background-day.png").convert() #bg ;convert() конвертирует изображение из src в формат,который болле удобен pygame (необязательно)
bg_surface = pygame.transform.scale2x(bg_surface) #Увеличиваем разрещение изображения (bg) вдвое

floor_surface = pygame.image.load("assets/base.png").convert() #floor;
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0; #Начальная координата floor(нужно для анимации движения пола)

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512)) #хитбокс птички

#Game working
while True:
    #Отслеживание событий со стороны пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #если тип события = QUIT(пользователь нажал на крестик вверху окна),то происходит закрытие окна
            pygame.quit() 
            sys.exit() #При закрытии окна пользвователем,процесс работы программы не прекращается,поэтому пользуемся библиотекой sys для прекращенеия этого самого процесса
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = bird_movement-12

    #Вызов и расположение объектов
    screen.blit(bg_surface,(0,0))

    bird_movement += gravity
    bird_rect.centery += bird_movement #настройка смещения хитбокса вместе с текстурой птички(ctntery ,потому что птичка падает центрально вертикально вниз(по прямой))

    screen.blit(bird_surface,bird_rect) #размещаем птичку в своем хитбоксе
    floor_x_pos -= 1 #т.к. у нас цикл while true :каждый раз к расположению по X прибавляется 1,что обеспечивает движением объект floor
    draw_floor()
    if floor_x_pos <= -576: #Когда щирина оставшейся можельки floor становется меньши или равна -576(конец экрана) ,она становится равна 0 и отрисовывается повтороно,см функцию выше
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(60) #ограничение fps

