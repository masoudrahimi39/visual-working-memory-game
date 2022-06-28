from gym.spaces import Box
from stable_baselines3 import PPO
from honey_memory_env_agent import HoneyMemoryEnvAgent
from honey_memory_env_human import HoneyMemoryEnvHuman
import gym
from stable_baselines3.common.evaluation import evaluate_policy

# used to turn of the warning
gym.logger.set_level(40)



###############################################
################### PPO #######################
# 1st training by agent
# episode_len = 100
# env_agent = HoneyMemoryEnvAgent(episode_len=episode_len, R_type='70-90', n_repeat=1, )
# model = PPO("MlpPolicy", env_agent, verbose=1, gamma=0.95)
# model.learn(total_timesteps=500000)
# model.save("ppo2_R_70_90_agent_traind")

# call a saved model on aget
# episode_len = 25
# env_agent = HoneyMemoryEnvAgent(episode_len=episode_len, R_type='70-90', n_repeat=1)
# model = PPO.load("ppo2_R_70_90_agent_traind", env=env_agent, verbose=1, gamma=0.97, n_steps=50)
# model.learn(total_timesteps=100)
# print(env_agent.cnt)
# model.save("ppo1_R_70_90_agent_traind")
# print(evaluate_policy(model, env_agent, n_eval_episodes=1000, deterministic=False))


# training with human
episode_len = 10
env_human = HoneyMemoryEnvHuman(episode_len=episode_len, R_type='70-90', n_repeat=1)
model = PPO.load("ppo2_R_70_90_agent_traind", env=env_human, n_steps=episode_len, verbose=1, gamma=0.95)
model.learn(total_timesteps=20)
model.save("ppo2_R_70_90_human_01")

