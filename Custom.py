import tkinter
import tkinter.messagebox as msg


class Dialog(tkinter.Toplevel):
    def __init__(self, root, set_custom_opt, cancel_custom_opt):
        super().__init__(root)
        self.resolution = (340, 100)
        self.title("Custom Field")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        self.root = root
        self.ok_func = set_custom_opt
        self.cancel_func = cancel_custom_opt
        self.height_var = tkinter.StringVar()
        self.width_var = tkinter.StringVar()
        self.mine_var = tkinter.StringVar()
        content_frame = tkinter.Frame(self)
        left_pane = tkinter.Frame(content_frame)
        row1 = tkinter.Frame(left_pane)
        tkinter.Label(row1, text="Height:", width=10).pack(side="left")
        tkinter.Entry(row1, textvariable=self.height_var, width=15).pack(side="left")
        row1.pack(pady=5)
        row2 = tkinter.Frame(left_pane)
        tkinter.Label(row2, text="Width:", width=10).pack(side="left")
        tkinter.Entry(row2, textvariable=self.width_var, width=15).pack(side="left")
        row2.pack(pady=5)
        row3 = tkinter.Frame(left_pane)
        tkinter.Label(row3, text="Mines:", width=10).pack(side="left")
        tkinter.Entry(row3, textvariable=self.mine_var, width=15).pack(side="left")
        row3.pack(pady=5)
        left_pane.pack(side="left")
        right_pane = tkinter.Frame(content_frame)
        self.ok_btn = tkinter.Button(right_pane, text="OK", width=10, command=self.ok)
        self.ok_btn.pack(pady=5)
        self.cancel_btn = tkinter.Button(right_pane, text="Cancel", width=10, command=self.cancel)
        self.cancel_btn.pack()
        right_pane.pack(side="left", padx=10)
        content_frame.pack()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()

    def ok(self):
        width = self.width_var.get()
        height = self.height_var.get()
        mines = self.mine_var.get()
        if width.isdigit() and height.isdigit() and mines.isdigit() and width != "0" and height != "0" and mines != "0":
            data = ((int(self.width_var.get()), int(self.height_var.get())), int(self.mine_var.get()))
            self.ok_func(data)
            self.destroy()
        else:
            self.ok_btn.config(state="disabled")
            self.cancel_btn.config(state="disabled")
            msg.showwarning("Error", "Invalid input.", master=self)
            self.ok_btn.config(state="normal")
            self.cancel_btn.config(state="normal")

    def cancel(self):
        self.destroy()
        self.cancel_func()
