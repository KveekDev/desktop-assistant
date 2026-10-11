# 🖥️ Desktop Assistant

A lightweight, modular desktop assistant application built using **Python** and **Tkinter**. This project was created as part of a Python learning journey utilizing project-based development and clean object-oriented architecture (`tk.Frame`).

---

## 🚀 Features

The application features a responsive multi-module sidebar interface:

1. **🕒 Time & Date**
   - Real-time digital clock with timezone support (using `zoneinfo`).
   - Built-in **Stopwatch & Timer** sub-module with precise state management and cancellation handlers (`after_cancel`).

2. **📊 System Monitor**
   - Real-time CPU, RAM, and Disk usage tracking powered by `psutil`.
   - Visual progress indicators (`ttk.Progressbar`).

3. **📁 File Manager & Search**
   - Directory selection dialogs.
   - Recursive file search using `os.walk()`.
   - Direct integration with Windows Explorer to locate and highlight files (`subprocess.Popen`).

4. **🛠️ Utilities**
   - **Random Generator:** Number generator (Min/Max range), Coin Flip, and Random Choice picker.
   - **Calculator:** A grid-based arithmetic calculator with error handling (`eval`, `ZeroDivisionError`) and locked manual keyboard input (`state="readonly"`).
   - **Emoji & Symbols Keyboard:** Quick clipboard copying tool for special characters and emojis.

---

## 🛠️ Built With

- **Language:** Python 3.x
- **GUI Framework:** `tkinter`, `ttk`
- **Libraries:** `psutil`, `datetime`, `zoneinfo`, `subprocess`, `random`, `os`

---

## 📦 Status
This project is Discontinued and will not be finished in near future.
