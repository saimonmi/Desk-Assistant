import tkinter as tk
from Screens.home_screen import Homescreen
from Screens.menu_screen import Menuscreen
from Screens.alarm_screen import Alarmscreen
from Screens.timer_screen import Timerscreen
from Screens.stopwatch_screen import Stopwatch
import serial

class App():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x500")

        self.pico=serial.Serial("COM5", 115200, timeout=1)

        self.home= Homescreen(self.window, self)
        self.menu= Menuscreen(self.window, self)
        self.alarm= Alarmscreen(self.window, self)
        self.timer= Timerscreen(self.window, self)
        self.stopwatch= Stopwatch(self.window, self)

        self.show_home()
        
        self.window.mainloop()

    def show_home(self, event=None):
        self.menu.container2.pack_forget()
        self.alarm.container3.pack_forget()
        self.timer.container5.pack_forget()
        self.stopwatch.container7.pack_forget()
        self.home.container1.pack()
        self.home.container1.focus_set()
        
    def show_menu(self, event=None):
        self.timer.container5.pack_forget()
        self.alarm.container3.pack_forget()
        self.home.container1.pack_forget()
        self.stopwatch.container7.pack_forget()
        self.menu.container2.pack()
        self.menu.container2.focus_set()

    def show_alarm(self, event=None):
        self.home.container1.pack_forget()
        self.menu.container2.pack_forget()
        self.alarm.container3.pack()
        self.alarm.container3.focus_set()

    def show_timer(self, event=None):
        self.menu.container2.pack_forget()
        self.timer.container5.pack()
        self.timer.container5.focus_set()
        
    def show_stopwatch(self, event=None):
        self.menu.container2.pack_forget()
        self.stopwatch.container7.pack()
        self.stopwatch.container7.focus_set()  

App()