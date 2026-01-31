from customtkinter import *

def start_ui():
    app = CTk()
    app.geometry("900x600")
    app.title("BitWire")
    app.resizable(False, False)
    app.configure(fg_color = "#0e1117")

    app.mainloop()