import platform
os = platform.system()

if os == "Windows":
    # WINDOWS
    import ctypes
    import win32gui
    def get_foreground_window():
        user32 = ctypes.windll.user32
        handle = user32.GetForegroundWindow()
        window_title = win32gui.GetWindowText(handle)
        return window_title

    active_window = get_foreground_window()
    print(f"Active Window Title: {active_window}")
elif os == "Linux":
    # LINUX 
    import subprocess
    def get_foreground_window():
        active_window_id = subprocess.check_output(["xdotool", "getactivewindow"]).strip()
        window_name = subprocess.check_output(["xdotool", "getwindowname", active_window_id]).strip()
        return window_name.decode("utf-8")

    active_window = get_foreground_window()
    print(f"Active Window: {active_window}")
