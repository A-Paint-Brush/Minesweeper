import os
import json
import tkinter
import tkinter.ttk
import tkinter.messagebox as msg


def ensure_exists():
    if not os.path.isfile(os.path.normpath(".\\Minesweeper.json")):
        try:
            file = open(os.path.normpath(".\\Minesweeper.json"), "w", encoding="utf8")
            data = {"score": {"Beginner": ["Anonymous", 999], "Intermediate": ["Anonymous", 999], "Expert": ["Anonymous", 999]}}
            file.write(json.dumps(data, indent=4))
            file.close()
        except (IOError, OSError):
            return -1
        else:
            return 0
    else:
        return 1


def read_scores():
    try:
        file = open(os.path.normpath(".\\Minesweeper.json"), "r", encoding="utf8")
        data = json.loads(file.read())
        file.close()
    except (IOError, OSError, json.decoder.JSONDecodeError):
        data = "Error reading data file."
    finally:
        return data


def compare_score(difficulty, timer):
    if ensure_exists() == -1:
        return None
    else:
        data = read_scores()
        if isinstance(data, str):
            return None
        else:
            return timer < data["score"][difficulty][1]


class ScoreBoard(tkinter.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.resolution = (400, 140)
        self.title("Best Times")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        self.iconbitmap(os.path.normpath(".\\Images\\icon\\Icon.ico"))
        self.root = root
        self.content_frame = None
        self.show_data()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.grab_set()
        self.focus()

    def show_data(self):
        error = False
        self.content_frame = tkinter.Frame(self)
        if ensure_exists() == -1:
            error = True
            tkinter.Label(self.content_frame, text="Error creating data file.").pack()
        else:
            data = read_scores()
            if isinstance(data, str):
                error = True
                tkinter.Label(self.content_frame, text=data).pack()
            else:
                tkinter.Label(self.content_frame, text="Fastest Mine Sweepers").pack(anchor="w", padx=(20, 0))
                tkinter.ttk.Separator(self.content_frame, orient="horizontal").pack(fill="x", pady=5)
                for difficulty in ("Beginner", "Intermediate", "Expert"):
                    tkinter.Label(self.content_frame, font="TkFixedFont", text="%-13s   %3d seconds   %s" % (
                    difficulty + ":", data["score"][difficulty][1], data["score"][difficulty][0])).pack(anchor="w",
                                                                                                        padx=(20, 0))
        button_row = tkinter.Frame(self.content_frame)
        if not error:
            tkinter.Button(button_row, text="Reset Scores", width=12, command=self.reset_scores).pack(side="left", padx=(0, 5))
        tkinter.Button(button_row, text="OK", width=12, command=self.close_window).pack(side="left")
        button_row.pack(anchor="e", padx=(0, 10), pady=(15, 0))
        self.content_frame.pack(expand=True, fill="both")

    def reset_scores(self):
        try:
            if os.path.isfile(os.path.normpath(".\\Minesweeper.json")):
                os.remove(os.path.normpath(".\\Minesweeper.json"))
        except (IOError, OSError):
            msg.showerror("Error", "Failed to reset scores.", parent=self)
        finally:
            self.content_frame.destroy()
            self.show_data()

    def close_window(self):
        self.destroy()
        self.root.deiconify()


class NameDialog(tkinter.Toplevel):
    def __init__(self, root, difficulty, timer, return_func):
        super().__init__(root)
        self.resolution = (280, 115)
        self.title("Congratulations")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        self.iconbitmap(os.path.normpath(".\\Images\\icon\\Icon.ico"))
        self.difficulty = difficulty
        self.timer = timer
        self.return_func = return_func
        self.root = root
        self.name_var = tkinter.StringVar()
        self.validate_cmd = self.register(self.check_keypress)
        content_frame = tkinter.Frame(self)
        tkinter.Label(content_frame, justify="left", text="You have the fastest time for {}\nlevel. Please type your name:".format(self.difficulty)).pack(anchor="w", padx=(10, 0))
        entry = tkinter.Entry(content_frame, textvariable=self.name_var, width=36, validate="key", validatecommand=(self.validate_cmd, "%P"))
        entry.pack(pady=10)
        tkinter.Button(content_frame, text="OK", width=12, command=self.update_score).pack(anchor="e", padx=(0, 10))
        content_frame.pack(expand=True, fill="both")
        self.name_var.set("Anonymous")
        entry.focus()
        entry.selection_range(0, "end")
        entry.icursor("end")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.grab_set()
        self.focus()

    def check_keypress(self, p):
        return len(p) <= 20

    def update_score(self):
        error = False
        name = self.name_var.get().strip()
        data = read_scores()
        if isinstance(data, str):
            error = True
            msg.showerror("Error", "Failed to save your high score.", parent=self)
            self.close_window(error)
        else:
            data["score"][self.difficulty] = [name, self.timer]
            try:
                file = open(os.path.normpath(".\\Minesweeper.json"), "w", encoding="utf8")
                file.write(json.dumps(data, indent=4))
                file.close()
            except (IOError, OSError):
                error = True
                msg.showerror("Error", "Failed to save your high score.", parent=self)
            finally:
                self.close_window(error)

    def close_window(self, return_code=None):
        self.destroy()
        self.root.deiconify()
        if return_code is not None:
            self.return_func(return_code)
