# This file contains things that aren't pages, but are still used in the program. 
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import sqlite3

class ExerciseWidget(tk.Frame):
    def __init__(self, parent, controller, title):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = 'white'

        # Create title label.
        title_label = tk.Label(
            self, 
            text=f'{title}', 
            font=controller.fonts['body']
        )
        title_label.pack(side='left', expand=False)

        # Create the delete button.
        delete_button = tk.Button(
            self,
            text='Del',
            command=lambda: self.destroy_exercise(),
            font=controller.fonts['buttons'],
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        delete_button.pack(side='right', expand=False)

        # Create the reps count textbox.
        reps_count_text = tk.Entry(
            self, 
            width=2,
        )
        reps_count_text.pack(side='right', expand=False)

        # Create the reps label.
        reps_label = tk.Label(
            self,
            text='Reps:',
            font=controller.fonts['body'],
        )
        reps_label.pack(side='right', expand=False)

        # Create the resistance textbox
        res_count_text = tk.Entry(
            self, 
            width=2,
        )
        res_count_text.pack(side='right', expand=False)

        # Create the resistance label.
        res_label = tk.Label(
            self,
            text='Res:',
            font=controller.fonts['body'],
        )
        res_label.pack(side='right', expand=False)

    # This method is used for deleting exercises.
    def destroy_exercise(self):
        self.pack_forget()
        self.destroy()

class EntryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.geometry('300x100')
        self.title('Enter Exercise Name')

        self.entry_box = tk.Entry(
            self, 
            width=30,
            exportselection=0,
        )
        self.entry_box.pack(side='top', fill='x', expand=False)
        
        done_button = tk.Button(
            self, 
            text='Done',
            command=lambda: self.finished_entry(),
            bg='red',
            fg='white',
            activebackground='white',
            activeforeground='red',
        )
        done_button.pack(side='bottom', fill='x', expand=False)

    def finished_entry(self):
        name = self.entry_box.get()

        if name.isspace() or name == '':
            messagebox.showerror('Error', 'Empty exercise name!')
            return -1

        conn = sqlite3.connect('exercises.db')
        c = conn.cursor()

        try:
            c.execute(f'''
            INSERT INTO exercises (exercise_name)
            
                VALUES
                ('{name}')
            ''')
        except sqlite3.Error as e:
            print(e.__class__)

        conn.commit()
        conn.close()

        if name not in self.parent.exercises.keys():
            exercise = ExerciseWidget(
                parent=self.parent.exercise_frame.scrollable_frame, 
                controller=self.parent.controller,
                title=name
                )
            self.parent.exercises[name] = exercise
            exercise.pack(side='top', fill='x', expand=False)
        else:
            messagebox.showerror('Error', 'Duplicate exercise!')

        self.destroy()

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")