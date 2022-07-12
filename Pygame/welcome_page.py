import pygame
from buttons import NextButton, Title

class Welcome:
    def __init__(self, screen) -> None:
        self.screen = screen

    def handler(self) -> None:
        next_btn = NextButton(self.screen, clr_txt=(0,59,102))
        title_bnt = Title(self.screen, clr_txt=(0,59,102), clr_brdr=(211, 211, 211), show_up_txt="Welcome")
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
    # width, height = pygame.display.get_desktop_sizes()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # print(type(screen))
    screen_color = (211,211,211)
    screen.fill(screen_color)
    obj_wlcom = Welcome(screen)
    obj_wlcom.handler()
    pygame.quit()
