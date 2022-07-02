"Author: Masoud Rahimi"


from turtle import position
import pygame
from welcome_page import Welcome
from sign_up_page import SignUp
from guid_page import GuidPage
from task import Task, task_param_based_on_screen
from start_actual_task_page import StartActualTask

if __name__ == '__main__':
    pygame.init()
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1920, 1080))
    # screen = pygame.display.set_mode((800, 800))
    screen_color = (211,211,211)
    screen.fill(screen_color)

    # welcome page
    wlcom_obj = Welcome(screen)
    wlcom_obj.handler()
    screen.fill(screen_color)

    # sign up page
    sign_up_pg_obj = SignUp(screen)
    user_info = sign_up_pg_obj.handeler()
    print(user_info)

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
