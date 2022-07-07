import os
import Path
import tkinter
try:
    import winsound
    sound = True
except ImportError:
    sound = False


class Dialog(tkinter.Toplevel):
    def __init__(self, root, set_custom_opt, cancel_custom_opt, prev_conf):
        super().__init__(root)
        self.resolution = (340, 100)
        self.title("Custom Field")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        self.iconbitmap(Path.resource_path(os.path.normpath("./Images/icon/Icon.ico")))
        self.root = root
        self.ok_func = set_custom_opt
        self.cancel_func = cancel_custom_opt
        self.height_var = tkinter.StringVar()
        self.width_var = tkinter.StringVar()
        self.mine_var = tkinter.StringVar()
        self.validate_cmd = self.register(self.check_keypress)
        content_frame = tkinter.Frame(self)
        left_pane = tkinter.Frame(content_frame)
        row1 = tkinter.Frame(left_pane)
        tkinter.Label(row1, text="Height:", width=10).pack(side="left")
        tkinter.Entry(row1, textvariable=self.height_var, width=15, validate="key", validatecommand=(self.validate_cmd, "%P")).pack(side="left")
        row1.pack(pady=5)
        row2 = tkinter.Frame(left_pane)
        tkinter.Label(row2, text="Width:", width=10).pack(side="left")
        tkinter.Entry(row2, textvariable=self.width_var, width=15, validate="key", validatecommand=(self.validate_cmd, "%P")).pack(side="left")
        row2.pack(pady=5)
        row3 = tkinter.Frame(left_pane)
        tkinter.Label(row3, text="Mines:", width=10).pack(side="left")
        tkinter.Entry(row3, textvariable=self.mine_var, width=15, validate="key", validatecommand=(self.validate_cmd, "%P")).pack(side="left")
        row3.pack(pady=5)
        left_pane.pack(side="left")
        right_pane = tkinter.Frame(content_frame)
        self.ok_btn = tkinter.Button(right_pane, text="OK", width=10, command=self.ok)
        self.ok_btn.pack(pady=5)
        self.cancel_btn = tkinter.Button(right_pane, text="Cancel", width=10, command=self.cancel)
        self.cancel_btn.pack()
        right_pane.pack(side="left", padx=10)
        content_frame.pack()
        self.height_var.set(prev_conf[0][1])
        self.width_var.set(prev_conf[0][0])
        self.mine_var.set(prev_conf[1])
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()
        self.focus()

    def check_keypress(self, p):
        if p.isdigit() or (not len(p)):
            return True
        else:
            if sound:
                winsound.MessageBeep(winsound.MB_ICONHAND)
            return False

    def ok(self):
        height = int(self.height_var.get() or 0)
        width = int(self.width_var.get() or 0)
        mines = int(self.mine_var.get() or 0)
        if height < 8:
            height = 8
        if width < 8:
            width = 8
        if mines < 10:
            mines = 10
        if height > 24:
            height = 24
        if width > 30:
            width = 30
        if mines > (width - 1) * (height - 1):
            mines = (width - 1) * (height - 1)
        self.ok_func(((width, height), mines))
        self.destroy()

    def cancel(self):
        self.destroy()
        self.cancel_func()
