import pygame as pg
import sys
import time
from game.RenderingManager import RenderingManager
from game.LogicManager import LogicManager

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class Snake():
    """
    Main class of the game that combines the RenderingManager and the
    LogicManager
    """
    def __init__(self,
                 screen_size,
                 grid_length,
                 with_rendering=True):
        """
        Basic constructor
        """
        self.with_rendering = with_rendering
        self.screen_size = screen_size
        self.grid_size = [grid_length, grid_length]

        self._init_game()

        self.loose = 0

    def _init_time(self, ips):
        """
        Init the time to handle human inputs
        """
        self.last_time = time.time()
        self.input_per_sec = ips

    def _init_game(self):
        """
        Init games functions
        """
        # set value to travel half the grid per second to quickly test the game
        self.loose = 0
        self._init_time(self.grid_size[0] // 2)
        if self.with_rendering:
            self.render = RenderingManager(self.screen_size,
                                           self.grid_size)
        self.logic = LogicManager(self.grid_size)
        if self.with_rendering:
            self.render.update_entities(self.logic.snake,
                                        self.logic.apples)

    def _take_input(self):
        """
        Check if the game should try to get an input
        from a human player
        """
        curr_time = time.time()
        delta_time = curr_time - self.last_time
        if delta_time > 1/self.input_per_sec:
            self.last_time = curr_time
            return True
        return False


    def _handle_keys(self, keys):
        """
        Handle human player keys
        """
        if keys[pg.K_RIGHT]:
            self._perform_move(RIGHT)
        elif keys[pg.K_LEFT]:
            self._perform_move(LEFT)
        elif keys[pg.K_UP]:
            self._perform_move(UP)
        elif keys[pg.K_DOWN]:
            self._perform_move(DOWN)


    def _perform_move(self, input):
        """
        Perform a move that can come from a human or an algorithm
        """
        if input == RIGHT:
            self.loose = self.logic.update_logic([1, 0])
        elif input == LEFT:
            self.loose = self.logic.update_logic([-1, 0])
        elif input == UP:
            self.loose = self.logic.update_logic([0, -1])
        elif input == DOWN:
            self.loose = self.logic.update_logic([0, 1])
        else:
            self.loose = 0

        if self.with_rendering:
            self.render.update_entities(
                self.logic.snake,
                self.logic.apples)
        if self.loose:
            return -1
        return self.logic.prev_reward

    def render_game(self):
        """
        Simple function to respect demeter's law in the Snake environment
        """
        self.render.render()

    def get_state(self):
        """
        Return the current state of the game for algorithm purpose
        """
        return self.logic.grid




    def start_interactive_game(self):
        """
        Start playing mode for a human with take_input routine
        """
        assert self.with_rendering, "Can't play without render"
        while True:
            if self.loose != 0:
                self._init_game()
            if self._take_input():
                self._check_events()
            if self.with_rendering:
                self.render_game()


    def _check_events(self):
        """
        Function to handle user-related events
        """
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        self._handle_keys(keys)
