import pygame as pg
import pygame.sprite as sprite
from game.EntitiesSprite import EntitiesSprite

class RenderingManager():
    """
    A class used to render the Snake game
    """
    def __init__(self, screen_size, grid_size):
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.display = pg.display

        self.sprites = sprite.Group()

        self._init_screen_and_components()

    def update_entities(self, snake, apples):
        """
        Modifies the entities and draw them
        """
        self.entities.snake = snake
        self.entities.apples = apples
        self.entities.draw_entities()

    def render(self):
        """
        Main function to render the game
        """
        self._draw_sprites()
        self._update_screen()


    def _add_sprite(self, sprite):
        """
        Add sprite to the sprites to be rendered
        """
        self.sprites.add(sprite)

    def _draw_sprites(self):
        """
        Private func to render during the rendering routine
        """
        for sprite in self.sprites:
            self.screen.blit(sprite.surf, sprite.rect)


    def _update_screen(self):
        """
        Update screen with newly drawn sprites
        """
        self.display.flip()


    def _init_screen_and_components(self):
        """
        Initialize the drawing screen according to size and fill it in black
        """
        self.screen = self.display.set_mode(size=self.screen_size)
        self.screen.fill((0, 0, 0))
        self.entities = EntitiesSprite(self.screen_size, self.grid_size)
        self._add_sprite(self.entities)
