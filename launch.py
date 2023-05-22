from game.Snake import Snake
from reinf.SnakeEnv import SnakeEnv
from reinf.utils import perform_mc, show_games

# Winning everytime hyperparameters
grid_length = 4
n_episodes = 1
epsilon = 0.
gamma = 0.
rewards = [0, 0, 0, 0]
# [Losing move, inefficient move, efficient move, winning move]

# Playing part
game = Snake((800, 800), grid_length)
game.start_interactive_game()

# Training part
env = SnakeEnv(grid_length=grid_length, with_rendering=False)
q_table = perform_mc(env, n_episodes, epsilon, gamma, rewards)


# Viz part
env = SnakeEnv(grid_length=grid_length, with_rendering=True)
show_games(env, 100, q_table)
