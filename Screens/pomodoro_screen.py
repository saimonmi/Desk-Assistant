import tkinter as tk

class Pomodoro():
    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container8= tk.Frame(self.frame)
        self.container8.pack()
        label5= tk.Label(self.container8, text= "Pomodoro erstellen", font=("Arial", 20))
        label5.pack()

        self.container8.bind("<Up>", self.app.show_pomodoro)
        