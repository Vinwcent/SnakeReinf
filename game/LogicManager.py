import random

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class LogicManager():

    def __init__(self, grid_size):
        """
        Basic constructor
        """
        self.grid_size = grid_size

        self._init_logic()

        self.prev_reward = 0

    def _init_logic(self):
        """
        Initialize the logic of the game
        """
        self.grid = [[0
                      for _ in range(self.grid_size[0])]
                     for _ in range(self.grid_size[1])]
        # Init the snake and the first apple
        self.snake = [[self.grid_size[0]//2, self.grid_size[1]//2]]
        self.grid[self.snake[0][0]][self.snake[0][1]] = 1

        self.apples = []
        self.add_apples()
        self._update_grid()

    def _update_grid(self):
        """
        Update the grid with the apples and snake arrays
        """
        self.grid = [[0
                      for _ in range(self.grid_size[0])]
                     for _ in range(self.grid_size[1])]
        for body_pos in self.snake:
            self.grid[body_pos[0]][body_pos[1]] = 1
        # Specific value for the head to show orientation
        self.grid[self.snake[0][0]][self.snake[0][1]] = 2
        for apple in self.apples:
            self.grid[apple[0]][apple[1]] = 3




    def _is_illegal(self, new_head_pos):
        """
        Check if the move of the head to the given position is illegal
        """
        if (len(self.snake) > 1 and
                new_head_pos == [self.snake[1][0], self.snake[1][1]]):
            return True
        return False

    def _is_loose(self, new_head_pos):
        """
        Check if the move of the head to the given position is a loosing move
        """
        if (
            new_head_pos in self.snake or
            new_head_pos[0] < 0 or
            new_head_pos[1] < 0 or
            new_head_pos[0] > self.grid_size[0] - 1 or
            new_head_pos[1] > self.grid_size[1] - 1
        ):

            return True

    def add_apples(self):
        """
        Try adding an apple,
        Send a winning signal if no apple can be placed meaning that the snake
        is on all the grid
        """
        eligible_pos = [[i, j]
                        for i in range(self.grid_size[0])
                        for j in range(self.grid_size[1])
                        if self.grid[i][j] == 0]
        # Win signal here
        if len(eligible_pos) == 0:
            return 1

        apple_pos = random.choice(eligible_pos)
        self.apples.append(apple_pos)
        return 0

    def update_logic(self, move):
        """
        Update the logic with a given move
        """
        self.prev_reward = 0
        new_head_pos = [self.snake[0][0] + move[0],
                        self.snake[0][1] + move[1]]
        if self._is_illegal(new_head_pos):
            return 0
        if self._is_loose(new_head_pos):
            return 1

        self.snake.insert(0, new_head_pos)
        value_at_pos = self.grid[self.snake[0][0]][self.snake[0][1]]
        if value_at_pos == 0:
            self.snake.pop(-1)
        elif value_at_pos == 3:
            self.prev_reward = 1
            self.apples.remove(self.snake[0])
            win = self.add_apples()
            if win:
                return 2
        self._update_grid()
        return 0





