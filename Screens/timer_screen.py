import tkinter as tk
import time
import serial

class Timerscreen():
    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container5= tk.Frame(self.frame)
        self.container5.pack()
        label3= tk.Label(self.container5, text= "Timer", font=("Arial", 20))
        label3.pack()

        self.clock= tk.Frame(self.container5)
        self.clock.pack(side= "top", expand= True, fill="x", padx=50)

        self.hour= 0
        self.minute= 0
        self.second= 0
        self.timer_running= False
        self.timer_paused= False

        self.hours = tk.Label(self.clock, text=f"{self.hour:02d}:", font=("Arial", 20), takefocus=True)
        self.hours.pack(side="left")

        self.minutes = tk.Label(self.clock, text=f"{self.minute:02d}:", font=("Arial", 20), takefocus=True)
        self.minutes.pack(side="left")

        self.seconds = tk.Label(self.clock, text=f"{self.second:02d}", font=("Arial", 20), takefocus=True)
        self.seconds.pack(side="left")

        self.start = tk.Button(self.container5, text="Starten", font=("Arial", 14), command=self.start_timer)
        self.start.pack()

        self.stop = tk.Button(self.container5, text="Stoppen", font=("Arial", 14), command=self.stop_timer)
        self.stop.pack()

        self.frame.bind("<Left>", lambda event: self.navigate("left"))
        self.frame.bind("<Right>", lambda event: self.navigate("right"))
        self.frame.bind("<Up>", lambda event: self.navigate("up"))
        self.frame.bind("<Down>", lambda event: self.navigate("down"))
        self.frame.bind("<F13>", lambda event: self.navigate("f13"))

        self.akt_widget = 1
        self.hours.configure(font=("Arial", 22, "bold"), highlightthickness=2)

    def navigate(self, action, event=None):
        current_focus = self.frame.focus_get()

        if action== "f13":
            self.stop.invoke()

        if current_focus == self.container5 or current_focus == self.frame or current_focus is None:
            if action == "left":
                if self.akt_widget <= 1:
                    self.akt_widget = 5
                else:
                    self.akt_widget = self.akt_widget - 1
            elif action == "right":
                if self.akt_widget >= 5:
                    self.akt_widget = 1
                else:
                    self.akt_widget = self.akt_widget + 1
            elif action == "down":
                self.app.show_menu()

            all_widgets = [self.hours, self.minutes, self.seconds, self.start, self.stop]
            for widget in all_widgets:
                if widget in [self.start, self.stop]:
                    widget.configure(font=("Arial", 14), highlightthickness=0)
                else:
                    widget.configure(font=("Arial", 20), highlightthickness=0)

            match self.akt_widget:
                case 1: self.hours.configure(font=("Arial", 22, "bold"), highlightthickness=2)
                case 2: self.minutes.configure(font=("Arial", 22, "bold"), highlightthickness=2)
                case 3: self.seconds.configure(font=("Arial", 22, "bold"), highlightthickness=2)
                case 4: self.start.configure(font=("Arial", 16, "bold"), highlightthickness=2)
                case 5: self.stop.configure(font=("Arial", 16, "bold"), highlightthickness=2)

            if action == "up":
                print(f"Betrete Widget {self.akt_widget}")
                match self.akt_widget:
                    case 1: self.hours.focus_set()
                    case 2: self.minutes.focus_set()
                    case 3: self.seconds.focus_set()
                    case 4: self.start.focus_set()
                    case 5: self.stop.focus_set()
                return "break"

        else:
            if action == "down" and (current_focus== self.hours or current_focus== self.minutes or current_focus== self.seconds or current_focus== self.start or current_focus== self.stop):
                print("Widget verlassen2 -> Zurück zum Navigationsmodus")
                self.container5.focus_set()
                return "break"

            if current_focus == self.hours:
                if action == "left":
                    self.hour = 23 if self.hour == 0 else self.hour - 1
                elif action == "right":
                    self.hour = 0 if self.hour == 23 else self.hour + 1
                self.hours.configure(text=f"{self.hour:02d}:")
                return "break"
                
            elif current_focus == self.minutes:
                if action == "left":
                    self.minute = 59 if self.minute == 0 else self.minute - 1
                elif action == "right":
                    self.minute = 0 if self.minute == 59 else self.minute + 1
                self.minutes.configure(text=f"{self.minute:02d}:")
                return "break"
                
            elif current_focus == self.seconds:
                if action == "left":
                    self.second = 59 if self.second == 0 else self.second - 1
                elif action == "right":
                    self.second = 0 if self.second == 59 else self.second + 1
                self.seconds.configure(text=f"{self.second:02d}")
                return "break"

            if action == "up" and current_focus in [self.start, self.stop]:
                current_focus.invoke()
                return "break"

        return "break"
        
    def start_timer(self):
        
        if self.timer_running== False:
            self.timer_paused= False
            self.timer_running = True
            self.start.configure(text="Pause")
            self.countdown()
        elif self.timer_running== True:
            self.timer_running= False
            self.timer_paused= True
            self.start.configure(text="Weiter")

    def stop_timer(self):
        self.timer_running = False
        self.timer_paused = True
        self.second= 0
        self.minute= 0
        self.hour= 0
        self.seconds.configure(text=f"{self.second:02d}", background="#F0F0F0")
        self.minutes.configure(text=f"{self.minute:02d}:", background="#F0F0F0")
        self.hours.configure(text=f"{self.hour:02d}:", background="#F0F0F0")
        self.start.configure(text="Start")

    def countdown(self):
        if self.timer_paused== False:
            self.hours.configure(background="lawn green")
            self.minutes.configure(background="lawn green")
            self.seconds.configure(background="lawn green")
            if self.second>0:
                self.second= self.second - 1
                self.seconds.configure(text=f"{self.second:02d}")
                self.container5.after(1000, self.countdown)
            elif self.second==0 and self.minute> 0:
                self.second= 59
                self.minute= self.minute - 1
                self.seconds.configure(text=f"{self.second:02d}")
                self.minutes.configure(text=f"{self.minute:02d}:")
                self.container5.after(1000, self.countdown)
            elif self.second==0 and self.minute== 0 and self.hour>0:
                self.second= 59
                self.minute= 59
                self.hour= self.hour-1
                self.seconds.configure(text=f"{self.second:02d}")
                self.minutes.configure(text=f"{self.minute:02d}:")
                self.hours.configure(text=f"{self.hour:02d}:")
                self.container5.after(1000, self.countdown)
            else:
                self.hours.configure(background="red")
                self.minutes.configure(background="red")
                self.seconds.configure(background="red")
                self.timer_running = False
                print("Alarm! Zeit vorbei!")
                self.klingel_schleife()

    def klingel_schleife(self):
        if self.timer_paused== True:
            print("Alarm beendet!")
            return
            
        self.app.pico.write(b"KLINGELN\n")
        
        self.container5.after(3000, self.klingel_schleife)