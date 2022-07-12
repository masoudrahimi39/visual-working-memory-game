import pygame
from buttons import NextButton, Title

class StartActualTask:
    def handler(self, screen) -> None:
        next_btn = NextButton(screen, clr_txt=(0,59,102), clr_brdr='white')
        title_bnt = Title(screen, clr_txt=(0,59,102), clr_brdr='white', show_up_txt="Click to start!")
        terminated = False
        while not terminated:
            event = pygame.event.wait()
                # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                terminated = next_btn.handle_click(event)
            next_btn.draw()
            title_bnt.draw()
            pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_color = ('white')
    screen.fill(screen_color)
    sater_actual_pg_obj = StartActualTask()
    sater_actual_pg_obj.handler(screen)
    pygame.quit()
