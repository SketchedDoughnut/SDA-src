import pygame
from typing import Callable

class StartScreen:
    def __init__(self, window: pygame.Surface) -> None:
        ## self
        self.hide_the_kids = False
        self.window = window
        self.sc_unit_width = pygame.display.get_window_size()[0] # scale unit width
        self.sc_unit_height = pygame.display.get_window_size()[1] # scale unit height
        # - colors
        # https://colorspire.com/rgb-color-wheel/
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'less black': (10, 10, 10),
            'grey': (128, 128, 128),
            'red': (255, 0, 0),
            'background highlight': (212, 215, 246),
            'accent 1': (176, 168, 219),
            'accent 2': (113, 103, 165),
            'learn more': (165, 147, 200),
            #'exit': (243, 101, 101)
            'exit': (255, 46, 46),
            #'close': (16, 36, 114)
            'close': (40, 50, 90)
        }

        # - set up queues
        self.bg_queue = [] # format: [[color, rect]]
        self.button_queue = [] # format: [[color, rect, function]]
        self.text_queue = [] # format: [[text, text_rect]]

        ## get background dimensions, assemble background
        bg_color = self.colors['background highlight']
        self.bg_width = self.scale(1250, 'x')
        self.bg_height = self.scale(800, 'y')
        self.increment = self.bg_height / 15 # to used for positioning
        self.bg_x = self.sc_unit_width / 2
        self.bg_y = self.sc_unit_height / 2
        center_x = self.bg_x - (self.bg_width / 2)
        center_y = self.bg_y - (self.bg_height / 2)
        self.assemble_background(                                           # ASSEMBLE
            bg_color, 
            center_x, 
            center_y, 
            self.bg_width, 
            self.bg_height
        )

        ## accent rectangles
        # shadow for top left accent, accent 1
        sar1_c = self.colors['less black']
        sar1_width = self.scale(225, 'x')
        sar1_height = sar1_width
        sar1_x = self.bg_x - ((self.bg_width / 2) + self.scale(-40, 'x'))
        sar1_y = (self.bg_y - (self.bg_height / 2)) + self.scale(45, 'y')
        center_x = sar1_x - sar1_width / 2
        center_y = sar1_y - sar1_height / 2
        if not self.hide_the_kids:
            self.assemble_background(
                sar1_c, 
                center_x,
                center_y,
                sar1_width,
                sar1_height
            )

        # top left accent
        ar1_c = self.colors['accent 1']
        ar1_width = self.scale(225, 'x')
        ar1_height = ar1_width
        ar1_x = self.bg_x - ((self.bg_width / 2) + self.scale(5, 'x'))
        ar1_y = (self.bg_y - (self.bg_height / 2)) + self.scale(15, 'y')
        center_x = ar1_x - ar1_width / 2
        center_y = ar1_y - ar1_height / 2
        if not self.hide_the_kids:
            self.assemble_background(
                ar1_c, 
                center_x,
                center_y,
                ar1_width,
                ar1_height
            )

        # shadow for bottom right accent, accent 2
        sar2_c = self.colors['less black']
        sar2_width = self.scale(150, 'x')
        sar2_height = sar2_width
        sar2_x = (self.bg_x + ( self.bg_width / 2) - self.scale(50, 'x'))
        sar2_y = (self.bg_y + (1.5 * (self.bg_height / 4) + self.scale(25, 'y')))
        center_x = sar2_x - sar2_width / 2
        center_y = sar2_y - sar2_height / 2
        if not self.hide_the_kids:
            self.assemble_background(
                sar2_c, 
                center_x,
                center_y,
                sar2_width,
                sar2_height
            )

        # bottom right accent
        ar2_c = self.colors['accent 2']
        ar2_width = self.scale(150, 'x')
        ar2_height = ar2_width
        ar2_x = (self.bg_x +( self.bg_width / 2))
        ar2_y = (self.bg_y + (1.5 * (self.bg_height / 4)))
        center_x = ar2_x - ar2_width / 2
        center_y = ar2_y - ar2_height / 2
        if not self.hide_the_kids:
            self.assemble_background(
                ar2_c, 
                center_x,
                center_y,
                ar2_width,
                ar2_height
            )
        
        ## get close menu button dimensions, assemble button
        button_color = self.colors['close']
        button_width = self.scale(75, 'x')
        button_height = button_width
        button_x = (self.bg_x) + (self.bg_width / 2) - (button_width - self.scale(25, 'x'))
        button_y = self.bg_y - (self.bg_height / 2)  + (button_height - self.scale(26, 'y'))
        center_x = button_x - (button_width / 2) # center before inputting
        center_y = button_y - (button_height / 2) # center before inputting
        self.assemble_button(                                               # ASSEMBLE
            button_color,
            center_x, 
            center_y, 
            button_width,
            button_height,
            self.close_menu
        )

        ## get exit button dimensions, assemble button
        button_color = self.colors['exit']
        button_width = self.bg_width - self.scale(350, 'x')
        button_height = self.scale(65, 'y')
        button_x = self.bg_x
        button_y = (self.bg_y - self.bg_height / 2) + (14 * self.increment)
        center_x = button_x - (button_width / 2) # center before inputting
        center_y = button_y - (button_height / 2) # center before inputting
        self.assemble_button(                                               # ASSEMBLE
            button_color,
            center_x,
            center_y,
            button_width,
            button_height,
            self.exit_button
        )
        
        ## get learn more button, assemble button
        button_color = self.colors['learn more']
        button_width = self.bg_width / 4
        button_height = self.scale(50, 'y')
        button_x = self.bg_x - self.scale(577.5, 'x')
        button_y = self.bg_y + self.scale(155, 'y')
        self.assemble_button(
            button_color,
            button_x,
            button_y,
            button_width,
            button_height,
            self.learn_more
        )

        ## assemble learn more text
        txt_color = self.colors['black']
        txt_msg = 'learn more'
        txt_size = self.scale(45, 'x')
        txt_x = (self.bg_x / 2) - self.scale(60, 'x')
        txt_y = self.bg_y  + self.scale(157, 'y')
        self.assemble_text(
            txt_color,
            txt_size,
            txt_msg,
            txt_x,
            txt_y
        )

        ## assemble title text
        txt_color = self.colors['black']
        txt_msg = 'Conways Game of Life'
        txt_size = self.scale(75, 'x')
        txt_x = ((self.bg_x + self.bg_width / 2)) - ((self.bg_width / 2) + self.scale(375, 'x'))
        txt_y = (self.bg_y - self.bg_height / 2) + self.scale(20, 'y')
        self.assemble_text(
            color = txt_color, 
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '___________________'
        txt_x += self.scale(10, 'x')
        txt_y += self.scale(30,'y')
        self.assemble_text(
            color = txt_color, 
            size = txt_size,
            txt_msg = txt_msg, 
            x = txt_x,
            y = txt_y
        )

        txt_msg = '- space to pause/play -'
        txt_size = self.scale(42.5, 'x') # originally 45
        txt_x += self.scale(175, 'x') # originally 70
        txt_y += self.scale(75, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '- r to reset board -'
        txt_x += self.scale(45, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '- left click to single paint -'
        txt_x -= self.scale(85, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '- right click to paintbrush -'
        txt_x -= self.scale(7.5, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )
        

        txt_msg = '- esc to open this menu -'
        txt_x += self.scale(22.5, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '- E to export map, I to import -'
        txt_x -= self.scale(50, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )
        
        txt_msg = '____________'
        txt_size += self.scale(15, 'x')
        txt_x += self.scale(115, 'x')
        txt_y += self.scale(15, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '~ Credits ~'
        txt_x += self.scale(40, 'x') # originally 125
        txt_y += self.scale(60, 'y') # originally 115
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = '____________'
        txt_x -= self.scale(40, 'x') # originally 100
        txt_y += self.scale(15, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = 'Sketched Doughnut'
        txt_size -= self.scale(15, 'x')
        txt_x -= self.scale(5, 'x')
        txt_y += self.scale(75, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )

        txt_msg = 'i1aw'
        txt_x += self.scale(160, 'x')
        txt_y += self.scale(60, 'y')
        self.assemble_text(
            color = txt_color,
            size = txt_size,
            txt_msg = txt_msg,
            x = txt_x,
            y = txt_y
        )





    ## ASSEMBLY FUNCTIONS
    def assemble_background(self, color: tuple, x: int, y: int, width: int, height: int) -> None:
        bg_rect = pygame.Rect(x, y, width, height)
        self.bg_queue.append([color, bg_rect])

    def assemble_button(self, color: tuple, x: int, y: int, width: int, height: int, func: Callable) -> None:
        button_rect = pygame.Rect(x, y, width, height)
        self.button_queue.append([color, button_rect, func])

    def assemble_text(self, color: tuple, size: int, txt_msg: str, x: int, y: int) -> None:
        # f_size = round(self.scale((size * 1.5), 'x')) # size is normally 36 in other projects
        f_size = round(size) # size is normally 36 in other projects
        font = pygame.font.Font('freesansbold.ttf', f_size)
        text = font.render(txt_msg, True, color, None) # text, some bool(?), text color, bg color
        text_rect = text.get_rect()
        text_rect.topleft = (x, y)
        self.text_queue.append([text, text_rect])


    
    ## DRAW FUNCTION
    def draw(self, board: list) -> bool:
        # selfs
        self.board = board
        pressed = pygame.mouse.get_pressed()

        for bg in self.bg_queue:
            color = bg[0]
            rect = bg[1]
            pygame.draw.rect(self.window, color, rect)

        for button in self.button_queue:
            color = button[0]
            rect = button[1]
            function = button[2]
            pygame.draw.rect(self.window, color, rect)
            if rect.collidepoint(pygame.mouse.get_pos()) and pressed[0]:
                state =  function()
                if state != 'no return':
                    return state
        
        for text in self.text_queue:
            self.window.blit(text[0], text[1])

        return True, self.board







    ## TOOL FUNCTIONS
    # function to scale numbers
    def scale(self, num: int, mode: str) -> int:
        if mode == 'x': return (num / 1920) * pygame.display.get_window_size()[0]
        elif mode == 'y': return (num / 1080) * pygame.display.get_window_size()[1]


    ## BUTTONS

    # basic function to exit
    def exit_button(self) -> None:
        print('clicked on exit button')
        import sys
        sys.exit()

    # basic function to close menu
    def close_menu(self) -> bool:
        print('menu closed')
        # import eval
        # width = 100
        # height = width
        # self.board = eval.GenerateBoard(width, height)
        return False, self.board # to end start_menu
    
    def learn_more(self) -> None:
        import os
        import webbrowser
        #filename = 'file:///'+ os.getcwd() + '/' + 'test.html'
        filename = "https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life"
        webbrowser.open_new_tab(filename) 
        return 'no return'