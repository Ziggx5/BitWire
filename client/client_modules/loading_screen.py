from customtkinter import *

progress_value = 0.0

def start_loading_screen(app):
    loading_frame = CTkFrame(app, fg_color = "transparent")
    loading_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    bitwire_label = CTkLabel(
        loading_frame,
        text = "B I T W I R E",
        text_color = "#a5a8ad",
        font = ("Courier New", 70)
    )
    bitwire_label.pack()

    line_frame = CTkFrame(
        loading_frame,
        width = 400,
        height = 2,
        fg_color = "#2554a1"
    )
    line_frame.pack()

    subtitle_label = CTkLabel(
        loading_frame,
        text = "Secure messaging",
        text_color = "#a5a8ad",
        font = ("Courier New", 20)
    )
    subtitle_label.pack(pady = 20)

    progress_bar = CTkProgressBar(
        loading_frame,
        width = 300,
        progress_color = "#4f87e3",
        determinate_speed = 0.4
    )
    progress_bar.pack(pady = 30)
    progress_bar.set(0)

    def update_progress():
        global progress_value
        if progress_value < 1.0:
            progress_value += 0.01
            progress_bar.set(progress_value)
            progress_bar.after(20, update_progress)
        else:
            progress_bar.set(1.0)
            print("dela")
    update_progress()


