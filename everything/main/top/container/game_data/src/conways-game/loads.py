# loading 
import os
# import json
import time
# import pygame
import tkinter

class Map_loader:
    def __init__(self):
        # unrelated jazz
        self.wDir = os.path.dirname(os.path.abspath(__file__))

        # tkinter stuff
        self.window = tkinter.Tk(className="window~!")
        self.text = tkinter.StringVar()
        self.button_text = tkinter.StringVar()
        self.element_list = []
        self.phase = 0

    def reset_element_list(self):
        self.element_list = []

    def clear_screen(self):
        for element in self.window.winfo_children():
            element.destroy()

    def submit_elements(self, new_elements: list):
        self.element_list.extend(new_elements)

    def extender(self):
        self.phase += 1
        # self.clear_screen()
        self.reset_element_list()
        self.load_map()

    def reverser(self):
        self.phase -= 1
        # self.clear_screen()
        self.reset_element_list()
        self.load_map()

    def end(self):
        self.window.destroy()
        self.load_map('return')

    def pack_elements(self):
        for element in self.element_list:
            element.pack()

    def phase_setter(self, text: str, button_text: str):
        self.text.set(text)
        self.button_text.set(button_text)

    def load_map(self, mode: str = 'op'):
        # return data
        if mode != 'op':
            return self.map_path

        # instruct them on where to put file
        if self.phase == 0:
            self.clear_screen()
            self.reset_element_list()
            self.phase_setter(
                text=f"Please put your map file (.json) into the following directory:\n- {self.wDir}/maps_in/",
                button_text="Continue"
            )
            self.submit_elements(
                [
                    tkinter.Label(self.window, textvariable=self.text),
                    tkinter.Button(self.window, textvariable=self.button_text, command=self.extender)
                ]
            )
            self.pack_elements()
            self.window.mainloop()

        # get file path
        elif self.phase == 1:
            self.clear_screen()
            self.reset_element_list()
            self.phase_setter(
                text=f'Input the name of your map. Ex: my_map',
                button_text="Continue"
            )
            self.entry_element = tkinter.Entry(self.window)
            self.submit_elements(
                [
                    tkinter.Label(self.window, textvariable=self.text),
                    self.entry_element,
                    tkinter.Button(self.window, textvariable=self.button_text, command=self.extender)
                ]
            )
            self.pack_elements()
        
        # analyze file path
        elif self.phase == 2:
            map_name = self.entry_element.get()
            self.reset_element_list()
            self.clear_screen()
            self.map_path = f'{self.wDir}/maps_in/{map_name}.json'
            self.map_name = map_name
            self.phase_setter(
                text=f'The path is: {self.map_path}',
                button_text='not used'
            )
            self.submit_elements(
                [
                    tkinter.Label(self.window, textvariable=self.text),
                    tkinter.Button(self.window, text="Correct", command=self.extender),
                    tkinter.Button(self.window, text="Incorrect", command=self.reverser)
                ]
            )
            self.pack_elements()
        
        elif self.phase == 3:
            self.reset_element_list()
            self.clear_screen()
            self.phase_setter(
                text='Done!',
                button_text='Exit'
            )
            self.submit_elements(
                [
                    tkinter.Label(self.window, textvariable=self.text),
                    tkinter.Button(self.window, textvariable=self.button_text, command=self.end)
                ]
            )
            self.pack_elements()



        ############################# LEGACY CODE



        # end current session
        # for _ in range(3):
        #     print('----------------------')
        # print('Exiting current session...')
        # pygame.quit()
        # print('----------------------')
        # print('Please put your map file (.json) into the following directory:')
        # print(f'- {wDir}/maps_in/')
        # input('Enter anything to continue: ')
        # while True:
        #     print('----------------------')
        #     print('Input the name of your map. Ex: my_map:')
        #     map_name = input('-> ')
        #     print('----------------------')
        #     print('Assembling path of map...')
        #     map_path = f'{wDir}/maps_in/{map_name}.json'
        #     print('----------------------')
        #     print('The path is:', map_path)
        #     if input('If this is right, enter y. otherwise, enter anything else to redo this\n-> ').lower() == 'y':
        #         break
        # print('Returning path...')

# test run
# l = Map_loader()
# l.load_map()