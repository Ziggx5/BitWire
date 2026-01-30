from customtkinter import *
from client_modules.loading_screen import start_loading_screen

def start_ui():
    app = CTk()
    app.geometry("900x600")
    app.title("BitWire")
    app.resizable(False, False)
    app.configure(fg_color = "#0e1117")

    start_loading_screen(app)


    app.mainloop()