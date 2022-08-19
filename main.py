import pygame, time, random
from pygame import mixer
from settings import*
from pygame.locals import *
pygame.init()
pygame.font.init()
mixer.init()

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]
        self.vel = 0
        self.jumping = False

    def update(self):
        cooldown = 15
        self.counter +=1
        keys = pygame.key.get_pressed()

        #gravity
        if flying:
            self.vel += 0.6
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < bg.get_height():
                self.rect.y += self.vel

        #jumping
        if not game_over:
            if keys[pygame.K_SPACE] and self.jumping == False:
                self.jumping = True
                self.vel = -10
            if not keys[pygame.K_SPACE]:
                self.jumping = False

            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                        self.index = 0
            self.image = self.images[self.index]

            #rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        elif game_over:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            if self.rect.bottom < bg.get_height():
                self.rect.y += 26

class Pipes(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.pos = pos
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        self.scroll = 4

        if self.pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [self.x,self.y - pipe_gap // 2]
        elif self.pos == -1:
            self.rect.topleft = [self.x,self.y + pipe_gap // 2]

    def update(self):
        if not game_over:
            self.rect.x -= self.scroll
            if self.rect.right <= 0:
                self.kill()

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 50
    flappy.rect.y = bg.get_height() // 2
    score = 0
    return score

#score
score = 0
pass_pipe = False

#assignments
running = True
pipe_gap = 150
pipe_frequency = 1800 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
#sprite group assignments
bird_group = pygame.sprite.Group()
flappy = Bird(50,bg.get_height() // 2)
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()
#load font
font = pygame.font.SysFont("arial", 40)
font1 = pygame.font.SysFont("bauhaus 93", 60)
text = font.render("You Lost!", False, "yellow")
text2 = font.render("Press to play again", False, "yellow")

flying = False
game_over = False
game_start = False

def draw_score(win,text,y):
    text1 = font1.render(text, True, "green")
    win.blit(text1, (screen_width // 2 - text1.get_width() // 2 - 10 , y))

def draw(win):
    global ground_scroll,scroll_speed

    #ground shifting
    if game_over is False:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 44:
            ground_scroll = 0
    #background
    win.blit(bg, (0,0))
    #pipe
    pipe_group.draw(win)
    pipe_group.update()
    win.blit(ground, (ground_scroll,bg.get_height()))
    #assign bird
    bird_group.draw(win)
    bird_group.update()
    #font
    if game_over:
        win.blit(text, (250,250))
        win.blit(text2, (168, 360))
        draw_score(win, f"Your score: {str(score)}",140)
    if not game_over:
        draw_score(win, str(score),50)
    #update screen
    pygame.display.update()
    clock.tick(FPS)

while running:
    draw(WIN)
    keys = pygame.key.get_pressed()

    #pass pipes
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    if flappy.rect.bottom >= bg.get_height():
        game_over = True
        flying = False
    if keys[pygame.K_SPACE] and game_over is False:
        flying = True
        game_start = True
    if keys[pygame.K_SPACE] and game_over:
        score = reset_game()
        game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency and game_start:
        random_height = random.randint(-150, 150)
        bottom_pipe = Pipes(screen_width, screen_height // 2 + random_height, -1)
        top_pipe = Pipes(screen_width, screen_height  // 2 + random_height, 1)
        pipe_group.add(bottom_pipe, top_pipe)
        last_pipe = time_now

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <= 0 or flappy.rect.bottom >= bg.get_height():
        game_over = True




pygame.quit()