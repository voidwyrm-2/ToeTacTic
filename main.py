import pygame
from random import randint



def limit(input, max):
    if input > max: return max
    return input

def log(data):
    with open('LOG.txt', 'at') as lf: lf.write(str(data) + '\n')


# initialize game
pygame.init()

# creating a screen
windratio = 600, 600
screen = pygame.display.set_mode(windratio)  # passing width and height
screen.fill("black")
pygame.display.flip()

# title and icon
pygame.display.set_caption("ToeTacTic")
#icon = pygame.image.load('Waypointer-icon(unshaded).png')
#if shadeicon: icon = pygame.image.load('Waypointer-icon(shaded).png')
#pygame.display.set_icon(icon)

pygame.font.init()
credfont = pygame.font.Font('freesansbold.ttf', 16)
mainfont = pygame.font.Font('freesansbold.ttf', 32)
tictacfont = pygame.font.Font('freesansbold.ttf', 70)

DEBUG = [False, False, False, False, False, False] #showDebugNumbers, fillAll, disableAI, cantWin, showWinLists, dontBlackOut

shownumbers = True

multiplayer = False

stopcontrol = False

playerturn = True
player = 'o'
enemy = 'x'

playerwon = False

px = [0,0,0]
py = [0,0,0]
pxy = [0,0]

ex = [0,0,0]
ey = [0,0,0]
exy = [0,0]

cansaylost = True
cansaywon = True
cansaytied = True

livetictacs = [] #looks like (0, 'o', True) #(POS, 'o'/'x', ISPLAYER)

tictacpos = [
    (windratio[0] // 4, (windratio[1] // 6) + 30),
    ((windratio[0] // 2) - 25, (windratio[1] // 6) + 30),
    (windratio[0] - 190, (windratio[1] // 6) + 30),

    (windratio[0] // 4, (windratio[1] // 2) - 40),
    ((windratio[0] // 2) - 25, (windratio[1] // 2) - 40),
    (windratio[0] - 190, (windratio[1] // 2) - 40),

    (windratio[0] // 4, (windratio[1] // 2) + 90),
    ((windratio[0] // 2) - 25, (windratio[1] // 2) + 90),
    (windratio[0] - 190, (windratio[1] // 2) + 90)
]

if DEBUG[1]:
    for itic in range(9): livetictacs.append((itic, '0', True))

def addp1tictac(index: int, beingplaced: str):
    global livetictacs
    global playerturn
    global DEBUG
    if len(livetictacs) >= 9: return
    if len(livetictacs) <= 0:
        livetictacs.append((index, beingplaced, playerturn))
        if not DEBUG[2]: playerturn = False
    else:
        canplace = True
        for tic in livetictacs:
            if tic[0] == index: canplace = False; break
        if canplace:
            livetictacs.append((index, beingplaced, playerturn))
            if not DEBUG[2]: playerturn = False

def addp2tictac(index: int, beingplaced: str):
    global livetictacs
    global playerturn
    global DEBUG
    if len(livetictacs) >= 9: return
    if len(livetictacs) <= 0:
        livetictacs.append((index, beingplaced, playerturn))
        if not DEBUG[2]: playerturn = True
    else:
        canplace = True
        for tic in livetictacs:
            if tic[0] == index: canplace = False; break
        if canplace:
            livetictacs.append((index, beingplaced, playerturn))
            if not DEBUG[2]: playerturn = True


def aiaddtictac():
    global livetictacs
    global playerturn
    global enemy
    if len(livetictacs) >= 9: return
    aiindex = randint(0, 8)
    if len(livetictacs) <= 0: livetictacs.append((aiindex, enemy, playerturn)); playerturn = True
    else:
        canplace = True
        while True:
            for tic in livetictacs:
                if tic[0] == aiindex: canplace = False; break
            if canplace: livetictacs.append((aiindex, enemy, playerturn)); print(f'placed an {enemy} at {aiindex}'); playerturn = True; break
            else: print(f'"{enemy}" already on {aiindex}! ai rerolling...'); canplace = True; aiindex = randint(0, 8)

def drawgrid():
    global windratio
    stepX = 200
    stepY = 200
    for li1 in range(2):
        pygame.draw.line(screen, (255, 255, 255), (100, stepX), (windratio[0] - 100, stepX), 5); stepX += 200
    #pygame.draw.line(screen, (255, 0, 0), (0, 200), (windratio[0], 200), 5)
    #pygame.draw.line(screen, (255, 0, 0), (0, 400), (windratio[0], 400), 5)

    for li2 in range(2):
        pygame.draw.line(screen, (255, 255, 255), (stepY, 100), (stepY, windratio[1] - 100), 5); stepY += 200
    #pygame.draw.line(screen, (0, 0, 255), (200, 0), (200, windratio[1]), 5)
    #pygame.draw.line(screen, (0, 0, 255), (400, 0), (400, windratio[1]), 5)

def drawturn(x, y):
    global playerturn
    global multiplayer
    turn = mainfont.render('currently Player turn', True, (255, 255, 255))
    if multiplayer: turn = mainfont.render('currently Player 1 turn', True, (255, 255, 255))
    if not playerturn and not multiplayer: turn = mainfont.render('currently AI turn', True, (255, 255, 255))
    if not playerturn and multiplayer: turn = mainfont.render('currently Player 2 turn', True, (255, 255, 255))
    screen.blit(turn, (x, y))

def drawtictacs():
    for tac in livetictacs:
        if tac[2] == True:
            otac = tictacfont.render(tac[1], True, (0, 0, 255))
            screen.blit(otac, tictacpos[tac[0]])
        elif tac[2] == False:
            xtac = tictacfont.render(tac[1], True, (255, 0, 0))
            screen.blit(xtac, tictacpos[tac[0]])

def drawnumbers():
    tti = 0
    for tac in tictacpos:
        ind = mainfont.render(str(tti), True, (200, 200, 200))
        screen.blit(ind, (tac[0] + 15, tac[1] + 35))
        tti += 1

def drawtruenumbers():
    tti = 1
    for tac in tictacpos:
        ind = mainfont.render(str(tti), True, (200, 200, 200))
        screen.blit(ind, (tac[0] + 15, tac[1] + 35))
        tti += 1

def drawwinlists(x, y):
    global px
    global py
    global pxy
    global ex
    global ey
    global exy
    one = credfont.render(f'px:{px}', True, (255, 255, 255))
    screen.blit(one, (x, y))
    two = credfont.render(f'py:{py}', True, (255, 255, 255))
    screen.blit(two, (x, y + 19))
    three = credfont.render(f'pxy:{pxy}', True, (255, 255, 255))
    screen.blit(three, (x, y + (19 * 2)))

    four = credfont.render(f'ex:{ex}', True, (255, 255, 255))
    screen.blit(four, (x, y + (19 * 3)))
    five = credfont.render(f'ey:{ey}', True, (255, 255, 255))
    screen.blit(five, (x, y + (19 * 4)))
    six = credfont.render(f'exy:{exy}', True, (255, 255, 255))
    screen.blit(six, (x, y + 19 * 5))


def credits(x, y):
    creds = credfont.render('A game by Nuclear Pasta', True, (255, 255, 255))
    #screen.blit(creds, (x + 60, y + 30))
    screen.blit(creds, (0, 0))


def lose(x, y):
    global stopcontrol
    global cansaylost
    global multiplayer
    stopcontrol = True
    loss = mainfont.render('You lost! womp womp', True, (255, 255, 255))
    if multiplayer: loss = mainfont.render('Player 2 won! yaaaay!', True, (255, 255, 255))
    screen.blit(loss, (x, y))
    credits(x, y)
    if cansaylost: print('Player 1 lost!'); cansaylost = False

def win(x, y):
    global stopcontrol
    global cansaywon
    global multiplayer
    stopcontrol = True
    won = mainfont.render('You won! wooooo!', True, (255, 255, 255))
    if multiplayer: won = mainfont.render('Player 1 won! wooooo!', True, (255, 255, 255))
    screen.blit(won, (x + 10, y))
    credits(x, y)
    if cansaywon: print('Player 1 won!'); cansaywon = False

def tie(x, y):
    global stopcontrol
    global cansaytied
    global multiplayer
    stopcontrol = True
    tied = mainfont.render('Twas but a tie', True, (255, 255, 255))
    screen.blit(tied, (x + 10, y))
    credits(x, y)
    if cansaytied and not multiplayer: print('Player and AI tied!'); cansaytied = False
    elif cansaytied and multiplayer: print('Player 1 and Player 2 tied!'); cansaytied = False

def checkforwin():
    global livetictacs
    global playerturn
    global stopcontrol
    global playerwon
    global multiplayer

    global px
    global py
    global pxy
    global ex
    global ey
    global exy

    px = [0,0,0]
    py = [0,0,0]
    pxy = [0,0]

    ex = [0,0,0]
    ey = [0,0,0]
    exy = [0,0]


    for toe in livetictacs:
        if toe[0] == 0 and toe[2] == True: px[0] += 1
        elif toe[0] == 1 and toe[2] == True: px[0] += 1
        elif toe[0] == 2 and toe[2] == True: px[0] += 1
        elif toe[0] == 3 and toe[2] == True: px[1] += 1
        elif toe[0] == 4 and toe[2] == True: px[1] += 1
        elif toe[0] == 5 and toe[2] == True: px[1] += 1
        elif toe[0] == 6 and toe[2] == True: px[2] += 1
        elif toe[0] == 7 and toe[2] == True: px[2] += 1
        elif toe[0] == 8 and toe[2] == True: px[2] += 1

        if toe[0] == 0 and toe[2] == True: py[0] += 1
        elif toe[0] == 3 and toe[2] == True: py[0] += 1
        elif toe[0] == 6 and toe[2] == True: py[0] += 1
        elif toe[0] == 1 and toe[2] == True: py[1] += 1
        elif toe[0] == 4 and toe[2] == True: py[1] += 1
        elif toe[0] == 7 and toe[2] == True: py[1] += 1
        elif toe[0] == 2 and toe[2] == True: py[2] += 1
        elif toe[0] == 5 and toe[2] == True: py[2] += 1
        elif toe[0] == 8 and toe[2] == True: py[2] += 1

        if toe[0] == 0 and toe[2] == True: pxy[0] += 1
        elif toe[0] == 4 and toe[2] == True: pxy[0] += 1
        elif toe[0] == 8 and toe[2] == True: pxy[0] += 1
        elif toe[0] == 2 and toe[2] == True: pxy[1] += 1
        elif toe[0] == 4 and toe[2] == True: pxy[1] += 1
        elif toe[0] == 6 and toe[2] == True: pxy[1] += 1
    
    for toe in livetictacs:
        if toe[0] == 0 and toe[2] == False: ex[0] += 1
        elif toe[0] == 1 and toe[2] == False: ex[0] += 1
        elif toe[0] == 2 and toe[2] == False: ex[0] += 1
        elif toe[0] == 3 and toe[2] == False: ex[1] += 1
        elif toe[0] == 4 and toe[2] == False: ex[1] += 1
        elif toe[0] == 5 and toe[2] == False: ex[1] += 1
        elif toe[0] == 6 and toe[2] == False: ex[2] += 1
        elif toe[0] == 7 and toe[2] == False: ex[2] += 1
        elif toe[0] == 8 and toe[2] == False: ex[2] += 1

        if toe[0] == 0 and toe[2] == False: ey[0] += 1
        elif toe[0] == 3 and toe[2] == False: ey[0] += 1
        elif toe[0] == 6 and toe[2] == False: ey[0] += 1
        elif toe[0] == 1 and toe[2] == False: ey[1] += 1
        elif toe[0] == 4 and toe[2] == False: ey[1] += 1
        elif toe[0] == 7 and toe[2] == False: ey[1] += 1
        elif toe[0] == 2 and toe[2] == False: ey[2] += 1
        elif toe[0] == 5 and toe[2] == False: ey[2] += 1
        elif toe[0] == 8 and toe[2] == False: ey[2] += 1

        if toe[0] == 0 and toe[2] == False: exy[0] += 1
        elif toe[0] == 4 and toe[2] == False: exy[0] += 1
        elif toe[0] == 8 and toe[2] == False: exy[0] += 1
        elif toe[0] == 2 and toe[2] == False: exy[1] += 1
        elif toe[0] == 4 and toe[2] == False: exy[1] += 1
        elif toe[0] == 6 and toe[2] == False: exy[1] += 1

    endingsX = 90
    endingsY = 250
    for pxc in px:
        if pxc == 3: stopcontrol = True; win(endingsX, endingsY); playerwon = True; break; return
    for pyc in py:
        if pyc == 3: stopcontrol = True; win(endingsX, endingsY); playerwon = True; break; return
    for pxyc in pxy:
        if pxyc == 3: stopcontrol = True; win(endingsX, endingsY); playerwon = True; break; return
    
    if playerwon: return

    for exc in ex:
        if exc == 3: lose(endingsX, endingsY); break; return
    for eyc in ey:
        if eyc == 3: lose(endingsX, endingsY); break; return
    for exyc in exy:
        if exyc == 3: lose(endingsX, endingsY); break; return

    #if not playerturn and not multiplayer: tie(endingsX, endingsY); return
    #else:
        axiscounter = 0
        for i in px: axiscounter += i
        for i in py: axiscounter += i
        for i in pxy: axiscounter += i

        for i in ex: axiscounter += i
        for i in ey: axiscounter += i
        for i in exy: axiscounter += i

        #print(f'counted it up, got {axiscounter}!')
        if axiscounter == 23: tie(endingsX, endingsY); return



running = True
while running:
    screen.fill((0, 0, 0))  # background
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: running = False; break
            if stopcontrol: break

            #if event.key == pygame.K_x and placing == 'o': placing = 'x'

            #if event.key == pygame.K_x and placing == 'x': placing = 'o'
            if playerturn:
                if event.key == pygame.K_1 and playerturn: addp1tictac(0, player)

                if event.key == pygame.K_2 and playerturn: addp1tictac(1, player)

                if event.key == pygame.K_3 and playerturn: addp1tictac(2, player)

                if event.key == pygame.K_4 and playerturn: addp1tictac(3, player)

                if event.key == pygame.K_5 and playerturn: addp1tictac(4, player)

                if event.key == pygame.K_6 and playerturn: addp1tictac(5, player)

                if event.key == pygame.K_7 and playerturn: addp1tictac(6, player)

                if event.key == pygame.K_8 and playerturn: addp1tictac(7, player)

                if event.key == pygame.K_9 and playerturn: addp1tictac(8, player)

            if not playerturn and multiplayer:
                if event.key == pygame.K_1 and not playerturn: addp2tictac(0, enemy)
            
                if event.key == pygame.K_2 and not playerturn: addp2tictac(1, enemy)

                if event.key == pygame.K_3 and not playerturn: addp2tictac(2, enemy)

                if event.key == pygame.K_4 and not playerturn: addp2tictac(3, enemy)

                if event.key == pygame.K_5 and not playerturn: addp2tictac(4, enemy)

                if event.key == pygame.K_6 and not playerturn: addp2tictac(5, enemy)

                if event.key == pygame.K_7 and not playerturn: addp2tictac(6, enemy)

                if event.key == pygame.K_8 and not playerturn: addp2tictac(7, enemy)

                if event.key == pygame.K_9 and not playerturn: addp2tictac(8, enemy)


    if not playerturn and not multiplayer and not stopcontrol and not DEBUG[2]: aiaddtictac()

    drawturn(0, 0)

    drawgrid()
    if shownumbers: drawtruenumbers()
    drawtictacs()
    if DEBUG[0]: drawnumbers()
    if DEBUG[4]: drawwinlists(0, 35)

    if stopcontrol and not DEBUG[5]: screen.fill((0, 0, 0))

    if not DEBUG[3]: checkforwin()

    pygame.display.update()