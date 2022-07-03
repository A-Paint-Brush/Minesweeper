import os
import tkinter


class Help(tkinter.Toplevel):
    def __init__(self, root, exit_func):
        super().__init__(root)
        self.exit_func = exit_func
        self.resolution = (280, 245)
        self.title("Minesweeper")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        scrollbar = tkinter.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        text = tkinter.Text(self, yscrollcommand=scrollbar.set, wrap="word", font=("simhei", 12, "normal"))
        text.pack(expand=True, fill="both")
        scrollbar.config(command=text.yview)
        text.insert("end", self.get_help_text())
        text.config(state="disabled")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def get_help_text(self):
        try:
            file = open(os.path.normpath(".\\Data\\Help.txt"), "r", encoding="utf8")
            text = file.read()
            file.close()
            return text
        except (IOError, OSError):
            return "Error loading help file."

    def close_window(self):
        self.destroy()
        self.exit_func()
