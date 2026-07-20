import tkinter as tk
import time
 
class Alarmscreen():
    def __init__(self, frame, app_controller):
        self.app = app_controller
        self.frame= frame
        self.container3= tk.Frame(self.frame)
        self.container3.pack()
        label= tk.Label(self.container3, text= "Alarmliste", font=("Arial", 20))
        label.pack()
        
        self.alarmliste= []

        self.alarm_running = False
       
        self.last_triggered_minute = -1

        for l in self.alarmliste:
            l= tk.Label(self.container3)

        self.new_alarm_btn = tk.Button(self.container3, text="+ neuer Alarm", font=("Arial", 12), command=self.show_new_alarm)
        self.new_alarm_btn.pack(side="bottom")
            
        self.container3.bind("<Down>", lambda event: self.navigate_main("down"))
        self.container3.bind("<Up>", lambda event: self.navigate_main("up"))
        self.container3.bind("<SHIFT_R>", lambda event: self.navigate_main("shiftr"))

        self.check_alarms()
    
    def show_new_alarm(self, event=None):
        self.ex_window= tk.Toplevel(self.frame)
        self.ex_window.geometry("500x300")
        self.container4= tk.Frame(self.ex_window)
        self.container4.pack()
        self.container4.focus_set()

        titel= tk.Label(self.container4, text= "Neuen Alarm erstellen", font=("Arial", 20))
        titel.pack(side= "top")

        self.clock= tk.Label(self.container4)
        self.clock.pack(side= "top")

        self.hours= tk.Spinbox(self.clock, from_=0, to=23, font=("Arial", 12), wrap= True, format="%02.0f", state= "readonly")
        self.hours.pack(side= "left")

        self.minutes= tk.Spinbox(self.clock, from_=0, to=59, font=("Arial", 12), wrap= True, format="%02.0f", state= "readonly")
        self.minutes.pack(side= "right")        

        self.hours.bind("<Up>", lambda event: "break")
        self.minutes.bind("<Up>", lambda event: "break")

        self.hours.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])
        self.minutes.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])

        self.hours.bind("<Left>", lambda event: [self.navigate_popup("left"), "break"][-1])
        self.hours.bind("<Right>", lambda event: [self.navigate_popup("right"), "break"][-1])
        self.minutes.bind("<Left>", lambda event: [self.navigate_popup("left"), "break"][-1])
        self.minutes.bind("<Right>", lambda event: [self.navigate_popup("right"), "break"][-1])

        self.active_var = tk.BooleanVar(value=False)
        self.active= tk.Checkbutton(self.container4, variable=self.active_var)
        self.active.pack()

        self.active.bind("<Up>", lambda event: [self.navigate_popup("up"), "break"][-1])
        self.active.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])

        self.msg= tk.Entry(self.container4, width=40, font=("Arial", 12))
        self.msg.pack()

        self.msg.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])

        self.delete= tk.Button(self.container4, text= "Löschen", font=("Arial", 12), command= lambda: self.ex_window.destroy())
        self.delete.pack(side=tk.LEFT)

        self.delete.bind("<Up>", lambda event: [self.navigate_popup("up"), "break"][-1])
        self.delete.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])

        self.save= tk.Button(self.container4, text= "Speichern", font=("Arial", 12), command= self.saved)
        self.save.pack(side=tk.RIGHT)

        self.save.bind("<Up>", lambda event: [self.navigate_popup("up"), "break"][-1])
        self.save.bind("<Down>", lambda event: [self.navigate_popup("down"), "break"][-1])
       
        self.container4.bind("<Left>", lambda event: self.navigate_popup("left"))
        self.container4.bind("<Right>", lambda event: self.navigate_popup("right"))
        self.container4.bind("<Up>", lambda event: self.navigate_popup("up"))
        self.container4.bind("<Down>", lambda event: self.navigate_popup("down"))
        
        self.akt_widget=0

    def saved(self):
        stunden_wert = self.hours.get()
        minuten_wert = self.minutes.get()
        neuer_alarm= Add_Alarm(self.container3, self.msg, self.active_var, stunden_wert, minuten_wert, len(self.alarmliste)+1)
        self.alarmliste.append(neuer_alarm)
        print("saved")
        self.ex_window.destroy()
        self.container3.focus_set()

    def navigate_main(self, action):
        current_focus = self.container3.focus_get()
        
        if action == "up" and current_focus== self.container3:
            print("Neuen Alarm erstellen")
            self.new_alarm_btn.invoke()
        
        if action == "down" and current_focus== self.container3:
            self.app.show_menu()
            print("Zurück zum Menü")
        
        if action == "shiftr":
            self.stop_alarm()

    def navigate_popup(self, action, event=None):
        current_focus = self.container4.focus_get()
        if action == "left" and current_focus== self.container4:
            if self.akt_widget <= 1:
                self.akt_widget = 6
            else:
                self.akt_widget = self.akt_widget - 1
            print(self.akt_widget)

        elif action == "right" and current_focus== self.container4:
            if self.akt_widget >= 6:
                self.akt_widget = 1
            else:
                self.akt_widget = self.akt_widget + 1
            print(self.akt_widget)

        all_widgets= [self.hours, self.minutes, self.active, self.msg, self.delete, self.save]
        for widget in all_widgets:
            widget.configure(font=("Arial", 12))

        match self.akt_widget:
            case 1:
                self.hours.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 2:
                self.minutes.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 3:
                self.active.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 4:
                self.msg.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 5:
                self.delete.configure(font=("Arial", 16, "bold"),highlightthickness=2)
            case 6:
                self.save.configure(font=("Arial", 16, "bold"),highlightthickness=2)

        if action == "up":
            if current_focus== self.container4:
                print("Widget entern")
                match self.akt_widget:
                    case 1:
                        print("hours entered")
                        self.hours.focus_set()
                        self.hours.configure(highlightcolor= "lawn green")
                    case 2:
                        print("minutes entered")
                        self.minutes.focus_set()
                        self.minutes.configure(highlightcolor= "lawn green")
                    case 3:
                        print("active entered")
                        self.active.focus_set()
                        self.hours.configure(highlightcolor= "lawn green")
                    case 4:
                        print("msg entered")
                        self.msg.focus_set()
                        self.msg.configure(highlightcolor= "lawn green")
                    case 5:
                        print("delete entered")
                        self.delete.focus_set()
                        self.delete.configure(highlightcolor= "lawn green")
                    case 6:
                        print("save entered")
                        self.save.focus_set()
                        self.save.configure(highlightcolor= "lawn green")

            elif current_focus == self.active:
                self.active_var.set(not self.active_var.get())
                print("Checkbox getoggled")

            elif current_focus== self.delete:
                self.delete.invoke()
                print("Button gedrückt")
            
            elif current_focus== self.save:
                self.saved()
                print("Button gedrückt")

        if action == "down" and current_focus in all_widgets:
            print("Widget verlassen1 -> Zurück zum Navigationsmodus")
            self.container4.focus_set()
               
        if current_focus == self.hours or current_focus == self.minutes:
            if action == "left":
                current_focus.invoke("buttondown")
                
            elif action == "right":
                current_focus.invoke("buttonup")
                 
    def check_alarms(self):
        jetzt = time.localtime()
        jetzt_stunde = jetzt.tm_hour
        jetzt_minute = jetzt.tm_min
        
        if jetzt.tm_min != self.last_triggered_minute and self.alarm_running == False:
            for alarm in self.alarmliste:
                if alarm.aktiv and alarm.stunden_wert == jetzt_stunde and alarm.minuten_wert == jetzt_minute:
                    print(f"Alarm ausgelöst für {alarm.titel_text} {alarm.stunden_wert:02d}:{alarm.minuten_wert:02d}!")
                    self.last_triggered_minute = jetzt.tm_min
                    self.start_alarm()
                    break

        self.container3.after(1000, self.check_alarms)

    def start_alarm(self):
        self.alarm_running = True
        self.app.show_alarm() 
        self.alarm_klingel_schleife()

    def stop_alarm(self):
        print("Alarm erfolgreich beendet!")
        self.alarm_running = False

    def alarm_klingel_schleife(self):
        if self.alarm_running == False:
            return
            
        self.app.pico.write(b"KLINGELN\n")
    
        self.container3.after(3000, self.alarm_klingel_schleife)

class Add_Alarm(Alarmscreen):
    def __init__(self, parent, text, check_var, stunden, minuten, lenlist):

        self.aktiv = check_var.get()
        self.stunden_wert = int(stunden)
        self.minuten_wert = int(minuten)        

        if text.get().strip():
            self.titel_text= text.get()
        else:
            self.titel_text= f"Alarm {lenlist}:"

        new_container= tk.Frame(parent)
        new_container.pack(expand=True, fill="x")

        if self.aktiv:
            new_container.configure(background="lawn green")
            bagr= "lawn green"
        else:
            new_container.configure(background="dim gray")
            bagr= "dim gray"
     
        self.titel= tk.Label(new_container, text= self.titel_text, font=("Arial", 14), background= bagr)
        self.titel.pack(side="left")
    
        zeit= tk.Label(new_container, text=f"{self.stunden_wert:02d}:{self.minuten_wert:02d}", font= ("Arial", 14), background= bagr)
        zeit.pack(side="right")
        new_container.configure(background= bagr)
