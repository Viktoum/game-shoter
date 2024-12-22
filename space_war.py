from pygame import *
from random import randint
font.init()

window_game = display.set_mode((1000, 800))
fon = transform.scale(image.load("Space-Free-PNG-Image.png"), (1000, 800))
font = font.SysFont("Arial", 70)
win = font.render("YOU WIN", True, (243, 235, 120))
lose = font.render("YOU LOSER", True, (243, 118, 120))
lost = 0
kills = 0
finish = False

class Game_Sprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_height, player_widght):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_widght, player_height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window_game.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(Game_Sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        
class Player(Game_Sprite):
    def update(self):
        keyboards = key.get_pressed()
        if keyboards[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keyboards[K_RIGHT] and self.rect.x < 935:
            self.rect.x += self.speed
        if keyboards[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keyboards[K_d] and self.rect.x < 935:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet_at_space_ship.png",self.rect.centerx - 13/2, self.rect.top, 10, 32, 13)
        bullets.add(bullet)

class Enemy(Game_Sprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.rect.y = 0
            self.rect.x = randint(0, 940)
            lost += 1

cloke = time.Clock()
FPS = 60
game = True

space_ship_player = Player("spacecraft.png", 500, 670, 10, 130, 65)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(6):
    space_enemy = Enemy("space_enemy.png", randint(0, 940), 60, randint(1, 4), 60, 60)
    monsters.add(space_enemy)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                space_ship_player.fire()
    if finish != True:
        window_game.blit(fon, (0,0))
        sprits_list_kill = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprits_list_kill:
            kills += 1
            space_enemy = Enemy("space_enemy.png", randint(0, 940), 60, randint(1, 4), 60, 60)
            monsters.add(space_enemy)
        sprite_list_ship_died = sprite.spritecollide(space_ship_player, monsters, False)
        if len(sprite_list_ship_died) >= 1:
            finish = True
        if lost >= 30:
            finish = True
        if kills >= 30:
            finish = True
        bullets.draw(window_game)
        bullets.update()
        monsters.draw(window_game)
        monsters.update()
        text_lost = font.render("MISS:" + str(lost), True, (255, 255, 255))
        text_kills = font.render("Kills:" + str(kills), True, (255, 255, 255))
        window_game.blit(text_kills, (10, 55))
        window_game.blit(text_lost, (10, 0))
        space_ship_player.reset()
        space_ship_player.update()
    display.update()
    cloke.tick(FPS)