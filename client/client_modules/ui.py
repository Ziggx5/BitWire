from customtkinter import *

def start_ui():
    app = CTk()
    app.geometry("900x600")
    app.title("BitWire")
    app.resizable(False, False)
    app.configure(fg_color = "#0e1117")

    bitwire_label = CTkLabel(
        app,
        text = "BITWIRE",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    bitwire_label.place(x = 30, y = 10)

    add_new_server = CTkButton(
        app,
        text = "New connection",
        font = ("Courier New", 20),
        height = 50,
        width = 200
    )
    add_new_server.place(x = 0, y = 50)

    left_frame = CTkFrame(
        app,
        fg_color = "red",
        height = 500
    )
    left_frame.place(x = 0, y = 100)

    lol_label = CTkLabel(left_frame, text = "lal")
    lol_label.place(x = 10, y = 10)

    app.mainloop()