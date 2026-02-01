from customtkinter import *

def start_ui():
    app = CTk()
    app.geometry("900x600")
    app.title("BitWire")
    app.resizable(False, False)
    app.configure(fg_color = "#0e1117")

    left_frame = CTkFrame(
        app,
        height = 500,
        fg_color = "transparent",
        border_color = "#737373",
        border_width = 1
    )
    left_frame.place(x = 0, y = 100)

    right_frame = CTkFrame(
        app,
        fg_color = "transparent",
        height = 600,
        width = 700,
        border_color = "#737373",
        border_width = 1
        
    )
    right_frame.place(x = 200, y = 0)

    server_placeholder_label = CTkLabel(left_frame, text = "All servers")
    server_placeholder_label.place(x = 10, y = 10)

    bitwire_label = CTkLabel(
        app,
        text = "BITWIRE",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    bitwire_label.place(x = 35, y = 10)

    add_new_server = CTkButton(
        app,
        text = "New connection",
        font = ("Courier New", 20),
        height = 50,
        width = 200
    )
    add_new_server.place(x = 0, y = 50)

    app.mainloop()