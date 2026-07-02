import tkinter as tk
import time

class Homescreen():
    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container1= tk.Frame(self.frame)
        self.container1.pack()
      
        self.zeit = tk.Label(self.container1, font=("Arial", 24))
        self.zeit.pack()
        
        self.container1.bind("<Up>", self.app.show_menu)

        self.update()  

    def update(self):
        current_time = time.strftime("%A-%d %B %y\n %H:%M:%S")
        self.zeit.config(text= current_time)
        
        self.container1.after(1000, self.update)