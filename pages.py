# Exercise tracker application for the final project of CMSC 437
# Author: Chase Fenton
# Email: wfenton1@umbc.edu

# TODO LIST:
# TODO: ADD SOME ERROR CHECKING.

import tkinter as tk
from tkinter import font as tkfont
from datetime import date
import sqlite3

from tools import *


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

        for F in (MainPage, HelpPage, TrackerPage):
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

        # Create the track button.
        track_button = tk.Button(
            self, 
            text='Track Exercises',
            font=controller.fonts['buttons'],
            command=lambda: controller.show_frame('TrackerPage'),
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        track_button.pack(side='bottom', fill='both', expand=False)

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
            This is a simple exercise tracker.

            When you open this program, 
            a database file will be created for you in the directory this file is stored in.

            To get started, press the 'Track Exercises' button to go to the tracker page. 
            You can add exercises to the page by pressing the 'Add Exercise' button on the tracker page. 
            When you add, you will be prompted for a name. 
            Enter either a new exercise or an exercise you have already done before.
            If you enter a new exercise, you will add that exercise to the database and to the page. 
            If you enter one you have already done before, it will just be added to the page. 
            Once you have added all your exercises for the day, 
            enter the resistance ('res') and repetitions ('reps') for your exercise.
            Once you're done, you can press the 'Done' button 
            to add all your exercise data (reps and resistance) to the database. 
            When you're done, simply close the window with the 'x' button.
            '''
        help_label = tk.Label(
            self, 
            text=help_text,
            font=controller.fonts['body'],
        )
        help_label.pack(side='bottom', fill='x', expand=True)

class TrackerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = 'white'
        
        # We will need to keep track of exercises we have added.
        self.exercises = {}

        self.exercise_frame = ScrollableFrame(self)
        
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
            text=f'{date.today()}',
            font=controller.fonts['body'],
        )
        subtitle_label.pack(side='top', fill='x', expand=False)

        self.exercise_frame.pack(side='top', fill='x', expand=False)

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

        # Create the done button.
        done_button = tk.Button(
            self, 
            text='Done',
            command=lambda: self.finish_day(),
            font=controller.fonts['buttons'],
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        done_button.pack(side='bottom', fill='x', expand=False)

        # Create the add exercise button.
        add_button = tk.Button(
            self,
            text='Add Exercise',
            command=lambda: self.add_exercise(),
            font=controller.fonts['buttons'],
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        add_button.pack(side='bottom', fill='x', expand=False)

    # This method facilitates adding an exercise widget to the tracker page. 
    def add_exercise(self):
        entry_window = EntryWindow(self)
    
    def finish_day(self):
        conn = sqlite3.connect('exercises.db')
        

        for f in self.exercises.values():
            exercise_name = f.title
            exercise_reps = f.reps_count_text.get()
            exercise_res = f.res_count_text.get()
            
            # select the id from the given name.
            c = conn.execute(f"SELECT exercise_id FROM exercises WHERE exercise_name='{exercise_name}'")

            exercise_id = c.fetchone()[0]

            c = conn.execute(f'''
            INSERT INTO data (date, exercise_id, reps, resistance)

                VALUES
                ('{date.today()}', '{exercise_id}', '{exercise_reps}', '{exercise_res}')
            ''')

        conn.commit()
        conn.close()


def init_database():
    conn = None
    try:
        conn = sqlite3.connect('exercises.db')
        print(sqlite3.version)

        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS exercises
        ([exercise_id] INTEGER PRIMARY KEY AUTOINCREMENT, [exercise_name] TEXT NOT NULL UNIQUE);
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS data
        ([entry_id] INTEGER PRIMARY KEY AUTOINCREMENT,
         [date] TEXT NOT NULL,
         [exercise_id] INT NOT NULL, 
         [reps] INT NOT NULL,
         [resistance] INT NOT NULL);
        ''')
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_database()
    app = App()
    app.mainloop()