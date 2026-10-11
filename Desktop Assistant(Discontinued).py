import os
import tkinter as tk
import datetime as dt
import subprocess
from zoneinfo import ZoneInfo, available_timezones
from tkinter import ttk
from tkinter import messagebox,filedialog as fd
import psutil as ps
import random
os.system('cls' if os.name == 'nt' else 'clear')
current_module = None
active_button = None

ALL_TIMEZONES = sorted(available_timezones())
def open_timer_stopwatch_view():
    global current_module
    if current_module is not None and hasattr(current_module, "stop"):
        current_module.stop()
        current_module = None
    for widget in main_content.winfo_children():
        widget.destroy()

    current_module = TimerStopwatchModule(main_content)
    current_module.pack(fill="both", expand=True)
def show_module(name, button):
    global active_button, current_module
    if current_module is not None and hasattr(current_module, "stop"):
        current_module.stop()
        current_module = None
    for widget in main_content.winfo_children():
        widget.destroy()
    if active_button is not None:
        active_button.config(bg="SystemButtonFace")
    active_button = button
    button.config(bg="lightblue")
    maincontenttitle = tk.Label(main_content, text=name, font=("Arial", 16, "bold"))
    maincontenttitle.pack(side="top", anchor="n", pady=10)

    if name == "TIME & DATE":
        root.geometry("520x660")
        current_module = TimeDateModule(main_content)
        current_module.pack(fill="both", expand=True)
    elif name == "SYSTEM":
        root.geometry("520x660")
        current_module = SystemModule(main_content)
        current_module.pack(fill="both", expand=True)
    elif name =="FILES":
        root.geometry("750x660")
        current_module = FilesModule(main_content)
        current_module.pack(fill="both",expand=True)
    elif name == "UTILITIES":
        root.geometry("560x860")
        current_module = UtilitiesModule(main_content)
        current_module.pack(fill="both", expand=True)
    elif name == "NETWORK":
        root.geometry("520x660")
    elif name == "NOTES":
        root.geometry("520x660")
        notes_label = tk.Label(main_content, text="посмотри файл 'заметка для notes '", font=("Arial", 14))
        notes_label.pack(pady=20)
class TimeDateModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.clock_after_id = None
        self.current_timezone = ZoneInfo("Europe/Kyiv")

        self.timezone_menu = None
        self.apply_button = None
        self.close_timezone_button = None

        self.time_label = tk.Label(self, font=("Arial", 16))
        self.time_label.pack(side="top", anchor="n")

        self.date_label = tk.Label(self, font=("Arial", 16))
        self.date_label.pack(side="top", anchor="n")

        self.day_label = tk.Label(self, font=("Arial", 16))
        self.day_label.pack(side="top", anchor="n")

        self.timezone_label = tk.Label(self, font=("Arial", 16))
        self.timezone_label.pack(side="top", anchor="n")

        self.timezone_buttons_frame = tk.Frame(self)
        self.timezone_buttons_frame.pack(side="top", pady=10)

        self.timezone_button = tk.Button(self.timezone_buttons_frame,text="Change timezone",font=("Arial", 16),command=self.change_timezone)
        self.timezone_button.pack(side="left")

        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(fill="x", pady=15)

        self.time_button = tk.Button(self,text="Timer and Stopwatch",font=("Arial", 16),command=open_timer_stopwatch_view)
        self.time_button.pack(side="top", pady=10)

        self.update_clock()
    def update_clock(self):
        clock = dt.datetime.now(self.current_timezone)
        self.time_label.config(text=clock.strftime("%H:%M:%S"))
        self.date_label.config(text=clock.strftime("%d %B %Y"))
        self.day_label.config(text=clock.strftime("%A"))
        self.timezone_label.config(text=str(self.current_timezone))
        self.clock_after_id = self.after(1000, self.update_clock)
    def change_timezone(self):
        if self.timezone_menu is None:
            self.timezone_menu = ttk.Combobox(self,values=ALL_TIMEZONES,font=("Arial", 16))
            self.timezone_menu.bind("<KeyRelease>", self.filter_timezones)
            self.timezone_menu.pack(side="top", pady=10, before=self.separator)
            self.close_timezone_button = tk.Button(self.timezone_buttons_frame,bg="Red",fg="White",text="X",font=("Arial", 16),command=self.close_timezone)
            self.close_timezone_button.pack(side="left", padx=(5, 0))
            self.apply_button = tk.Button(self,text="Apply",font=("Arial", 16),command=self.apply_timezone)
            self.apply_button.pack(side="top", pady=5, before=self.separator)
    def filter_timezones(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        typed_text = self.timezone_menu.get()

        if not typed_text:
            self.timezone_menu['values'] = ALL_TIMEZONES
        else:
            filtered = [tz for tz in ALL_TIMEZONES if typed_text in tz]
            self.timezone_menu['values'] = filtered
    def apply_timezone(self):
        selected_timezone = self.timezone_menu.get()
        if selected_timezone:
            self.current_timezone = ZoneInfo(selected_timezone)
            self.update_clock()
    def close_timezone(self):
        if self.timezone_menu is not None:
            self.timezone_menu.destroy()
            self.timezone_menu = None

        if self.apply_button is not None:
            self.apply_button.destroy()
            self.apply_button = None

        if self.close_timezone_button is not None:
            self.close_timezone_button.destroy()
            self.close_timezone_button = None
    def stop(self):
        if self.clock_after_id is not None:
            self.after_cancel(self.clock_after_id)
            self.clock_after_id = None
class TimerStopwatchModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.stopwatch_seconds = 0
        self.stopwatch_running = False
        self.stopwatch_after_id = None

        self.timer_seconds = 0
        self.timer_running = False
        self.timer_after_id = None

        header = tk.Frame(self)
        header.pack(side="top", fill="x", pady=5)
        tk.Button(header, bg="Red", fg="White", text="X", font=("Arial", 14),command=lambda: show_module('TIME & DATE', Button_TimeDate)).pack(side="left")
        tk.Label(header, text="STOPWATCH & TIMER", font=("Arial", 16, "bold")).pack(side="left", padx=10)

        self.stopwatch_label = tk.Label(self, text="00:00:00", font=("Arial", 20))
        self.stopwatch_label.pack(side="top", pady=5)

        sw_btns = tk.Frame(self)
        sw_btns.pack(side="top", pady=5)
        tk.Button(sw_btns, text="Start", font=("Arial", 16), command=self.start_stopwatch).pack(side="left", padx=2)
        tk.Button(sw_btns, text="Pause", font=("Arial", 16), command=self.stop_stopwatch).pack(side="left", padx=2)
        tk.Button(sw_btns, text="Reset",font=("Arial", 16), command=self.reset_stopwatch).pack(side="left", padx=2)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        self.timer_label = tk.Label(self, text="00:00", font=("Arial", 20))
        self.timer_label.pack(side="top", pady=5)

        entry_frame = tk.Frame(self)
        entry_frame.pack(side="top", pady=5)
        self.timer_entry_min = tk.Entry(
        entry_frame, width=4, font=("Arial", 16), justify="center")
        self.timer_entry_min.insert(0, "00")
        self.timer_entry_min.pack(side="left", padx=3)
        tk.Label(entry_frame, text=":", font=("Arial", 16, "bold")).pack(side="left", padx=2)
        self.timer_entry_sec = tk.Entry(entry_frame, width=4, font=("Arial", 16), justify="center")
        self.timer_entry_sec.insert(0, "00")
        self.timer_entry_sec.pack(side="left", padx=3)

        tm_btns = tk.Frame(self)
        tm_btns.pack(side="top", pady=5)
        tk.Button(tm_btns, text="Start", font=("Arial", 16), command=self.start_timer).pack(side="left", padx=2)
        tk.Button(tm_btns, text="Pause", font=("Arial", 16), command=self.stop_timer).pack(side="left", padx=2)
        tk.Button(tm_btns, text="Reset", font=("Arial", 16), command=self.reset_timer).pack(side="left", padx=2)

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_seconds += 1
            h = self.stopwatch_seconds // 3600
            m = (self.stopwatch_seconds % 3600) // 60
            s = self.stopwatch_seconds % 60
            self.stopwatch_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.stopwatch_after_id = self.after(1000, self.update_stopwatch)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.update_stopwatch()

    def stop_stopwatch(self):
        self.stopwatch_running = False
        if self.stopwatch_after_id:
            self.after_cancel(self.stopwatch_after_id)
            self.stopwatch_after_id = None

    def reset_stopwatch(self):
        self.stop_stopwatch()
        self.stopwatch_seconds = 0
        self.stopwatch_label.config(text="00:00:00")

    def update_timer(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_seconds -= 1
            m = self.timer_seconds // 60
            s = self.timer_seconds % 60
            self.timer_label.config(text=f"{m:02d}:{s:02d}")
            if self.timer_seconds > 0:
                self.timer_after_id = self.after(1000, self.update_timer)
            else:
                self.timer_running = False

    def start_timer(self):
        if not self.timer_running:
            if self.timer_seconds == 0:
                try:
                    m = int(self.timer_entry_min.get())
                except ValueError:
                    m = 0
                try:
                    s = int(self.timer_entry_sec.get())
                except ValueError:
                    s = 0
                self.timer_seconds = m * 60 + s
            if self.timer_seconds > 0:
                self.timer_running = True
                self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None

    def reset_timer(self):
        self.stop_timer()
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")

    def stop(self):
        self.stop_stopwatch()
        self.stop_timer()
class SystemModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.system_after_id = None
  
        self.cpu_label = tk.Label(self, font=("Arial", 16))
        self.cpu_label.pack(side="top", pady=(10, 2))
        self.cpu_bar = ttk.Progressbar(self, orient="horizontal", length=220, mode="determinate")
        self.cpu_bar.pack(side="top", pady=(0, 10))
        
        self.ram_label = tk.Label(self, font=("Arial", 16))
        self.ram_label.pack(side="top", pady=(10, 2))
        self.ram_bar = ttk.Progressbar(self, orient="horizontal", length=220, mode="determinate")
        self.ram_bar.pack(side="top", pady=(0, 10))

        self.disk_label = tk.Label(self, font=("Arial", 16))
        self.disk_label.pack(side="top", pady=(10, 2))
        self.disk_bar = ttk.Progressbar(self, orient="horizontal", length=220, mode="determinate")
        self.disk_bar.pack(side="top", pady=(0, 10))

        self.update_stats()
    def update_stats(self):
        cpu_usage = ps.cpu_percent()
        ram_usage = ps.virtual_memory().percent
        disk_usage = ps.disk_usage('/').percent

        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.ram_label.config(text=f"RAM Usage: {ram_usage}%")
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

        self.cpu_bar['value'] = cpu_usage
        self.ram_bar['value'] = ram_usage
        self.disk_bar['value'] = disk_usage
        self.system_after_id = self.after(1000, self.update_stats)
    def stop(self):
        if self.system_after_id is not None:
            self.after_cancel(self.system_after_id)
            self.system_after_id = None
class FilesModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_folder = ""
        self.folder_choose = tk.Button(self,text="Select Folder",font=("Arial",16),command=self.select_folder)
        self.folder_choose.pack(side="top", pady=5)
        self.path=tk.Label(self, text="Folder: Not selected", font=("Arial", 16), fg="gray",wraplength=450)
        self.path.pack(side="top",pady=5)

        search_frame = tk.Frame(self)
        search_frame.pack(side="top", pady=5)
        self.entry = tk.Entry(search_frame, font=("Arial", 16), width=18)
        self.entry.pack(side="left", padx=5)
        self.search_btn = tk.Button(search_frame, text="Search", font=("Arial", 16), command=self.search_files)
        self.search_btn.pack(side="left")

        list_frame = tk.Frame(self)
        list_frame.pack(side="top",pady=5,fill="both", expand=True)
        self.bar=tk.Scrollbar(list_frame, orient="vertical")
        self.list=tk.Listbox(list_frame,font=("Arail",16),yscrollcommand=self.bar.set)
        self.bar.config(command=self.list.yview)
        self.bar.pack(side="right", fill="y")
        self.list.pack(side="left", fill="both", expand=True)
        self.list.bind("<Double-Button-1>", self.open_in_explorer)
    def select_folder(self):
        folder_path = fd.askdirectory()
        self.selected_folder = folder_path
        self.path.config(text=f"Folder: {folder_path}", fg="black")
    def search_files(self):
        self.list.delete(0, "end") 
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        query = self.entry.get().strip().lower()
        found_count = 0
        for root, dirs, files in os.walk(self.selected_folder):
            for file in files:
                if not query or query in file.lower():
                    full_path = os.path.normpath(os.path.join(root, file))
                    self.list.insert("end", full_path)
                    found_count += 1
        if found_count == 0:
            messagebox.showinfo("Search", "No files found.")
    def open_in_explorer(self, event):
        selection = self.list.curselection()
        if not selection:
            return  
        file_path = self.list.get(selection[0])
        
        if os.path.exists(file_path):
            abs_path = os.path.abspath(file_path)
            subprocess.Popen(f'explorer.exe /select,"{abs_path}"')
class CalculatorModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = tk.Frame(self)
        header.pack(side="top", fill="x", pady=5)
        tk.Button(header, bg="Red", fg="White", text="X", font=("Arial", 14),
            command=lambda: show_module('UTILITIES', Button_Utilities)).pack(side="left")
        tk.Label(header, text="CALCULATOR", font=("Arial", 16, "bold")).pack(side="left", padx=10)

        self.display = tk.Entry(self, font=("Arial", 20), justify="right", bd=5, state="readonly")
        self.display.pack(fill="x", padx=10, pady=10)

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=10)
        buttons = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '⌫']
        ]

        for row_index, row in enumerate(buttons):
            for col_index, char in enumerate(row):
                btn = tk.Button(self.grid_frame, text=char, font=("Arial", 14), width=5, height=2,
                                command=lambda c=char: self.on_button_click(c))
                btn.grid(row=row_index, column=col_index, padx=3, pady=3)
    def on_button_click(self, char):
        self.display.config(state="normal")
        current_text = self.display.get()
        if char == 'C':
            self.display.delete(0, 'end')
        elif char == '⌫':
            if current_text:
                self.display.delete(len(current_text) - 1, 'end')
        elif char == '=':
            try:
                result = eval(current_text)
                self.display.delete(0, 'end')
                self.display.insert('end', str(result))
            except ZeroDivisionError:
                messagebox.showwarning("Error", "Cannot divide by zero!")
            except Exception:
                messagebox.showwarning("Error", "Invalid expression!")
        else:
            self.display.insert('end', char)
        self.display.config(state="readonly")
class EmojiModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = tk.Frame(self)
        header.pack(side="top", fill="x", pady=5)
        tk.Button(header, bg="Red", fg="White", text="X", font=("Arial", 14),
                  command=lambda: show_module('UTILITIES', Button_Utilities)).pack(side="left")
        tk.Label(header, text="EMOJI & SYMBOLS", font=("Arial", 16, "bold")).pack(side="left", padx=10)

        self.text_entry = tk.Entry(self, font=("Arial", 16))
        self.text_entry.pack(fill="x", padx=10, pady=10)

        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(pady=5)
        tk.Button(ctrl_frame, text="Copy to Clipboard", font=("Arial", 14), command=self.copy_to_clipboard).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="Clear", font=("Arial", 14), command=lambda: self.text_entry.delete(0, 'end')).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="⌫", font=("Arial", 14), command=self.backspace).pack(side="left", padx=5)

        grid_frame = tk.Frame(self)
        grid_frame.pack(pady=10)

        emojis = [
            ['😀', '😂', '😍', '😎', '😢'],
            ['👍', '👎', '❤️', '🔥', '✨'],
            ['★', '→', '€', '©', 'π'],
            ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        ]

        for row_index, row in enumerate(emojis):
            for col_index, char in enumerate(row):
                btn = tk.Button(grid_frame, text=char, font=("Arial", 16), width=4, height=2, command=lambda c=char: self.insert_symbol(c))
                btn.grid(row=row_index, column=col_index, padx=3, pady=3)

    def insert_symbol(self, char):
        self.text_entry.insert('end', char)

    def backspace(self):
        current_text = self.text_entry.get()
        if current_text:
            self.text_entry.delete(len(current_text) - 1, 'end')

    def copy_to_clipboard(self):
        text_to_copy = self.text_entry.get()
        if text_to_copy:
            self.clipboard_clear()
            self.clipboard_append(text_to_copy)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Field is empty!")
class UtilitiesModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Random Number", font=("Arial", 16, "bold")).pack(pady=(5, 2))

        num_frame = tk.Frame(self)
        num_frame.pack(pady=2)

        tk.Label(num_frame, text="Min:", font=("Arial", 16)).pack(side="left", padx=2)
        self.min_entry = tk.Entry(num_frame, width=6, font=("Arial", 16), justify="center")
        self.min_entry.insert(0, "1")
        self.min_entry.pack(side="left", padx=5)

        tk.Label(num_frame, text="Max:", font=("Arial", 16)).pack(side="left", padx=2)
        self.max_entry = tk.Entry(num_frame, width=6, font=("Arial", 16), justify="center")
        self.max_entry.insert(0, "100")
        self.max_entry.pack(side="left", padx=5)

        tk.Button(self, text="Generate Number", font=("Arial", 16), command=self.generate_number).pack(pady=5)
        self.num_result_label = tk.Label(self, text="Result: -", font=("Arial", 16, "bold"), fg="blue")
        self.num_result_label.pack(pady=2)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=15)

        tk.Button(self, text="Calculator", font=("Arial", 16), command=self.open_calculator).pack(pady=5)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=15)

        tk.Label(self, text="Coin Flip", font=("Arial", 16, "bold")).pack(pady=5)

        tk.Button(self, text="Flip Coin", font=("Arial", 16), command=self.flip_coin).pack(pady=5)
        self.coin_result_label = tk.Label(self, text="Result: -", font=("Arial", 16, "bold"), fg="green")
        self.coin_result_label.pack(pady=5)

        tk.Label(self, text="Random Choice", font=("Arial", 16, "bold")).pack(pady=(5, 2))

        tk.Label(self, text="Enter options (comma separated):", font=("Arial", 12)).pack(pady=2)
        self.choice_entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.choice_entry.pack(pady=5)

        tk.Button(self, text="Pick Random", font=("Arial", 16), command=self.pick_random).pack(pady=5)
        self.choice_result_label = tk.Label(self, text="Result: -", font=("Arial", 16, "bold"), fg="purple")
        self.choice_result_label.pack(pady=2)

        tk.Button(self, text="Emoji & Symbols", font=("Arial", 16), command=self.open_emoji_keyboard).pack(pady=5)

    def generate_number(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
            if min_val > max_val:
                messagebox.showwarning("Warning", "Min cannot be greater than Max!")
                return
            result = random.randint(min_val, max_val)
            self.num_result_label.config(text=f"Result: {result}")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numbers!")
    def open_calculator(self):
        for widget in main_content.winfo_children():
            widget.destroy()
        calc = CalculatorModule(main_content)
        calc.pack(fill="both", expand=True)
    def flip_coin(self):
        outcomes = ["Heads 🪙", "Tails 🪙"]
        result = random.choice(outcomes)
        self.coin_result_label.config(text=f"Result: {result}")
    def pick_random(self):
        raw_text = self.choice_entry.get()
        options = [item.strip() for item in raw_text.split(",") if item.strip()]
        if options: 
            choice=random.choice(options)
            self.choice_result_label.config(text=f"Result: {choice}")
        else:
            messagebox.showwarning("Warning", "Please enter options separated by commas!")
    def open_emoji_keyboard(self):
        for widget in main_content.winfo_children():
            widget.destroy()
        emoji_mod = EmojiModule(main_content)
        emoji_mod.pack(fill="both", expand=True)
root = tk.Tk()
root.title("Desktop Assistant app")
root.geometry("520x660")

Title = tk.Frame(root)
Title.pack(pady=10)
Title_label = tk.Label(Title, text = "Desktop Assistant",font = ("Arial", 20),)
Title_label.pack(pady=10)
sidebar = tk.Frame(root)
sidebar.pack(pady=10, padx =10, side="left", fill="y")
Button_TimeDate =tk.Button(sidebar,text = "Time & Date",font = ("Arial", 16),command=lambda: show_module('TIME & DATE',Button_TimeDate))
Button_TimeDate.pack(pady=10, padx =10, anchor="w")
Button_System =tk.Button(sidebar,text = "System",font = ("Arial", 16),command=lambda: show_module("SYSTEM",Button_System))
Button_System.pack(pady=10, padx =10, anchor="w")
Button_Files =tk.Button(sidebar,text = "Files",font = ("Arial", 16),command=lambda: show_module('FILES',Button_Files))
Button_Files.pack(pady=10, padx =10, anchor="w")
Button_Utilities =tk.Button(sidebar,text = "Utilities",font = ("Arial", 16),command=lambda: show_module('UTILITIES',Button_Utilities))
Button_Utilities.pack(pady=10, padx =10, anchor="w")
Button_Network =tk.Button(sidebar,text = "Network",font = ("Arial", 16),command=lambda: show_module('NETWORK',Button_Network))
Button_Network.pack(pady=10, padx =10, anchor="w")
Button_Notes =tk.Button(sidebar,text = "Notes",font = ("Arial", 16), command=lambda: show_module('NOTES',Button_Notes))
Button_Notes.pack(pady=10, padx =10, anchor="w")
main_content = tk.Frame(root)
main_content.pack(pady=10, padx=10, side="top", fill="both", expand=True)
content_label = tk.Label(main_content, text="Select a module",font=("Arial", 19),pady=10,anchor="center",)
content_label.pack(pady=10, padx=10, side="right", fill="both", expand=True)

root.mainloop()