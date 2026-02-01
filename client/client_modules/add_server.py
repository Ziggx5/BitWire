from customtkinter import *

def add_server_handler(app, left_frame, right_frame, upper_frame, bitwire_label):
    left_frame.place_forget()
    right_frame.place_forget()
    upper_frame.place_forget()
    bitwire_label.place_forget()

    add_server_frame = CTkFrame(
        app,
        height = 400,
        width = 600,
        fg_color = "transparent",
        border_color = "#737373",
        border_width = 1,
        corner_radius = 5
    )
    add_server_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

