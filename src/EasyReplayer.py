import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from pynput import mouse, keyboard
import pydirectinput
import time
import threading
import os

class EasyReplayer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EasyReplayer v1.0")
        self.geometry("450x420") 
        
        # Path configuration (points to the 'actions' folder at root level)
        self.actions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions"))
        if not os.path.exists(self.actions_dir):
            os.makedirs(self.actions_dir)
        
        # Logical variables
        self.recording = False
        self.replaying = False
        self.stop_replay_flag = False
        self.recorded_actions = []
        self.start_time = 0
        self.loop_var = tk.BooleanVar(value=False) # Loop flag
        
        # Listeners for recording
        self.mouse_listener = None
        self.kb_stop_listener = None

        self.setup_ui()
        
        # Global hotkey listener
        self.hotkey_listener = keyboard.Listener(on_press=self.on_global_key)
        self.hotkey_listener.start()

    def setup_ui(self):
        # Allow the root window column to stretch responsibly
        self.grid_columnconfigure(0, weight=1)
        
        # --- Header Title ---
        self.header = ctk.CTkLabel(self, text="EasyReplayer Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=20)

        # --- Recording Section ---
        self.record_frame = ctk.CTkFrame(self)
        self.record_frame.pack(fill="x", padx=20, pady=10)
        
        # Configure column weights: stretch middle column(1), keep sides fixed
        self.record_frame.grid_columnconfigure(0, weight=0)
        self.record_frame.grid_columnconfigure(1, weight=1)
        self.record_frame.grid_columnconfigure(2, weight=0)

        # Unified label width to ensure colon alignment
        ctk.CTkLabel(self.record_frame, text="Filename:", width=80, anchor="e").grid(row=0, column=0, padx=(15, 5), pady=15, sticky="e")
        self.filename_entry = ctk.CTkEntry(self.record_frame, placeholder_text="actions", width=140)
        self.filename_entry.insert(0, "actions")
        self.filename_entry.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        # Fixed button width
        self.record_btn = ctk.CTkButton(self.record_frame, text="Record (R)", 
                                        fg_color="#E74C3C", hover_color="#C0392B", width=110,
                                        command=self.toggle_record)
        self.record_btn.grid(row=0, column=2, padx=(5, 15), pady=15, sticky="e")

        # --- Replay Section ---
        self.replay_frame = ctk.CTkFrame(self)
        self.replay_frame.pack(fill="x", padx=20, pady=10)
        
        # Keep identical column weights as the top frame
        self.replay_frame.grid_columnconfigure(0, weight=0)
        self.replay_frame.grid_columnconfigure(1, weight=1)
        self.replay_frame.grid_columnconfigure(2, weight=0)

        # Unified label width
        ctk.CTkLabel(self.replay_frame, text="Select File:", width=80, anchor="e").grid(row=0, column=0, padx=(15, 5), pady=15, sticky="e")
        self.file_combo = ctk.CTkComboBox(self.replay_frame, values=self.get_file_list(), width=140)
        self.file_combo.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        # Fixed button width
        self.replay_btn = ctk.CTkButton(self.replay_frame, text="Replay (P)", 
                                        fg_color="#2ECC71", hover_color="#27AE60", width=110,
                                        command=self.start_replay_thread)
        self.replay_btn.grid(row=0, column=2, padx=(5, 15), pady=15, sticky="e")

        # --- Speed Adjustment ---
        ctk.CTkLabel(self.replay_frame, text="Speed:", width=80, anchor="e").grid(row=1, column=0, padx=(15, 5), pady=10, sticky="e")
        self.speed_scale = ctk.CTkSlider(self.replay_frame, from_=0.1, to=5.0, 
                                         command=self.update_speed_label)
        self.speed_scale.set(1.0)
        # Allow the slider to fill all remaining middle space
        self.speed_scale.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        
        self.speed_label = ctk.CTkLabel(self.replay_frame, text="1.0x", width=110, anchor="center")
        self.speed_label.grid(row=1, column=2, padx=(5, 15), pady=10)

        # --- Loop Switch ---
        self.loop_check = ctk.CTkCheckBox(self.replay_frame, text="Enable Infinite Loop Mode", 
                                          variable=self.loop_var)
        self.loop_check.grid(row=2, column=0, columnspan=3, pady=(15, 10))

        # --- Status Bar ---
        self.status_label = ctk.CTkLabel(self, text="System Ready", text_color="#3498DB")
        self.status_label.pack(pady=(15, 5))
        
        ctk.CTkLabel(self, text="Tip: Press 'Esc' key during recording or replaying to stop immediately", 
                     font=ctk.CTkFont(size=11), text_color="gray").pack(pady=5)

    # --- Helper Functions ---
    def get_file_list(self):
        try:
            files = [f for f in os.listdir(self.actions_dir) if f.endswith(".txt")]
            return files if files else ["No record files"]
        except Exception:
            return ["No record files"]

    def update_speed_label(self, value):
        self.speed_label.configure(text=f"{value:.1f}x")

    def on_global_key(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char.lower() == 'r' and not self.recording and not self.replaying:
                    self.after(0, self.toggle_record)
                elif key.char.lower() == 'p' and not self.recording and not self.replaying:
                    self.after(0, self.start_replay_thread)
        except: pass

    # --- Recording Logic ---
    def toggle_record(self):
        if not self.recording:
            self.recording = True
            self.recorded_actions = []
            self.start_time = time.time()
            self.record_btn.configure(text="Stop (Esc)", fg_color="#95A5A6")
            self.status_label.configure(text="● Recording...", text_color="#E74C3C")
            
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.kb_stop_listener = keyboard.Listener(on_press=self.on_interrupt_press)
            self.mouse_listener.start()
            self.kb_stop_listener.start()
        else:
            self.stop_record()

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            elapsed = round(time.time() - self.start_time, 3)
            self.recorded_actions.append(("click", x, y, elapsed))

    def on_interrupt_press(self, key):
        if key == keyboard.Key.esc:
            if self.recording:
                self.after(0, self.stop_record)
            if self.replaying:
                self.stop_replay_flag = True
            return False 

    def stop_record(self):
        if self.recording:
            self.recording = False
            if self.mouse_listener: self.mouse_listener.stop()
            
            self.record_btn.configure(text="Record (R)", fg_color="#E74C3C")
            filename = self.filename_entry.get().strip() or "actions"
            if not filename.endswith(".txt"): filename += ".txt"
            
            filepath = os.path.join(self.actions_dir, filename)
            with open(filepath, "w") as f:
                for act in self.recorded_actions:
                    f.write(f"{act[0]},{act[1]},{act[2]},{act[3]}\n")
            
            self.status_label.configure(text=f"Saved successfully: {filename}", text_color="#3498DB")
            self.file_combo.configure(values=self.get_file_list())

    # --- Replay Logic ---
    def start_replay_thread(self):
        if self.recording or self.replaying: return
        filename = self.file_combo.get()
        filepath = os.path.join(self.actions_dir, filename)
        
        if filename == "No record files" or not os.path.exists(filepath):
            messagebox.showwarning("Warning", "Please record first or select a valid file")
            return

        self.replaying = True
        self.stop_replay_flag = False
        threading.Thread(target=self.run_replay, args=(filepath,), daemon=True).start()

    def run_replay(self, filepath):
        speed = self.speed_scale.get()
        
        with keyboard.Listener(on_press=self.on_interrupt_press) as listener:
            try:
                # Loop control structure
                while True:
                    self.status_label.configure(text=f"▶ Replaying ({speed:.1f}x)...", text_color="#2ECC71")
                    with open(filepath, "r") as f:
                        actions = f.readlines()
                    
                    last_time = 0
                    for line in actions:
                        if self.stop_replay_flag: break
                        
                        parts = line.strip().split(',')
                        if len(parts) < 4: continue
                        
                        act_type, x, y, timestamp = parts
                        x, y, timestamp = int(float(x)), int(float(y)), float(timestamp)

                        wait_time = (timestamp - last_time) / speed
                        if wait_time > 0:
                            # Stepwise wait segmentation
                            steps = int(wait_time / 0.05)
                            for _ in range(steps):
                                if self.stop_replay_flag: break
                                time.sleep(0.05)
                            if not self.stop_replay_flag:
                                time.sleep(wait_time % 0.05)

                        if not self.stop_replay_flag and act_type == "click":
                            pydirectinput.moveTo(x, y)
                            pydirectinput.click()
                        
                        last_time = timestamp

                    # Check if loop continuation is requested
                    if self.stop_replay_flag or not self.loop_var.get():
                        break
                    else:
                        self.status_label.configure(text="▶ Looping: preparing next replay...", text_color="#2ECC71")
                        time.sleep(0.5) # Slight interval between loops

                if self.stop_replay_flag:
                    self.status_label.configure(text="Replay interrupted by user", text_color="#F1C40F")
                else:
                    self.status_label.configure(text="Replay finished successfully", text_color="#3498DB")

            except Exception as e:
                print(f"Error: {e}")
                self.status_label.configure(text="An error occurred during replay", text_color="red")
            
            self.replaying = False
            self.stop_replay_flag = False