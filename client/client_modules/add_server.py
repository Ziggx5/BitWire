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
    add_server_frame.grid_propagate(False)

    add_server_label = CTkLabel(
        add_server_frame,
        text = "Add server",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    add_server_label.grid(row = 0, column = 0, pady = 30, padx = 30)

    server_nickname_label = CTkLabel(
        add_server_frame,
        text = "Server name:",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    server_nickname_label.grid(row = 1, column = 0, pady = 10, padx = 10)

    server_nickname_entry = CTkEntry(
        add_server_frame,
        font = ("Courier New", 30),
        height = 40,
        width = 200
    )
    server_nickname_entry.grid(row = 1, column = 1, pady =  10, padx = 10)

    server_ip_label = CTkLabel(
        add_server_frame,
        text = "Server address:",
        text_color = "#a5a8ad",
        font = ("Courier New", 30)
    )
    server_ip_label.grid(row = 2, column = 0, pady = 10, padx = 10)

    server_ip_entry = CTkEntry(
        add_server_frame,
        font = ("Courier New", 30),
        height = 40,
        width = 200
    )
    server_ip_entry.grid(row = 2, column = 1, pady = 10, padx = 10)

    cancel_button = CTkButton(
        add_server_frame,
        font = ("Courier New", 30),
        text = "Cancel",
        height = 40,
        width = 60,
        command = lambda: exit_add_server(app, left_frame, right_frame, upper_frame, bitwire_label, add_server_frame)
    )
    cancel_button.grid(row = 4, column = 0, pady = (100,0))

    confirm_button = CTkButton(
        add_server_frame,
        font = ("Courier New", 30),
        text = "Confirm",
        height = 40,
        width = 60
    )
    confirm_button.grid(row = 4, column = 1, pady = (100,0))

def exit_add_server(app, left_frame, right_frame, upper_frame, bitwire_label, add_server_frame):
    add_server_frame.destroy()
    left_frame.place(x = 0, y = 100)
    right_frame.place(x = 200, y = 0)
    upper_frame.place(x = 0, y = 50)
    bitwire_label.place(x = 35, y = 10)


