import pygame , sys

pygame.init()
#Screen - окно ,его размещение и размер (576-w,1024-h)
screen = pygame.display.set_mode((576,1024))
while True:
    #Отслеживание событий со стороны пользователя
    for event in pygame.event.get():
        #если тип события = QUIT(пользователь нажал на крестик вверху окна),то происходит закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit() #При закрытии окна пользвователем,процесс работы программы не прекращается,поэтому пользуемся библиотекой sys для прекращенеия этого самого процесса
            
    pygame.display.update()

