# from tkinter import W
import pygame


class NextButton:
    def __init__(self, screen, clr_txt=(0,59,102), clr_brdr=(211,211,211), w=280, h=70, show_up_txt='Next'):
        self.screen = screen
        # get the screen based parameters; x, y, w, font size are determined based on screen size
        screen_width, screen_height = screen.get_size()
        FONT = pygame.font.Font(None, screen_width//24)
        text_width, text_height = FONT.size(show_up_txt) 
        w = text_width*1.14
        x = 5*screen_width/6 - w/2
        y = 3*screen_height/4
        self.rect = pygame.Rect(x, y, w, h)
        self.clr_brdr = clr_brdr
        
        self.txt_surface = FONT.render(show_up_txt, True, clr_txt)
        self.go_next_page = False
        # self.clr_brdr = 'black'

    def handle_click(self, click_event):
        if self.rect.collidepoint(click_event.pos):
            self.go_next_page = True
        else:
            self.go_next_page = False
        return self.go_next_page

    def draw(self):
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.clr_brdr, self.rect, 2)

class Title:
    def __init__(self, screen, font_ratio_to_screen=20 ,clr_txt=(0,59,102), clr_brdr=(211,211,211), h=90, show_up_txt=""):
        self.screen = screen 
        screen_width, screen_height = screen.get_size()
        self.FONT = pygame.font.Font(None, screen_width//font_ratio_to_screen)
        text_width, text_height = self.FONT.size(show_up_txt) 
        w = text_width*1.08
        x = screen_width/2 - w/2
        y = screen_height/30
        
        self.rect = pygame.Rect(x, y, w, h)
        
        self.txt_surface = self.FONT.render(show_up_txt, True, clr_txt)
        self.clr_brdr = clr_brdr
        # self.clr_brdr = 'black'

    def draw(self):
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.clr_brdr, self.rect, 2)
        # pygame.display.flip()
 
class TitleOfInputBox:
    def __init__(self, screen, title_text, x, y, w=280, clr_brdr_inactive=(192,192,192), clr_txt=(0,59,102)):

        self.title_text = title_text
        # get the screen based parameters; x, y, w, font size are determined based on screen size
        screen_width, screen_height = screen.get_size()
        self.FONT = pygame.font.Font(None, screen_width//48)
        w = screen_width//7
        h = screen_height//27
        self.rect = pygame.Rect(x, y, w, h)
        self.clr_brdr_inactive = clr_brdr_inactive
        blank_spc = (w//10 - len(title_text))//2 if title_text != 'last_name' else (w//11 - len(title_text))//2
        self.txt_surface = self.FONT.render(self.title_text.capitalize(), True, clr_txt)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.clr_brdr_inactive, self.rect, 2)

class InputBox:
    ''' https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame '''
    def __init__(self, screen, type_text, x, y, clr_brdr_inactive=(192,192,192), 
                 clr_brdr_active=(105,105,105), clr_txt=(0,59,102)):

        self.type_text = type_text
        self.text = ''
        # rect paramters based on screen size
        screen_width, screen_height = screen.get_size()
        self.FONT = pygame.font.Font(None, screen_width//48)
        w = screen_width//7
        h = screen_height//18
        self.rect = pygame.Rect(x, y, w, h)
        self.clr_txt = clr_txt
        self.clr_brdr = clr_brdr_inactive
        self.clr_brdr_inactive = clr_brdr_inactive
        self.clr_brdr_active = clr_brdr_active
        self.txt_surface = self.FONT.render(self.text, True, clr_txt)
        self.active = False

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.clr_brdr = self.clr_brdr_active         # Change the current color of the input box.
            else:
                self.active = False
                self.clr_brdr = self.clr_brdr_inactive       # Change the current color of the input box.

        elif event.type == pygame.KEYDOWN:        
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.clr_txt)

        

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.clr_brdr, self.rect, 2)




