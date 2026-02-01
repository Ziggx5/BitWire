from customtkinter import *
from client_modules.add_server import add_server_handler
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
        border_width = 1,
        corner_radius = 0
    )
    left_frame.place(x = 0, y = 100)
    left_frame.propagate(False)
    
    right_frame = CTkFrame(
        app,
        fg_color = "transparent",
        height = 600,
        width = 700,
        border_color = "#737373",
        border_width = 1,
        corner_radius = 0
    )
    right_frame.place(x = 200, y = 0)
    right_frame.propagate(False)

    upper_frame = CTkFrame(
        app,
        fg_color = "transparent",
        height = 50,
        width = 200,
        border_color = "#737373",
        border_width = 1,
        corner_radius = 0
    )
    upper_frame.place(x = 0, y = 50)
    upper_frame.propagate(False)

    server_placeholder_label = CTkLabel(
        upper_frame,
        text = "All servers"
    )
    server_placeholder_label.pack(side = "left", padx = 10)

    bitwire_label = CTkLabel(
        app,
        text = "BITWIRE",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    bitwire_label.place(x = 35, y = 10)

    add_new_server = CTkButton(
        upper_frame,
        text = "+",
        font = ("Courier New", 18, "bold"),
        width = 32,
        height = 32,
        fg_color = "#1f6feb",
        hover_color = "#388bfd",
        text_color = "#ffffff",
        corner_radius = 16,
        border_width = 0,
        command = lambda: add_server_handler(app, left_frame, right_frame, upper_frame, bitwire_label)
    )
    add_new_server.pack(side = "right", padx = 10)

    app.mainloop()