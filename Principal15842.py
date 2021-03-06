import pygame, sys
from pygame.locals import *
from Juego import *

def draw_text(text, size, color, surface, x, y):
    font = pygame.font.Font(pygame.font.match_font('comicsansms'), size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

def selectBotton(pos, ac):
    if ac=="subir" and pos <= 2:
        pos+=1
        return pos
    elif ac=="bajar" and pos <= 1:
        pos-=1
        return pos

def pintarBoton(estado, boton):
    if estado:
        pygame.draw.rect(screen, (255, 0, 0), boton)
    else: #Seleccionado
        pygame.draw.rect(screen, (0, 255, 0), boton)

def main_menu():
    click = False
    selectB = 1
    fondo = pygame.image.load("textures/grad10.png")

    # INSIDE OF THE GAME LOOP
    b1= False
    b2 = False

    button_1 = pygame.Rect(150, 250, 200, 50)
    button_2 = pygame.Rect(150, 350, 200, 50)

    while True:

        screen.blit(fondo, (0, 0))
        draw_text('main menu', 40, (255, 0, 255), screen, 150, 50)

        mx, my = pygame.mouse.get_pos()

        pintarBoton(b1, button_1)
        pintarBoton(b2, button_2)

        draw_text('Play', 20, (0, 0, 0), screen, 250, 250)
        draw_text('Exit', 20, (0, 0, 0), screen, 250, 350)

        if button_1.collidepoint((mx, my)):
            b1=True
            b2 = False
            pintarBoton(b1, button_1)
            draw_text('Play', 20, (255, 255, 255), screen, 250, 250)
            if click:
                play()
                screen.fill((0, 0, 0))
        if button_2.collidepoint((mx, my)): #Boton Exit
            b1 = False
            b2 = True
            pintarBoton(b2, button_2)
            draw_text('Exit', 20, (255, 255, 255), screen, 250, 350)
            if click:
                pygame.quit()
                sys.exit()
                screen.fill((0, 0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    b1 = True
                    b2 = False
                    pintarBoton(b1, button_1)
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    b1 = False
                    b2 = True
                    pintarBoton(b2, button_2)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if b1:
                        play()
                    elif b2:
                        pygame.quit()
                        sys.exit()
            #K_RIGHT
            #K_LEFT


        pygame.display.update()
        mainClock.tick(60)



def play():
    r.load_map('levels/map.txt')

    isRunning = True
    while isRunning:

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_LEFT:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_RIGHT:
                    r.player['angle'] += 5

                i = int(newX / r.blocksize)
                j = int(newY / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY

        screen.fill(pygame.Color("gray"))  # Fondo

        # Techo
        screen.fill(pygame.Color("saddlebrown"), (int(r.width / 2), 0, int(r.width / 2), int(r.height / 2)))

        # Piso
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2), int(r.height / 2)))

        r.render()

        # FPS
        screen.fill(pygame.Color("black"), (0, 0, 30, 30))
        screen.blit(updateFPS(), (0, 0))
        clock.tick(30)

        pygame.display.update()


mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)


r = Raycaster(screen)
main_menu()
pygame.quit()