# 🎮 EasyReplayer v1.0

A lightweight, automated macro recording and playback assistant built with Python, CustomTkinter, and PyDirectInput. It is specifically designed to simulate mouse and keyboard inputs across **3D video games** and standard Win32 desktop applications, turning tedious, repetitive tasks into flawless single-click automation.

> 💡 **Why EasyReplayer?** > Most standard mouse recorders fail in 3D games because modern game engines utilize DirectInput/Raw Input, causing the game camera to spin uncontrollably or ignore clicks completely. EasyReplayer utilizes `pydirectinput` and forces Windows Administrative privileges (UAC) to bypass these barriers, ensuring your macros land exactly where they should.

---

## 📁 Project Structure

```text
EasyReplayer/
│
├── actions/             # Directory where recorded .txt macro files are saved/read
├── src/
│   ├── EasyReplayer.py  # Core GUI design and event processing logic
│   └── main.py          # Application entry point (handles admin verification)
└── README.md            # Documentation

```

---

## 🚀 Core Features

* **Built for 3D Games & Core Engines**
Uses DirectX-compatible input emulation to seamlessly automate tasks, farming routines, or camera movements inside modern 3D games without input rejection.
* **Universal Task Automation**
Perfect for grinding, clicker games, stress-testing interfaces, or handling any mundane desktop workflow requiring aggressive, repeated clicking.
* **Dynamic Alignment GUI**
A clean, scannable, and modern responsive user interface designed using CustomTkinter Dark Mode.
* **Global Background Hotkeys**
Trigger or cancel recordings completely hands-free from outside the app interface (`R` to record, `P` to replay, `Esc` to instantly terminate via safety-switch).
* **Adaptive Execution Throttle**
Speed up sluggish workflows or slow down precise routines by scaling playback speeds smoothly from `0.1x` to `5.0x`.
* **Automatic Admin UAC Elevation**
Automatically detects your system privileges on launch and hooks into Windows UAC to ensure the macro injector can interact with high-privilege applications and games.

---

## 🛠️ Prerequisites & Installation

To run the project from its raw source code, install the required dependencies using `pip`:

```bash
pip install customtkinter pynput pydirectinput

```

---

## 📖 How to Use

1. **Launch the App** Run `main.py` inside the `src` folder and accept the Windows UAC administrative pop-up prompt.
2. **Recording Macros** Type a recognizable file name, click **Record (R)** (or press your global `R` key), and perform your routine. Hit **Esc** when finished. Your macro will be safely archived into the `/actions` directory.
3. **Replaying Macros** Select your macro from the dropdown, slide to your ideal speed modifier, toggle infinite loop preferences if desired, and click **Replay (P)** (or press your global `P` key).

```

```
