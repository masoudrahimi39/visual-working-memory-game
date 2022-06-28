import random
import sys

import numpy as np
import pandas as pd
import pygame
from gym import Env
from gym.spaces import Box
from gym.utils.env_checker import check_env as check_env_gym
from stable_baselines3.common.env_checker import check_env as check_env_stable_baselines3

sys.path.append('/media/expansion/Master/DDA-Thesis/Implementation/001-/visual-spatial-memory-game')
from task import Task, task_param_based_on_screen
np.set_printoptions(precision=2)


class HoneyMemoryEnvHuman(Env):
    def __init__(self, task_database_path='dfclty_dtbs.pkl', episode_len=100, R_type='70-90', n_repeat=1):  
        self.action_space = Box(low=-1.0, high=1.0, shape=(1,))   # action: difficulty
        self.observation_space = Box(low=np.array([-1.0, 0.0]), high=np.array([1.0, 1.0]))  # state: : (difficulty, score)
        
        self.episode_len_init = episode_len                                # episode_len
        self.episode_len = episode_len 
        self.state =  self.reset()               # starting state 
        self.R_type = R_type                                               # R_type ∈ {'d*s', }
        self.n_repeat = n_repeat

        # TODO: below loading difficlty should be changed. it must be loaded once.
        self.dfclty_dtbs = pd.read_pickle(task_database_path)
        self.screen = self.start_rendering()
        self.position_init, self.R_hexagon = task_param_based_on_screen(self.screen)

    def start_rendering(self):
        ''' first initial the pygame, then it provide the welcome, sign up, guid, guiding task playing pages in pygame'''
        pygame.init()
        self.screen = pygame.display.set_mode((1919, 1079))
        self.screen.fill('white')
        return self.screen

    def provide_n_reapet_task(self, source_val):
        ''' we have a df whth two columns. 
                col_1=difficulty_nrmlizd: float, 
                col_2=indices_to_become_one: list(...); len(list) is various in each row.
            we want to choose n_repeat elemenet form the col_2 which have nearest value of col_1 to source_val.
            this fn do this'''
        spcified_dfclty_df = self.dfclty_dtbs.iloc[(self.dfclty_dtbs['dfclty_nrmlzd'] - source_val).abs().argsort()[:self.n_repeat]]
        spcified_dfclty_df.reset_index(drop=True, inplace=True)
        row = 0
        chosn_tsks = []
        n_need_to_chose = self.n_repeat
        while n_need_to_chose != 0:
            spcified_dfclty_lst_i = spcified_dfclty_df.loc[row, 'indcs_trgt']
            if len(spcified_dfclty_lst_i) >= n_need_to_chose:
                chosn_tsks.extend(random.choices(spcified_dfclty_lst_i, k=n_need_to_chose))
                n_need_to_chose = 0
            else:
                chosn_tsks.extend(spcified_dfclty_lst_i)
                n_need_to_chose -= len(spcified_dfclty_lst_i)
            row += 1
        return chosn_tsks
    
    def step(self, action):
        '''action: np: shape (1,): difficulty of the task; give the difficulty to the player agent
            and take the perfomance of the player agent'''
        # provide task to human player
        chosn_tsks = self.provide_n_reapet_task(source_val=action.item())
        score = self.render(chosn_tsks=chosn_tsks, dfclty=action.item())
        self.state = np.array([action.item(), score], dtype=np.float32)

        # reward based on R_type
        if self.R_type == 'd*s':
            reward = ((action.item()+1)/2)*(2*score)**2    # reward = action * score**2
        elif self.R_type == '70-90':
            if 0.7 <= score <= 0.9:
                reward = +1
            elif 0.9 < score <= 1:
                reward = 0
            else:
                reward = -1

        info = {}
        print(f'step({self.episode_len_init - self.episode_len}), sate {self.state}, reward({reward:.2f})')

        ### Check if it is terminal state
        self.episode_len -= 1 
        if self.episode_len == 0 :
            done = True 
        else:
            done = False
        return self.state, reward, done, info
    
    def reset(self):
        # TODO: starting state should be changed based on player performance  
        self.state = np.array([0.2, 0.5], np.float32)              # Reset the state
        self.episode_len = self.episode_len_init                   # Reset the episode len
        return self.state
     
    def render(self, chosn_tsks, dfclty):
        ''' get a list of tasks and provide that to the user and return the avg_score of the user
            input
            --------
                chosn_tsks: list(tuple, tuple) : each tuple indicate the indices of target cells in a single task
                dfclty: all tasks in in the chosn _tsks have same difficulty of dfclty
            output
            --------
                avg_score: float in range [0, 1]: avg of player score in each task of chosn_tsks'''
        avg_score = 0
        n = 0
        for indcs in chosn_tsks: 
            task_obj = Task(indices_target=indcs, difficulty=dfclty, user_id=100, 
                            position_init=self.position_init, R_hexagon=self.R_hexagon)
            score = task_obj.run_task(self.screen)
            avg_score = (avg_score*n + score) / (n+1)
            n += 1
        return avg_score

    def close(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()


# check if HoneyMemoryEnv is Gym-compatible.
if __name__ == '__main__':
    # env = HoneyMemoryEnvHuman(episode_len=2, n_repeat=1)
    # print('gym check_env')
    # check_env_gym(env, warn=True)
    # print('==='*10)
    print('stable baselines3 check_env')
    env = HoneyMemoryEnvHuman(episode_len=5, n_repeat=1)
    check_env_stable_baselines3(env, warn=True)
    

