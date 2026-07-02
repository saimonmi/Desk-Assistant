import tkinter as tk

class Menuscreen():

    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container2= tk.Frame(self.frame)
        self.container2.pack()

        self.screens = ["Home", "Alarme","Timer","Stoppuhr"]
        self.aktuell = 0
        self.screens [self.aktuell]

        self.menulist = tk.Label(self.container2, text=self.screens[self.aktuell], font=("Arial", 24))
        self.menulist.pack()

        self.container2.bind("<Left>", self.previous_screen)
        self.container2.bind("<Right>", self.next_screen)
        self.container2.bind("<Up>", self.to_screen)
        self.container2.bind("<Down>", self.app.show_home)

    def previous_screen(self, event=None):
        if self.aktuell == 0:
            self.aktuell = 3
            self.update_screen()
        else:
            self.aktuell = (self.aktuell - 1)
            self.update_screen()

    def next_screen(self, event=None):
        if self.aktuell == 3:
            self.aktuell = 0
            self.update_screen()
        else:
            self.aktuell = (self.aktuell + 1)
            self.update_screen()
        
    def update_screen(self):
        self.menulist.config(text=self.screens[self.aktuell])

    def to_screen(self, event=None):
        match self.aktuell:
            case 0:
                self.app.show_home()
            case 1:
                self.app.show_alarm()
            case 2:
                self.app.show_timer()
            case 3:
                self.app.show_stopwatch()