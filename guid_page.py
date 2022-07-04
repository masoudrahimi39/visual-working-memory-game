import pygame
from buttons import NextButton
import sys 
sys.path.append('/media/expansion/Master/DDA-Thesis/Implementation/001-/visual-spatial-memory-game')

class GuidPage:
    # def __init__(self) -> None:
        # self.screen = screen 

    def provide_guide(self, screen):
        img1 = pygame.image.load('guide_fa.png')
        next_obj = NextButton(screen, clr_brdr=(255, 255, 255))
        terminated = False
        while not terminated:
            event = pygame.event.wait()
            # for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                terminated = next_obj.handle_click(event)

            screen.blit(img1, (650, 50))
            next_obj.draw()
            pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_color = 'white'
    screen.fill(screen_color)
    obj = GuidPage()
    obj.provide_guide(screen)
    pygame.quit()
