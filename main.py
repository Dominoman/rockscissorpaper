import sys

import pygame
from pygame import Surface, Color, Vector2


class Sprite:
    def __init__(self, type: int, x: int, y: int, game: 'Game') -> None:
        self.type = type
        self.pos = Vector2(x, y)
        self.game = game
        self.killed = False

    def update(self) -> None:
        distance = 100000
        other = None
        for sprite in self.game.sprites:
            if (sprite.type == self.enemy_type() or sprite.enemy_type() == self.type) and self.get_distance(
                    sprite) < distance:
                distance = self.get_distance(sprite)
                other = sprite
        if other is not None:
            if other.type == self.enemy_type():
                self.pos += (other.pos - self.pos).normalize()
            else:
                self.pos -= (other.pos - self.pos).normalize()

        if self.pos.x < 16:
            self.pos.x = 16
        elif self.pos.x > Game.WIDTH - 16:
            self.pos.x = Game.WIDTH - 16
        if self.pos.y < 16:
            self.pos.y = 16
        elif self.pos.y > Game.HEIGHT - 16:
            self.pos.y = Game.HEIGHT - 16

    def draw(self, surface: Surface) -> None:
        surface.blit(self.game.images[self.type], (self.pos.x - 16, self.pos.y - 16))

    def enemy_type(self) -> int:
        return self.type + 1 if self.type < 2 else 0

    def get_distance(self, o: 'Sprite') -> float:
        return (o.pos - self.pos).length()

    def hit(self, o: 'Sprite') -> bool:
        return self.get_distance(o) < 16


class Game:
    images: list[Surface]
    sprites: list[Sprite]
    WIDTH = 800
    HEIGHT = 600

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Rock paper scissor")
        self.surface = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.timer = pygame.time.Clock()
        self.images = []
        self.images.append(pygame.image.load("images\\rock.png").convert_alpha())
        self.images.append(pygame.image.load("images\\scissor.png").convert_alpha())
        self.images.append(pygame.image.load("images\\paper.png").convert_alpha())
        self.font = pygame.font.Font("font\\calibri.ttf", 16)
        self.sprites = []
        self.selected_type = 0
        self.last_mouse = pygame.mouse.get_pressed()
        self.count = [0, 0, 0]

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw(self.surface)
            pygame.display.flip()
            self.timer.tick(50)

    def update(self) -> None:
        button = pygame.mouse.get_pressed()
        if not button[0] and self.last_mouse[0]:
            pos = pygame.mouse.get_pos()
            self.sprites.append(Sprite(self.selected_type, pos[0], pos[1], self))
        if not button[2] and self.last_mouse[2]:
            self.selected_type = self.selected_type + 1 if self.selected_type < len(self.images) - 1 else 0
        self.last_mouse = button

        for sprite in self.sprites:
            sprite.update()
        for sprite1 in self.sprites:
            for sprite2 in self.sprites:
                if sprite1.enemy_type() == sprite2.type and sprite1.hit(sprite2):
                    sprite2.killed=True
        i=len(self.sprites)-1
        while i>0:
            if self.sprites[i].killed:
                self.sprites.pop(i)
            i-=1
        self.count = [0, 0, 0]
        for sprite in self.sprites:
            self.count[sprite.type] += 1

    def draw(self, surface: Surface) -> None:
        surface.fill(Color("White"), (0, 0, Game.WIDTH, Game.HEIGHT))
        surface.blit(self.images[self.selected_type], (0, 0))
        for sprite in self.sprites:
            sprite.draw(surface)
        surface.blit(
            self.font.render(f"Rock:{self.count[0]},Scissor:{self.count[1]},Paper:{self.count[2]}", 0, Color(0, 0, 0)),
            (40, 10))


if __name__ == "__main__":
    game = Game()
    game.run()
