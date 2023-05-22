import pygame as pg
import pygame.sprite as sprite
import pygame.image as image
import pygame.transform as transform

class EntitiesSprite(sprite.Sprite):
    def __init__(self, screen_size, grid_size):
        """
        Basic constructor
        """
        super(EntitiesSprite, self).__init__()
        self.grid_size = grid_size
        self.screen_size = screen_size
        self.surf = pg.Surface((screen_size[0],
                                screen_size[1]))
        self.rect = [0, 0]

        self.snake = []
        self.apples = []

    def _get_body_img(self, index):
        """
        Handmade function to get the right texture
        NB: Could be easily improved with 4-bits autotiling algorithm
        """
        if index == 0:
            part = "head"
        elif index == len(self.snake) - 1:
            part = "tail"
        else:
            part = "body"

        if part == "body":
            delta_x = self.snake[index+1][0] - self.snake[index-1][0]
            delta_y = self.snake[index+1][1] - self.snake[index-1][1]
            if abs(delta_x) == 2:
                direction = "horizontal"
            elif abs(delta_y) == 2:
                direction = "vertical"
            elif delta_x == 1 and delta_y == 1:
                if self.snake[index][0] == self.snake[index+1][0]:
                    direction = "bottomleft"
                else:
                    direction = "topright"
            elif delta_x == -1 and delta_y == 1:
                if self.snake[index][0] == self.snake[index+1][0]:
                    direction = "bottomright"
                else:
                    direction = "topleft"
            elif delta_x == -1 and delta_y == -1:
                if self.snake[index][0] == self.snake[index+1][0]:
                    direction = "topright"
                else:
                    direction = "bottomleft"
            else:
                if self.snake[index][0] == self.snake[index+1][0]:
                    direction = "topleft"
                else:
                    direction = "bottomright"
        elif part == "tail":
            delta_x = self.snake[index-1][0] - self.snake[index][0]
            delta_y = self.snake[index-1][1] - self.snake[index][1]
            if delta_x == 1:
                direction = "left"
            elif delta_x == -1:
                direction = "right"
            elif delta_y == 1:
                direction = "up"
            else:
                direction = "down"
        else:
            if len(self.snake) == 1:
                return "art/head_begin.png"
            delta_x = self.snake[index+1][0] - self.snake[index][0]
            delta_y = self.snake[index+1][1] - self.snake[index][1]
            if delta_x == 1:
                direction = "left"
            elif delta_x == -1:
                direction = "right"
            elif delta_y == 1:
                direction = "up"
            else:
                direction = "down"
        return f"art/{part}_{direction}.png"






    def _add_snake(self):
        """
        Draw the snake in snake prop
        """
        x_tile = 0.8 * self.screen_size[0] / self.grid_size[0]
        y_tile = 0.8 * self.screen_size[1] / self.grid_size[1]
        for index, body_pos in enumerate(self.snake):
            img = image.load(self._get_body_img(index))
            part_surf = img.convert()
            part_surf = transform.scale(part_surf, (x_tile, y_tile))
            part_surf.set_colorkey((255, 255, 255),
                                   pg.RLEACCEL)
            self.surf.blit(part_surf, [0.1 * self.screen_size[0] + body_pos[0] * x_tile,
                                       0.1 * self.screen_size[1] + body_pos[1] * y_tile])

    def _add_apples(self):
        """
        Draw the apples in apples prop
        """
        x_tile = 0.8 * self.screen_size[0] / self.grid_size[0]
        y_tile = 0.8 * self.screen_size[1] / self.grid_size[1]
        img = image.load(f"art/apple.png")
        for apple_pos in self.apples:
            part_surf = img.convert()
            part_surf = transform.scale(part_surf, (x_tile, y_tile))
            part_surf.set_colorkey((255, 255, 255),
                                   pg.RLEACCEL)
            self.surf.blit(part_surf, [0.1 * self.screen_size[0] + apple_pos[0] * x_tile,
                                       0.1 * self.screen_size[1] + apple_pos[1] * y_tile])

    def _add_borders(self):
        """
        Draw border limits
        """
        surf_right = pg.Surface((self.screen_size[0]/20,
                                 self.screen_size[1]*0.9))
        surf_right.fill((30, 100, 40))
        self.surf.blit(surf_right,
                       [0.05 * self.screen_size[0],
                        0.05 * self.screen_size[1]])

        surf_left = pg.Surface((self.screen_size[0]/20,
                                 self.screen_size[1]*0.9))
        surf_left.fill((30, 100, 40))
        self.surf.blit(surf_left,
                       [0.90 * self.screen_size[0],
                        0.05 * self.screen_size[1]])

        surf_top = pg.Surface((self.screen_size[0]*0.9,
                                 self.screen_size[1]/20))
        surf_top.fill((30, 100, 40))
        self.surf.blit(surf_top,
                       [0.05 * self.screen_size[0],
                        0.05 * self.screen_size[1]])

        surf_bot = pg.Surface((self.screen_size[0]*0.9,
                                 self.screen_size[1]/20))
        surf_bot.fill((30, 100, 40))
        self.surf.blit(surf_bot,
                       [0.05 * self.screen_size[0],
                        0.90 * self.screen_size[1]])

    def _fill_terrain(self):
        """
        Fill the terrain with green squares that are slightly differents
        """
        x_tile = 0.8 * self.screen_size[0] / self.grid_size[0]
        y_tile = 0.8 * self.screen_size[1] / self.grid_size[1]
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                color_surf = pg.Surface((x_tile, y_tile))
                if (i+j)%2:
                    color_surf.fill((170, 210, 70))
                else:
                    color_surf.fill((160, 210, 60))
                pos = [0.1 * self.screen_size[0] + i*x_tile,
                       0.1 * self.screen_size[1] + j*y_tile]
                self.surf.blit(color_surf, pos)


    def draw_entities(self):
        """
        Draw every entities
        """
        self.surf.fill((0, 0, 0))
        self._fill_terrain()
        self._add_snake()
        self._add_apples()
        self._add_borders()
