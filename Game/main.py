import random
import sys
import math

import pygame as pyg
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

BLACK =   0,   0,   0
RED   = 255,   0,   0
GREEN =   0, 255,   0
BLUE  =   0,   0, 255
WHITE = 255, 255, 255

RAD2DEG = 180 / math.pi
DONE = False


class Player:
    def __init__ (self, posX, posY, pWidth, pHeight, color):
        self.posX = posX
        self.posY = posY
        self.pWidth = pWidth
        self.pHeight = pHeight
        self.color = color

        self.shape = Rect(self.posX, self.posY, self.pWidth, self.pHeight)
        self.bullet = Projectiles(self.shape.x, self.shape.y, 32, 32, WHITE)
        self.bullets = []

        self.speed = 1

    def Collision (self) -> None:
        if self.shape.x < 0:
            self.shape.x = 0

        if self.shape.right > WIDTH:
            self.shape.x = WIDTH - self.pWidth

        if self.shape.y < 0:
            self.shape.y = 0

        if self.shape.bottom > HEIGHT:
            self.shape.y = HEIGHT - self.pHeight

    def Shoot (self) -> None:
        for i in range(1):
            self.bullets.append(Projectiles(self.shape.x, self.shape.y, 32, 32, WHITE))

    def Update (self, dt) -> None:
        self.Collision()

        keys = pyg.key.get_pressed()

        self.shape.x += ((keys[pyg.K_d] - keys[pyg.K_a]) * self.speed) * dt
        self.shape.y += ((keys[pyg.K_s] - keys[pyg.K_w]) * self.speed) * dt

    def Render (self, screen):
        pyg.draw.rect(screen, self.color, self.shape)


class Projectiles:
    def __init__ (self, posX, posY, pWidth, pHeight, color):
        self.posX = posX
        self.posY = posY
        self.pWidth = pWidth
        self.pHeight = pHeight
        self.color = color

        self.shape = Rect(self.posX, self.posY, self.pWidth, self.pHeight)

        self.speed = 100

    # this part of the script it's just a test so it doesn't works perfectly
    def Update (self, dt) -> None:
        dir_ = pyg.math.Vector2(pyg.mouse.get_pos()) - pyg.math.Vector2(self.posX, self.posY)
        dir_ang = math.atan2(dir_.y, dir_.x)

        self.shape.x += math.cos(dir_ang) * dt
        self.shape.y += math.sin(dir_ang) * dt

    def Render (self, screen) -> None:
        pyg.draw.rect(screen, self.color, self.shape)


class Enemy:
    def __init__ (self, posX, posY, pWidth, pHeight, color):
        self.posX = posX
        self.posY = posY
        self.pWidth = pWidth
        self.pHeight = pHeight
        self.color = color

        self.shape = Rect(self.posX, self.posY, self.pWidth, self.pHeight)

        self.speed = .3

        self.dirX = 1
        self.dirY = 1

    def Update (self, dt) -> None:
        if self.shape.left < 0:
            self.shape.x += self.speed * dt

            self.dirX = 1
        elif self.shape.right > WIDTH:
            self.shape.x -= self.speed * dt

            self.dirX = -1
        else:
            if self.dirX == 1:
                self.shape.x += self.speed * dt
            elif self.dirX == -1:
                self.shape.x -= self.speed * dt

        if self.shape.top < 0:
            self.shape.y += self.speed * dt

            self.dirY = 1
        elif self.shape.bottom > HEIGHT:
            self.shape.y -= self.speed * dt

            self.dirY = -1
        else:
            if self.dirY == 1:
                self.shape.y += self.speed * dt
            elif self.dirY == -1:
                self.shape.y -= self.speed * dt

    def Render (self, screen):
        pyg.draw.rect(screen, self.color, self.shape)


class Game:
    def __init__ (self):
        pyg.init()

        self.clock = pyg.time.Clock()
        self.fps = 60

        self.player = Player(WIDTH / 2, HEIGHT / 2, 32, 32, BLUE)
        self.enemies = []
        self.enemiesAmount = 10

        for i in range(self.enemiesAmount):
            self.enemies.append(Enemy(random.randrange(40, WIDTH - 40), random.randrange(40, HEIGHT - 40), 32, 32, RED))

        self.screenSize = WIDTH, HEIGHT
        self.screen = pyg.display.set_mode(self.screenSize)

    def CollisionOuter (self) -> None:
        for i in range(len(self.enemies)):
            if self.enemies[i].shape.colliderect(self.player.shape):
                global DONE

                DONE = True

        if len(self.enemies) > 0 and len(self.player.bullets) > 0:
            for i in range(len(self.enemies)):
                for k in range(len(self.player.bullets)):
                    if self.enemies[i - 1].shape.colliderect(self.player.bullets[k - 1].shape):
                        del self.enemies[i - 1]
                        del self.player.bullets[k - 1]

                        return

        if len(self.player.bullets) >= 1:
            for i in range(len(self.player.bullets)):
                if self.player.bullets[i - 1].shape.right > WIDTH or self.player.bullets[i - 1].shape.x < 0 or\
                        self.player.bullets[i - 1].shape.bottom > HEIGHT or self.player.bullets[i - 1].shape.y < 0:
                    del self.player.bullets[i - 1]

                print(len(self.player.bullets))

    def Update (self) -> None:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                sys.exit()

            if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                self.player.Shoot()

        delta_time = self.clock.tick(self.fps)

        self.CollisionOuter()

        self.player.Update(delta_time)

        for i in range(len(self.enemies)):
            self.enemies[i].Update(delta_time)

        for i in range(len(self.player.bullets)):
            self.player.bullets[i].Update(delta_time)

    def Render (self) -> None:
        self.screen.fill(BLACK)

        self.player.Render(self.screen)

        for i in range(len(self.enemies)):
            self.enemies[i].Render(self.screen)

        for i in range(len(self.player.bullets)):
            self.player.bullets[i].Render(self.screen)

        pyg.display.flip()


def main ():
    game = Game()

    while not DONE:
        game.Update()
        game.Render()


if __name__ == "__main__":
    main()
