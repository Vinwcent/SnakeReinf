import time
import numpy as np
from tqdm import tqdm
from collections import defaultdict

def perform_mc(env, num_episodes, epsilon, gamma, rewards):
    """
    Perform monte carlo algorithm on num_episodes with epsilon moves on the
    Snake environment.

    Rewards should be given in the form of a list in the order :
    [Losing move, Inefficient move, Efficient move, Winning move]
    """
    action_space_size = 4
    q_table = defaultdict(lambda: np.zeros(action_space_size))
    state_action_count = defaultdict(lambda: np.zeros(action_space_size))
    for _ in tqdm(range(num_episodes)):
        episode_rewards = []
        episode_states = []
        episode_actions = []
        state, _ = env.reset()
        n_step = 0
        while True:
            actions = env.get_valid_actions(state)
            action = epsilon_greedy_policy(tuple(tuple(x) for x in state),
                                           actions,
                                           q_table,
                                           epsilon)
            next_state, reward, done, _ = env.step(action)
            # Reward is:
            # -1 if the move made the player lose
            # 0 if no apple is taken
            # 1 if apple is taken
            # 10 if the player won (screen full of snake)

            if reward == -1:
                reward = rewards[0]
            elif reward == 0:
                reward = rewards[1]
            elif reward == 1:
                reward = rewards[2]
            else:
                reward = rewards[3]
            episode_rewards.append(reward)
            episode_states.append(tuple(tuple(x) for x in state))
            episode_actions.append(action)
            if done or n_step > 100:
                break
            state = next_state
        unique_state_action_pairs = list(set(zip(episode_states, episode_actions)))

        for state, action in unique_state_action_pairs:
            indices = [i for i, (s, a) in enumerate(zip(episode_states, episode_actions)) if s == state and a == action]
            for i in indices:
                G = sum([episode_rewards[j]*gamma**(j-i) for j in range(i, len(episode_rewards))])
                state_action_count[state][action] += 1
                q_table[state][action] += (G - q_table[state][action]) / state_action_count[state][action]

    return q_table

def epsilon_greedy_policy(state, actions, q_table, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(actions)
    else:
        q_values = {action: q_table[state][action] for action in actions}
        return max(q_values, key=q_values.get)

def show_games(env, n_games, q_table, time_between_plays=0.2):
    assert env.with_rendering, "You need to activate rendering on the \
    environment to see the game"

    total_reward = 0
    for i in range(n_games):
        state, _ = env.reset()

        episode_reward = 0
        done = False
        while not done:
            time.sleep(time_between_plays)
            actions = env.get_valid_actions(state)
            action = epsilon_greedy_policy(tuple(tuple(x) for x in state),
                                           actions,
                                           q_table,
                                           0.00)
            new_state, reward, done, _ = env.step(action)
            episode_reward += reward
            state = new_state
        print(f"Reward on game {i} was {episode_reward}")

        total_reward += episode_reward
