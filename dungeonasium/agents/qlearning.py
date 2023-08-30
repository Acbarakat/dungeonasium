import numpy as np
import gymnasium as gym
from tqdm import tqdm
from IPython.display import display
from ipywidgets import widgets

from .base import BaseAgent


class QLearningAgent(BaseAgent):
    def __init__(self,
                 env: gym.vector.AsyncVectorEnv | gym.vector.SyncVectorEnv,
                 learning_rate=0.1,
                 discount_factor=0.9,
                 exploration_prob=1.0,
                 exploration_decay=0.995,
                 min_exploration_prob=0.1,
                 weighted_actions: bool = False) -> None:
        super().__init__(env)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.exploration_decay = exploration_decay
        self.min_exploration_prob = min_exploration_prob
        self.weighted_actions = weighted_actions

        self.state_space_size = env.metadata['size']
        self.action_space_size = env.action_space.nvec  # Action space size

        self.q_table = np.zeros((*self.state_space_size,
                                 self.action_space_size[0]))

    def choose_action(self, states):
        if self.env.np_random.uniform(0, 1) < self.exploration_prob:
            return self.env.action_space.sample()  # Choose a random action

        result = []
        for state in states["agent"]:
            state = tuple(state)
            weights = self.q_table[state].sum()
            if self.weighted_actions or weights == 0.0:
                if weights == 0.0:
                    weights = None
                else:
                    weights = self.q_table[state] / weights
                actions = list(range(self.action_space_size[0]))
                result.extend(self.env.np_random.choice(actions, 1, p=weights))
            else:
                # Choose the action with the highest Q-value
                result.append(np.argmax(self.q_table[state]))
        return result

    def update_q_table(self, states, actions, rewards, next_states):
        for state, action, reward, next_state in zip(states["agent"], actions, rewards, next_states["agent"]):
            next_state = tuple(next_state)
            state = tuple(state)
            best_next_action = np.argmax(self.q_table[next_state])
            # print(state, action, reward, next_state, best_next_action)
            idx = state + (action, )
            idx2 = next_state + (best_next_action, )
            try:
                self.q_table[idx] = (1 - self.learning_rate) * self.q_table[idx] + self.learning_rate * (reward + self.discount_factor * self.q_table[idx2])
            except IndexError:
                print(self.q_table[next_state])
                print(idx, idx2)
                raise

    def train(self, num_episodes, update_table=True):
        progress = tqdm(range(num_episodes),
                        disable=self.render_mode == "jupyter",
                        desc="training",
                        postfix={
                            "avg_reward": 0,
                            "exploration_prob": self.exploration_prob
                        })

        if self.render_mode == "jupyter":
            handles = []
            progress_bar = widgets.IntProgress(value=0, min=0, max=num_episodes, description="Training:")

            display(progress_bar, display_id=True)

        total_reward = 0
        for episode in progress:
            states, info = self.env.reset()
            done = np.array([False])

            while not done.any():
                actions = self.choose_action(states)
                next_states, rewards, done, _, info = self.env.step(actions)
                if "img" in info and self.render_mode == "jupyter":
                    for i, img in enumerate(info["img"]):
                        if len(handles) < i + 1 or handles[i] is None:
                            handle = display(img, display_id=True)
                            handles.append(handle)
                        elif img is not None:
                            handles[i].update(img)

                total_reward += rewards.sum()
                if update_table:
                    self.update_q_table(states, actions, rewards, next_states)

                states = next_states

            self.exploration_prob = max(self.min_exploration_prob, self.exploration_prob * self.exploration_decay)

            if self.render_mode == "jupyter":
                progress_bar.value += 1
            else:
                progress.set_postfix({
                    "avg_reward": total_reward / (episode + 1),
                    "exploration_prob": self.exploration_prob
                })
