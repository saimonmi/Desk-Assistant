import tkinter as tk
import time

class Stopwatch():
    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container7= tk.Frame(self.frame)
        self.container7.pack()
        label4= tk.Label(self.container7, text= "Stopwatch", font=("Arial", 20))
        label4.pack()
        
        self.hour= 0
        self.minute= 0
        self.second= 0
        self.millisecond= 0
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

        self.clock= tk.Frame(self.container7)
        self.clock.pack(side= "top", expand= True, fill="x", padx=50)

        self.hours= tk.Label(self.clock, text= f"{self.hour:02d}:", font=("Arial", 20))
        self.hours.pack(side= "left")

        self.minutes= tk.Label(self.clock, text= f"{self.minute:02d}:", font=("Arial", 20))
        self.minutes.pack(side= "left")

        self.seconds= tk.Label(self.clock, text= f"{self.second:02d}:", font=("Arial", 20))
        self.seconds.pack(side= "left")

        self.milliseconds= tk.Label(self.clock, text= f"{self.millisecond:02d}", font=("Arial", 20))
        self.milliseconds.pack(side= "left")

        self.button_frame = tk.Frame(self.container7)
        self.button_frame.pack(side="top", pady=10)

        self.start = tk.Button(self.button_frame, text="Start", font=("Arial", 14), command=self.start_stopwatch)
        self.start.pack(side="left", padx=5)
        
        self.reset = tk.Button(self.button_frame, text="Reset", font=("Arial", 14), command=self.reset_stopwatch)
        self.reset.pack(side="left", padx=5)

        self.lap = tk.Button(self.button_frame, text="Runde", font=("Arial", 14), command=self.save_lap)
        self.lap.pack(side="left", padx=5)

        self.lap.bind("<Up>", lambda event: [self.navigate("up"), "break"][-1])
        self.lap.bind("<Down>", lambda event: [self.navigate("down"), "break"][-1])

        self.lap_liste = tk.Frame(self.container7)
        self.lap_liste.pack(side="top", fill="x", pady=10)

        self.laps = []

        self.start.bind("<Up>", lambda event: [self.navigate("up"), "break"][-1])
        self.start.bind("<Down>", lambda event: [self.navigate("down"), "break"][-1])

        self.reset.bind("<Up>", lambda event: [self.navigate("up"), "break"][-1])
        self.reset.bind("<Down>", lambda event: [self.navigate("down"), "break"][-1])
        
        self.container7.bind("<Left>", lambda event:self.navigate("left"))
        self.container7.bind("<Right>", lambda event:self.navigate("right"))
        self.container7.bind("<Up>", lambda event:self.navigate("up"))
        self.container7.bind("<Down>", lambda event:self.navigate("down"))
        self.container7.bind("<F13>", lambda event:self.navigate("f13"))
        self.start.bind("<F13>", lambda event: self.navigate("f13"))
        self.reset.bind("<F13>", lambda event: self.navigate("f13"))
        self.lap.bind("<F13>", lambda event: self.navigate("f13"))

        self.akt_widget=0

    def update_clock(self):
        if self.running== True:
            
            total_elapsed = time.time() - self.start_time + self.elapsed_time
            
            self.hour = int(total_elapsed // 3600)
            self.minute = int((total_elapsed % 3600) // 60)
            self.second = int(total_elapsed % 60)
            self.millisecond = int((total_elapsed % 1) * 100)
            
            
            self.hours.configure(text= f"{self.hour:02d}:")
            self.minutes.configure(text= f"{self.minute:02d}:")
            self.seconds.configure(text= f"{self.second:02d}:")
            self.milliseconds.configure(text= f"{self.millisecond:02d}")
            
            self.container7.after(10, self.update_clock)

    def start_stopwatch(self):
        if self.running== False:
            self.start_time = time.time()
            self.running = True
            self.update_clock()
            self.start.configure(text="Pause")
        elif self.running== True:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            self.start.configure(text="Start")

    def reset_stopwatch(self):
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.hour= 0
        self.minute= 0
        self.second= 0
        self.millisecond= 0
        self.hours.configure(text= f"{self.hour:02d}:")
        self.minutes.configure(text= f"{self.minute:02d}:")
        self.seconds.configure(text= f"{self.second:02d}:")
        self.milliseconds.configure(text= f"{self.millisecond:02d}")
        for rundenlabel in self.laps:
            rundenlabel.destroy()
        self.laps = []

    def save_lap(self):
        aktuelle_zeit = (time.time() - self.start_time + self.elapsed_time) if self.running else self.elapsed_time

        h = int(aktuelle_zeit // 3600)
        m = int((aktuelle_zeit % 3600) // 60)
        s = int(aktuelle_zeit % 60)
        ms = int((aktuelle_zeit % 1) * 100)

        rundenlabel = tk.Label(self.lap_liste, text=f"Runde {len(self.laps)+1}: {h:02d}:{m:02d}:{s:02d}:{ms:02d}", font=("Arial", 12))
        rundenlabel.pack()
        self.laps.append(rundenlabel)

    def navigate(self, action, event=None):
        current_focus= self.container7.focus_get()

        if action == "up":
            if current_focus == self.start or current_focus == self.reset or current_focus == self.lap:
                current_focus.invoke()

            elif current_focus == self.container7:
                print("Widget entern")
                match self.akt_widget:
                    case 1:
                        self.start.focus_set()
                        self.start.configure(highlightcolor= "lawn green")
                    case 2:
                        self.reset.focus_set()
                        self.reset.configure(highlightcolor= "lawn green")
                    case 3:
                        self.lap.focus_set()
                        self.lap.configure(highlightcolor= "lawn green")

        if action == "f13":
            self.lap.invoke()

        if action == "down":
            if current_focus == self.container7:
                self.app.show_menu()
                print("Zurück zum Menü")
            else:
                print("Widget verlassen -> Zurück zum Navigationsmodus")
                self.container7.focus_set() 

        if action == "left":
            if self.akt_widget <= 1:
                self.akt_widget = 3
            else:
                self.akt_widget = self.akt_widget - 1

        elif action == "right":
            if self.akt_widget >= 3:
                self.akt_widget = 1
            else:
                self.akt_widget = self.akt_widget + 1

        all_widgets= [self.start, self.reset, self.lap]
        for widget in all_widgets:
            widget.configure(font=("Arial", 14), highlightthickness=0)

        match self.akt_widget:
            case 1:
                self.start.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 2:
                self.reset.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 3:
                self.lap.configure(font=("Arial", 16, "bold"),highlightthickness=2)