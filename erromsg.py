import ctypes

class msg:
    def error(title, text, style):
        ctypes.windll.user32.MessageBoxW(0, text, title, 0)