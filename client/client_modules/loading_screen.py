from customtkinter import *
from client_modules.ui import start_ui

progress_value = 0.0
def start_loading_screen():
    app = CTk()
    app.overrideredirect(True)
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"200x250+{x}+{y}")
    app.title("BitWire")
    app.resizable(False, False)
    app.configure(fg_color = "#0e1117")

    loading_frame = CTkFrame(app, fg_color = "transparent")
    loading_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    bitwire_label = CTkLabel(
        loading_frame,
        text = "BITWIRE",
        text_color = "#a5a8ad",
        font = ("Courier New", 20)
    )
    bitwire_label.pack(pady = (0, 10))

    line_frame = CTkFrame(
        loading_frame,
        width = 100,
        height = 2,
        fg_color = "#2554a1"
    )
    line_frame.pack(pady = (0, 10))

    progress_bar = CTkProgressBar(
        loading_frame,
        width = 80,
        progress_color = "#4f87e3",
    )
    progress_bar.pack(pady = 10)
    progress_bar.set(0)

    loading_label = CTkLabel(
        loading_frame,
        text = "Loading...",
        text_color = "#a5a8ad",
        font = ("Courier New", 10)
    )
    loading_label.pack()

    def update_progress():
        global progress_value
        if progress_value < 1.0:
            progress_value += 0.01
            progress_bar.set(progress_value)
            app.after(20, update_progress)
        else:
            progress_bar.set(1.0)
            loading_label.configure(
                text = "Success!"
            )
            app.after(1000, finish)
    
    def finish():
        app.destroy()
        start_ui()

    update_progress()
    app.mainloop()


