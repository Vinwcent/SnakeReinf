import numpy as np
import gymnasium as gym

from gymnasium import spaces
from game.Snake import Snake

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class SnakeEnv(gym.Env):

    def __init__(self, grid_length, with_rendering):
        self.grid_length = grid_length
        self.grid_size = [grid_length, grid_length]
        self.observation_space = spaces.Box(low=0,
                                            high=1,
                                            shape=self.grid_size,
                                            dtype=np.int32)

        self.action_space = spaces.Box(low=0,
                                       high=3,
                                       dtype=np.int32)
        self.with_rendering = with_rendering

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = Snake((800, 800), self.grid_length, with_rendering=self.with_rendering)

        state = self.game.get_state()

        if self.with_rendering:
            self.game.render_game()

        return state, {}

    def step(self, action):
        reward = self.game._perform_move(action)
        next_state = self.game.get_state()

        done = self.game.loose != 0
        if done and self.game.loose == 2:
            reward = 10
        if self.with_rendering:
            self.game.render_game()

        return next_state, reward, done, {}

    def get_valid_actions(self, state):
        movements = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

        grid = [list(s) for s in state]

        character_pos = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == 2]
        if not character_pos:
            raise ValueError("No character in the grid.")
        character_pos = character_pos[0]

        valid_actions = []
        for action, (dx, dy) in movements.items():
            new_pos = (character_pos[0] + dy, character_pos[1] + dx)
            if new_pos[0] < 0 or new_pos[0] >= len(grid[0]) or new_pos[1] < 0 or new_pos[1] >= len(grid[1]):
                valid_actions.append(action)
            elif grid[new_pos[0]][new_pos[1]] in {0, 3}:
                valid_actions.append(action)

        if len(valid_actions) == 0:
            # Very specific case when the head is
            # surrounded by the body
            valid_actions = [0, 1, 2, 3]

        return valid_actions
