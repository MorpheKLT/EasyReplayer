import sys
import ctypes
import customtkinter as ctk
from EasyReplayer import EasyReplayer

# Initialize CustomTkinter styling configs globally
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # Check for administrator privileges
    if is_admin():
        # Run application normally if privileges exist
        app = EasyReplayer()
        app.mainloop()
    else:
        # Re-run the program with admin privileges requested
        # 'runas' triggers the Windows Account Access prompt screen dialog box
        print("Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)