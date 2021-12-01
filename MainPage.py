# Exercise tracker application for the final project of CMSC 437
# Author: Chase Fenton
# Email: wfenton1@umbc.edu

# TODO LIST:
# TODO: CREATE THE EXERCISE PAGE.
# TODO: LEARN HOW TO INTEGRATE A SQLITE DATABASE.
# TODO: FIND OUT HOW TO DYNAMICALLY UPDATE TKINTER FRAMES.

import tkinter as tk
from tkinter import font as tkfont

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('Exercise Tracker')
        self.minsize(600, 450)
        self.maxsize(1000, 750)

        # Set up the fonts.
        self.fonts = {
            'title':tkfont.Font(family='Helvetica', size=22, weight='bold'),
            'body':tkfont.Font(family='Helvetica', size=14),
            'buttons':tkfont.Font(family='Helvetica', size=14, weight='bold'),
        }

        # Create the container to show all the pages in.
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Set up the pages in the app.
        self.frames = {}

        for F in (MainPage, HelpPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Make sure to put all the pages in the same place.
            frame.grid(row=0, column=0, sticky='nsew')

        # Show the starting page after setup is done. 
        
        self.show_frame('MainPage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = 'white'

        # Create title label.
        title_label = tk.Label(
            self, 
            text='Exercise Tracker', 
            font=controller.fonts['title']
        )
        title_label.pack(side='top', fill='x', expand=False)

        # Create subtitle label.
        subtitle_label = tk.Label(
            self, 
            text='Click the "Get Started" button to see the instructions.',
            font=controller.fonts['body'],
        )
        subtitle_label.pack(side='top', fill='x', expand=False)

        # Create the Get Started button.
        help_button = tk.Button(
            self, 
            text='Get Started',
            font=controller.fonts['buttons'],
            command=lambda: controller.show_frame('HelpPage'),
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        help_button.pack(side='bottom', fill='both', expand=False)

class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = 'white'

        # Create title label.
        title_label = tk.Label(
            self, 
            text='Exercise Tracker', 
            font=controller.fonts['title']
        )
        title_label.pack(side='top', fill='x', expand=False)

        # Create subtitle label.
        subtitle_label = tk.Label(
            self, 
            text='Help Page',
            font=controller.fonts['body'],
        )
        subtitle_label.pack(side='top', fill='x', expand=False)

        # Create the back button.
        back_button = tk.Button(
            self, 
            text='Back', 
            command=lambda: controller.show_frame('MainPage'),
            font=controller.fonts['buttons'],
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        back_button.pack(side='bottom', fill='x', expand=False)

        # Create the help text.
        help_text = \
            '''
            Lorem ipsum dolor sit amet, consectetur adipiscing el
            it. Donec ornare neque a feugiat tristique. Suspendiss
            e ultricies sem eu risus pellentesque interdum. Sed vu
            lputate porttitor nibh...
            '''
        help_label = tk.Label(
            self, 
            text=help_text,
            font=controller.fonts['body'],
        )
        help_label.pack(side='bottom', fill='x', expand=True)

if __name__ == '__main__':
    app = App()
    app.mainloop()