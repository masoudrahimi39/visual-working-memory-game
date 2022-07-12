"Author: Masoud Rahimi"

import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygame

from guid_page import GuidPage
from sign_up_page import SignUp
from start_actual_task_page import StartActualTask
from task import Task, task_param_based_on_screen
from task_guiding import TaskGuiding
from welcome_page import Welcome


def dda_rule_based(*, screen, episode_len, user_info, do_sv_gm_ply_dt, gm_ply_dt_file_nm, num_x, num_y,
                   is_eye_tracker, tracker):
    '''provide task with rule based policy in order to Difficulty Adjustment
            input
            ------
                is_eye_tracker: boolean: if True, there is a eye tracker device, else there is not.
                tracker: tracer object: it is used if is_eye_tracker == True else ignored
                screen: pygame screen obj
                episode_len: number of tasks that is provided to the user
                user_info: dict: it contains the user info. it is passed to the task_object
                num_x, num_y: int: respectively, number of columns and number of rows in the task. it is passed 
                        to the task_obj
                do_sv_gm_ply_dt: Bollean: if True, save the game play data. If False, do not save the game play data
                gm_ply_dt_file_nm: str: if do_sv_gm_ply_dt == True, it is used as file name to save 
                        the game play data in csv and pkl format 
            output
            ------
                it provide the tasak
                '''
    # get parameters to pass into the Task based on screen size
    position_init, R_hexagon = task_param_based_on_screen(screen)
    # a list to store the player scores
    score_list = []
    game_play_data_list = []
    position_init, R_hexagon = task_param_based_on_screen(screen)
    n_target = 5
    for t in range(episode_len):
        n_target = np.clip(n_target, a_min = 4, a_max = 14) 
        
        can_be_target_cell = set(range(36)) - {0, 5, 8, 9, 11, 17, 20, 22, 30, 33, 35}
        indces_one = random.sample(can_be_target_cell, k=n_target)
        task_obj = Task(indices_target=indces_one, dda_mthd='rule-base', user_info=user_info, difficulty=None, 
                        num_x=num_x, num_y=num_y, show_time=2, position_init=position_init, R_hexagon=R_hexagon,
                        is_eye_tracker=is_eye_tracker, tracker=tracker)
        score = task_obj.run_task(screen)
        game_play_data_list.append(vars(task_obj))
        print('(n_target, score): ', n_target,', ',  score)
        score_list.append(score)
        if 0.9 < score <= 1:
            n_target += 1 
        elif 0 <= score < 0.7:
            n_target -= 1
    
    # save the game play data into a csv and pkl file
    if do_sv_gm_ply_dt == True:
        game_play_data_df = pd.DataFrame.from_dict(game_play_data_list)
        game_play_data_df.to_csv(gm_ply_dt_file_nm + '.csv')
        game_play_data_df.to_pickle(gm_ply_dt_file_nm + '.pkl')

    return score_list


def game_provider_rule_based(*, episode_len):
    '''it is used to provide rule-based spatial working memroy'''
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen_color = (211,211,211)
    screen.fill(screen_color)

    ### welcome page
    wlcom_obj = Welcome(screen)
    wlcom_obj.handler()
    screen.fill(screen_color)

    ### sign up page
    sign_up_pg_obj = SignUp(screen, clr_scrn=screen_color)
    user_info = sign_up_pg_obj.handeler()    # user_info is a dictionary contains user data

    ### guiding page
    screen.fill('white')
    guid_obj = GuidPage()
    guid_obj.provide_guide(screen)

    ### guiding task playing
    position_inti, R_hexagon= task_param_based_on_screen(screen=screen)
    for indices in ((1, 4, 13), (4, 10, 15, 23), (9, 12, 17, 21, 23), (3, 4, 9, 10, 15, 16, 20)):
        screen.fill('white')
        task_obj = TaskGuiding(indices_target=indices, position_init=position_inti, R_hexagon=R_hexagon,
                               show_time=2, num_x=6, num_y=6)
        task_obj.run_guiding_task(screen)
        # break


    ### go to actual task
    screen.fill('white')
    sater_actual_pg_obj = StartActualTask()
    sater_actual_pg_obj.handler(screen)


    ### running Rule-based 
    screen.fill('white') 
    score_list = dda_rule_based(screen=screen, episode_len=episode_len, user_info=user_info, do_sv_gm_ply_dt=True,
                gm_ply_dt_file_nm='test_rule_base', num_x=6, num_y=6, is_eye_tracker=False, tracker=None)
    
    pygame.display.quit()
    pygame.quit()

    return score_list




if __name__ == '__main__':
    score_list = game_provider_rule_based(episode_len=10    )
    plt.plot(score_list)
    plt.title('your score graph')
    plt.xlabel('step')
    plt.ylabel('score')
    plt.show()
    

