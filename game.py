import pygame
from pygame.locals import *
import os
import random

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Corona game')

bg = pygame.image.load(os.path.join('images', 'bg3.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()


class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.4
            self.x += 0.3
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif 20 < self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)

        pygame.draw.rect(win, (255,0,0),self.hitbox, 2)


class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'corona.png')),
              pygame.image.load(os.path.join('images', 'corona.png')),
              pygame.image.load(os.path.join('images', 'corona.png')),
              pygame.image.load(os.path.join('images', 'corona.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.5

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount // 2], (64, 64)), (self.x, self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class spike(saw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


class sanitizer(object):
    san = pygame.image.load(os.path.join('images', 'sani1.png'))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        self.hitbox = (self.x, self.y + 5, self.width, self.height)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        win.blit(self.san, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1]+self.hitbox[3]:
                print("yes")

                return True
        return False


def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False

        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        # lastScore = largeFont.render('Best Score: ' + str(updateFile()), 1, (255, 255, 255))
        currentScore = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
        bonusScore = largeFont.render('Bonus: ' + str(bonus), 1, (255, 255, 255))
        # win.blit(lastScore, (W / 2 - lastScore.get_width() / 2, 150))
        win.blit(currentScore, (W / 2 - currentScore.get_width() / 2, 240))
        win.blit(bonusScore, (W / 2 - currentScore.get_width() / 2, 300))
        pygame.display.update()
    score = 0


def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    text = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
    bonusTxt = largeFont.render('Bonus: ' + str(bonus), 1, (255, 255, 255))
    runner.draw(win)

    for obstacle in obstacles:
        obstacle.draw(win)

    for sani in sanitizers:
        sani.draw(win)

    win.blit(text, (700, 10))
    win.blit(bonusTxt, (700, 30))
    pygame.display.update()


pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, 3000)
pygame.time.set_timer(USEREVENT + 3, 7000)
speed = 35

score = 0

run = True
runner = player(200, 310, 64, 64)

obstacles = []
pause = 0
fallSpeed = 0
sanitizers = []
bonus = 0
b=0
while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = (speed // 10 - 3)
    bonus = b

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True

            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.5

    for sani in sanitizers:
        if sani.collide(runner.hitbox):

            b = 5
            pygame.time.delay(50)

        else:
            b = 0

        if sani.x < -64:
            sanitizers.pop(sanitizers.index(sani))
        else:
            sani.x -= 1.5

    bgX -= 1.5
    bgX2 -= 1.5

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        if event.type == USEREVENT + 1:
            speed += 1

        if event.type == USEREVENT + 2:
            r = random.randrange(0, 2)
            if r == 0:
                obstacles.append(saw(810, 310, 50, 50))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))

        if event.type == USEREVENT + 3:
            sanitizers.append(sanitizer(810, 200, 50, 50))

    if not runner.falling:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not runner.jumping:
                runner.jumping = True

        if keys[pygame.K_DOWN]:
            if not runner.sliding:
                runner.sliding = True

    clock.tick(speed)
    redrawWindow()
