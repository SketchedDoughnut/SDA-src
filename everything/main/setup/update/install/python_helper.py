# This code is taken and modified from loads.py, which is used in conways game of life to load maps
#########################################################################################################
# loading 
import os
import subprocess
# import json
# import time
import requests
import tkinter

TEXT_DATA = [
    """Welcome to the Python helper! This guide will help you through the process of installing Python. Click "Continue" to get started.""",

    """This project requires an installation of Python. It was specifically made on Python 3.11.""",

    """To check if you have Python installed, open command prompt and enter -
    -> "python --version". 
- You should get a version number back. This project can not guarantee proper functionality on versions other then Python 3.11.""",

    """If you have Python installed, click "Yes, I have Python" below. Otherwise, click "No, I do not have Python" below.""",

    """You now have two options. You can install Python from the Microsoft store, or install it via this installer.
If you use this installer, it will be quicker but slightly more complex. If you use the Microsoft Store, it will take longer but will be more simple.
It is advised that you use this installer (I spent a long time making the system :c ).
Select the respective buttons below to decide.""",

"""The installer will now install the Python installation agent, and then run it. When the installer runs, on the first page, please select the option to
"Install Now". As well as that, select the option to "Add Python.exe to PATH". These are both necessary settings for this project to work. On the last page, when Python
is done installing, select the checkbox that allows Python to make its PATH variable longer. Then, you're done!""",

"""
Do the followng instructions to install Python from the Microsoft Store:
- go to Microsoft Store
- search "Python 3.11"
- Install
- You're done!
NOTE: FUNCTIONALITY CAN NOT BE GUARANTEED WITH ANY OTHER PYTHON VERSIONS."""
]

text_1_2_1 = 'If you have Python installed, you can click "Exit" below. However, functionality can not be guaranteed with any versions besides Python 3.11.'
text_1_2_2 = 'If you want to go back, click "Go back" below.'

class Python_helper:
    def __init__(self, wDir):
        # unrelated jazz
        # self.wDir = os.path.dirname(os.path.abspath(__file__))
        # self.wDir = os.path.dirname(os.path.dirname(self.wDir))
        self.wDir = wDir

        # tkinter stuff
        self.window = tkinter.Tk(className="window~!")
        self.window.geometry('500x480')
        self.text = tkinter.StringVar()
        # self.text = tkinter.Text(wrap=tkinter.WORD)
        self.button_text = tkinter.StringVar()
        self.element_list = []
        self.phase = 0
        self.manual_set = False
        self.manual_phase = 0

        # CUSTOM VARIABLES
        self.run_install = False

    def reset_element_list(self):
        self.element_list = []

    def clear_screen(self):
        for element in self.window.winfo_children():
            element.destroy()

    def submit_elements(self, new_elements: list):
        self.element_list.extend(new_elements)

    def set_phase(self, prep_num: int):
        self.manual_set = True
        self.manual_phase = prep_num
        self.phase = self.manual_phase
        self.reset_element_list()
        self.main()

    def extender(self):
        self.phase += 1
        # self.clear_screen()
        self.reset_element_list()
        self.main()

    def reverser(self):
        self.phase -= 1
        # self.clear_screen()
        self.reset_element_list()
        self.main()

    def end(self):
        self.window.destroy()
        self.main('return')

    def pack_elements(self):
        for element in self.element_list:
            element.pack()

    def phase_setter(self, text: str = 'default', button_text: str = 'default'):
        self.text.set(text)
        self.button_text.set(button_text)

    def main(self, mode: str = 'op'):
        # return data
        if mode != 'op':
            return self.run_install # returns go here
        # introductions
        if self.phase == 0:
            self.clear_screen()
            self.reset_element_list()
            self.phase_setter(
                button_text="Continue"
            )
            label = self.label_wrapped(text_data=TEXT_DATA[0])
            self.submit_elements(
                [
                    label,
                    tkinter.Button(self.window, textvariable=self.button_text, command=self.extender)
                ]
            )
            self.pack_elements()
            self.window.mainloop()

        elif self.phase == 1:
            self.clear_screen()
            self.reset_element_list()
            label1 = self.label_wrapped(text_data=TEXT_DATA[2])
            label2 = self.label_wrapped(text_data=TEXT_DATA[3])
            self.submit_elements(
                [
                    label1,
                    label2,
                    tkinter.Button(self.window, text="Yes, I have Python", command=lambda: self.set_phase(2)),
                    tkinter.Button(self.window, text="No, I do not have Python", command=lambda:self.set_phase(3))
                ]
            )
            self.pack_elements()
            
        elif self.phase == 2:
            self.clear_screen()
            self.reset_element_list()
            label1 = self.label_wrapped(text_data=text_1_2_1)
            label2 = self.label_wrapped(text_data=text_1_2_2)
            self.submit_elements(
                [
                    label1,
                    label2,
                    tkinter.Button(self.window, text="Exit", command=self.end),
                    tkinter.Button(self.window, text="Go back", command=lambda:self.set_phase(1))
                ]
            )
            self.pack_elements()

        elif self.phase == 3:
            self.clear_screen()
            self.reset_element_list()
            label1 = self.label_wrapped(text_data=TEXT_DATA[4])
            self.run_install = False
            self.submit_elements(
                [
                    label1,
                    tkinter.Button(self.window, text="Microsoft store", command=lambda:self.set_phase(4)),
                    tkinter.Button(self.window, text="Install via this installer", command=lambda:self.set_phase(5)),
                    tkinter.Button(self.window, text="Go back", command=lambda:self.set_phase(1))
                ]
            )
            self.pack_elements()
        
        elif self.phase == 4:
            self.clear_screen()
            self.reset_element_list()
            label1 = self.label_wrapped(text_data=TEXT_DATA[6])
            self.submit_elements(
                [
                    label1,
                    tkinter.Button(self.window, text="Exit", command=self.end),
                    tkinter.Button(self.window, text="Go back", command=lambda:self.set_phase(3))
                ]
            )
            self.pack_elements()

        elif self.phase == 5:
            self.clear_screen()
            self.reset_element_list()
            label1 = self.label_wrapped(text_data=TEXT_DATA[5])
            self.run_install = True
            self.submit_elements(
                [
                    label1,
                    tkinter.Button(self.window, text="Continue", command=self.end),
                    tkinter.Button(self.window, text="Go back", command=lambda:self.set_phase(3))
                ]
            )
            self.pack_elements()





    # CUSTOM FUNCTIONS
    def label_wrapped(self, text_data: str = 'autofill', justifyer: str = 'center', wraplengther = 490, padding_x = 10, padding_y = 10) -> tkinter.Label:
        # justify can be center, left, or right
        # https://stackoverflow.com/questions/11949391/how-do-i-use-tkinter-to-create-line-wrapped-text-that-fills-the-width-of-the-win
        if text_data == 'autofill':
            text_data = self.text
        text_obj = tkinter.StringVar()
        text_obj.set(text_data)
        return tkinter.Label(self.window, textvariable=text_obj, justify=justifyer, wraplength=wraplengther, padx = padding_x, pady=padding_y)

    def run_python_installer(self):
        print('Getting installer data...')
        installer_data = requests.get('https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe')
        if installer_data.status_code == 200:
            tmp_path = self.wDir + '/tmp'
            try:
                print('Creating tmp directory...')
                os.mkdir(tmp_path)
            except:
                pass
            exec_path = tmp_path + '/python-3.11.9-amd64.exe'
            print('Writing to file...')
            f = open(exec_path, 'wb')
            f.write(installer_data.content)
            f.close()
            print('Running file...')
            # os.system(exec_path)
            subprocess.run(f"{exec_path}")
            print('Success!')

# Python_helper().main()