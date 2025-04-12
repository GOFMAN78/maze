import pygame as pg

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image_name, width, height, speed, x, y):
        self.image = pg.transform.scale(pg.image.load(image_name), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def move(self, keys_pressed):
        if keys_pressed[pg.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[pg.K_d] and self.rect.x < w - w/10:
            self.rect.x += self.speed   
        if keys_pressed[pg.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[pg.K_s] and self.rect.y < h - w/10:
            self.rect.y += self.speed
    def put_bomb(self, keys_pressed):
        if keys_pressed[pg.K_SPACE]:
            pass
            #bomb = Bomb('bomb.png', w/10, w/10, 0, self.rect.x, self.rect.y)
            #bombs.append(bomb)

class Enemy(GameSprite):
    def move(self, keys_pressed):
        self.rect.x += self.speed
        if self.rect.x > w - w/12:
            self.speed *= -1
        elif self.rect.x < w - w/4:
            self.speed *= -1

class Bomb(GameSprite):
    def boom(self):
        pass

class Wall(pg.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.color = color
        self.image = pg.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

win = pg.display.set_mode((700, 500), pg.FULLSCREEN)
w, h = pg.display.get_window_size()

pg.display.set_caption('Лабиринт')
#fonova musica
pg.mixer.init()
pg.mixer.music.load('jungles.ogg')
pg.mixer.music.play()

#обьекты игровые

#sprite_2 = pg.transform.scale(pg.image.load('sprite2.png'), (100, 100))
#переменные
bg = pg.transform.scale(pg.image.load('background.jpg'), (w, h))
hero = Hero('hero.png', w/10, w/10, 10, 25, h - 75)
enemy = Enemy('cyborg.png', w/10, w/10, 10, w - 75, h - 150)
gold = GameSprite('treasure.png', w/10, w/10, 10, w - 75, h - 75)
wall1 = Wall(25, h - 150, 150,  50, (200,200,200))
wall2 = Wall(w - 150, 25, 50,  50, (200,200,200))
wall3 = Wall(25, h - 150, 50,  50, (200,200,200))

bombs = list()
finish = False
run = True
clock = pg.time.Clock()
win_sound = pg.mixer.Sound('money.ogg')
lose_sound = pg.mixer.Sound('kick.ogg')
#x1 = 50
#y1 = 450
#x2 = w - 150
#y2 = 450
#цикл игровой
while run:
    for e in pg.event.get():
        
        if e.type == pg.QUIT:
            run = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                win = pg.display.set_mode((700,500))
                w = 700
                h = 500
                bg = pg.transform.scale(pg.image.load('background.jpg'), (w, h))
                hero = Hero('hero.png', w/10, w/10, 10, 25, h - 75)
                enemy = Enemy('cyborg.png', w/10, w/10, 10, w - 75, h - 150)
                gold = GameSprite('treasure.png', w/10, w/10, 10, w - 75, h - 75)
    if not finish:
        keys_pressed = pg.key.get_pressed()
        

        win.blit(bg, (0,0))
        hero.move(keys_pressed)
        hero.put_bomb(keys_pressed)
        enemy.move(keys_pressed)
        enemy.reset()
        wall1.reset()
        wall2.reset()
        wall3.reset()
        gold.reset()
        for b in bombs:
            b.reset()
        hero.reset()
        if pg.sprite.collide_rect(hero, gold):
            win_sound.play()
            finish = True
            victory = True
        if pg.sprite.collide_rect(hero, wall1):
            lose_sound.play()
            finish = True
            victory = False
        if pg.sprite.collide_rect(hero, wall2):
            lose_sound.play()
            finish = True
            victory = False
        if pg.sprite.collide_rect(hero, wall3):
            finish = True
            victory = False
            lose_sound.play()
        if pg.sprite.collide_rect(hero, enemy):
            finish = True
            victory = False
    if finish:
        if victory:
            bg = pg.transform.scale(pg.image.load('victory.jpg'), (w, h))
        else:
            bg = pg.transform.scale(pg.image.load('gameover.png'), (w, h))

    pg.display.update()
    clock.tick(60)