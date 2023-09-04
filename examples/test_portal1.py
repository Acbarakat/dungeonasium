import gymnasium as gym

from dungeonasium.agents import qlearning

gym.register("portal1", "dungeonasium.envs.portal_worlds:PortalWorldEnv")

if __name__ == "__main__":
    # Create the Q-learning agent instance
    agent = qlearning.QLearningAgent(
        gym.make_vec("portal1", render_mode=None, num_envs=10)
    )

    # Train the agent
    agent.train(int(5e3))
    agent.env.close()

    # Visualize/Test play on whats been learned
    agent.env = gym.make_vec("portal1", render_mode="human")
    # agent.exploration_prob = 0.0
    print(agent.exploration_prob)
    agent.weighted_actions = True
    agent.train(5, update_table=False)
    agent.env.close()
