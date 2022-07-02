import sys
sys.path.append('/media/expansion/Master/DDA-Thesis/Implementation/001-/visual-spatial-memory-game')

import pygame
from welcome_page import Welcome
from sign_up_page import SignUp
from guid_page import GuidPage
from task import Task, task_param_based_on_screen
from start_actual_task_page import StartActualTask
import os

from stable_baselines3 import PPO
from honey_memory_env_agent import HoneyMemoryEnvAgent
from honey_memory_env_human import HoneyMemoryEnvHuman
import gym
from stable_baselines3.common.evaluation import evaluate_policy
import matplotlib.pyplot as plt

from openGazeNew import OpenGazeTracker



pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen_color = (211,211,211)
screen.fill(screen_color)

# welcome page
wlcom_obj = Welcome(screen)
wlcom_obj.handler()
screen.fill(screen_color)

# sign up page
sign_up_pg_obj = SignUp(screen)
user_info = sign_up_pg_obj.handeler()
sbjct_nmbr = sign_up_pg_obj.user_info['sbjct_nmbr']

# guide page
screen.fill('white')
guid_obj = GuidPage()
guid_obj.provide_guide(screen)

# guiding task playing
position_inti, R_hexagon= task_param_based_on_screen(screen=screen)
screen.fill('white')
for indices in ((1, 4, 13), (4, 10, 15, 23), (9, 12, 17, 21, 23), (3, 4, 9, 10, 15, 16, 20)):
    screen.fill('white')
    task_obj = Task(indices, position_init=position_inti, R_hexagon=R_hexagon)
    task_obj.run_guiding_task(screen)
    break

# go to actual task
screen.fill('white')
sater_actual_pg_obj = StartActualTask()
sater_actual_pg_obj.handler(screen)

# initialize eye tracker for RL-based
methd = 'M1'
file_name = 'S' + sbjct_nmbr + '_' + methd + '_ET' + '.tsv'
dir = os.path.dirname(os.path.abspath(__file__))
TSV_FILE_DIR = dir + '/TSVFiles'
TSV_FILE_NAMES = os.path.join(TSV_FILE_DIR, file_name)

# Tracker Object Definition
tracker = OpenGazeTracker(logfile=TSV_FILE_NAMES, debug=False)
# Calibrate the tracker.
print("calibrating")
tracker.calibrate()
print("calibration done")

# running RL 
episode_len = 25
env_human = HoneyMemoryEnvHuman(tracker, episode_len=episode_len, R_type='70-90', n_repeat=1)
model = PPO.load("ppo1_R_70_90_agent_traind", env=env_human, n_steps=episode_len, verbose=1, gamma=0.95)
model.learn(total_timesteps=episode_len*1)

# stop eye tracker
tracker.stop_recording()
# close connection to the tracker
tracker.close()
model.save("ppo1_R_70_90_human_01")


# running Rule-based


# actual task playing
print('==='*20, '\n\nwarning: you have to change difficulty and user_id. there have been set temporarily\n\n', '==='*20)
screen.fill('white')
for indices in ((1, 4, 13), (4, 10, 15, 23), (4, 5, 23)):
# for indices in ((1, 4, 13), (4, 10, 15, 23), (9, 12, 17, 21, 23), (3, 4, 9, 10, 15, 16, 20)):
    screen.fill('white')
    task_obj = Task(indices, position_init=position_inti, R_hexagon=R_hexagon)
    task_obj.run_task(screen)
    # break

pygame.quit()