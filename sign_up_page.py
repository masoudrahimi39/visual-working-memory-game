# from platform import python_branch
import pygame
from buttons import NextButton, Title, TitleOfInputBox, InputBox

class SignUp:
    def __init__(self, screen):
        self.screen = screen 
        screen_width, screen_height = screen.get_size()
        self.user_info = {'sbjct_nmbr': None, 'tril_nmbr': None, 'name': None, 
                          'last_name': None, 'mobile': None, 'age': None, 'gender': None}
        self.title_box = Title(self.screen, show_up_txt='Sign Up')
        self.next_button = NextButton(self.screen)
        self.title_of_input_boxes = {'sbjct_nmbr': None, 'tril_nmbr': None, 'name': None, 
                                    'last_name': None, 'mobile': None, 'age': None, 'gender': None}
        self.input_boxes = {'sbjct_nmbr':None, 'tril_nmbr': None, 'name': None, 
                                    'last_name': None, 'mobile': None, 'age': None, 'gender': None}
        y_init_1 = screen_height/4
        y_init_2 = screen_height/4
        x_init_1 = 1*screen_width/5
        x_init_2 = 3*screen_width/5
        blank_spc = screen_height//27
        for ind, el in enumerate(['sbjct_nmbr', 'tril_nmbr', 'name', 'last_name', 'mobile', 'age', 'gender']):
            if ind <= 1:
                self.title_of_input_boxes[el] = TitleOfInputBox(self.screen, title_text=el, x=x_init_1, y=y_init_1)
                self.input_boxes[el] = InputBox(self.screen, type_text=el, x=x_init_1, y=y_init_1+blank_spc)
                y_init_1 += screen_height/8
            if ind > 1:
                self.title_of_input_boxes[el] = TitleOfInputBox(self.screen, title_text=el, x=x_init_2, y=y_init_2)
                self.input_boxes[el] = InputBox(self.screen, type_text=el, x=x_init_2, y=y_init_2+blank_spc)
                y_init_2 += screen_height/8
        
    def handeler(self):
        terminated = False
        while not terminated:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button.handle_click(event):
                    terminated = True
            
            for key, value in self.input_boxes.items():
                value.handle_event(event)
            
            # for event in pygame.event.get():
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if self.next_button.handle_click(event):
            #             terminated = True
            #     
            #     for key, value in self.input_boxes.items():
            #         value.handle_event(event)

            for input_boxes_obj in self.input_boxes.values():
                input_boxes_obj.draw(self.screen)
            for obj_titl_box in self.title_of_input_boxes.values():
                obj_titl_box.draw(self.screen)
            self.next_button.draw()
            self.title_box.draw()
            pygame.display.flip()
        
        # fill the dict named "user_info" which contains user info
        for obj_inp_bx in self.input_boxes.values():
            self.user_info[obj_inp_bx.type_text] = obj_inp_bx.text

        return self.user_info

    def __delete__(self):
        pass 
    
if __name__ == '__main__':
    pygame.init()
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1200, 1000))
    screen_color = (211,211,211)
    screen.fill(screen_color)
    sign_up_pg = SignUp(screen)
    user_info = sign_up_pg.handeler()
    print(user_info)
    pygame.quit()
