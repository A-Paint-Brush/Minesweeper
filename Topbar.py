import os
import Timer
import tkinter


class Topbar(tkinter.Frame):
    def __init__(self, root, mark_number, reset):
        super().__init__(root)
        self.root = root
        image_dir = os.path.normpath(".\\Images\\top bar")
        self.images = dict((image[:-4], tkinter.PhotoImage(file=os.path.join(image_dir, image))) for image in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, image)))
        self.timer_obj = Timer.Timer()
        self.timer_obj.reset()
        self.next_id = None
        self.game_over = False
        self.timer_str = "000"
        self.reset_func = reset
        self.mark_frame = tkinter.Frame(self)
        self.mark_display = list(tkinter.Label(self.mark_frame, bd=0, highlightthickness=0, image=self.images[i]) for i in str(mark_number).zfill(3))
        for i in self.mark_display:
            i.pack(side="left")
        self.mark_frame.pack(side="left")
        self.face_btn = tkinter.Button(self, image=self.images["smile"], bd=0, highlightthickness=0, command=self.reset)
        self.face_btn.pack(side="left", padx=5)
        self.timer_frame = tkinter.Frame(self)
        self.timer_display = list(tkinter.Label(self.timer_frame, bd=0, highlightthickness=0, image=self.images[self.timer_str[i]]) for i in range(3))
        for i in self.timer_display:
            i.pack(side="left")
        self.timer_frame.pack(side="left")

    def reset(self):
        self.game_over = True
        if self.next_id is not None:
            self.root.after_cancel(self.next_id)
        self.reset_func()

    def win(self):
        self.game_over = True
        if self.next_id is not None:
            self.root.after_cancel(self.next_id)
        self.face_btn.config(image=self.images["boss"])

    def start_o(self, event=None):
        if not self.game_over:
            self.face_btn.config(image=self.images["click"])

    def stop_o(self, event=None):
        if not self.game_over:
            self.face_btn.config(image=self.images["smile"])

    def set_mark_number(self, number):
        number = str(number).zfill(3)
        for i in range(3):
            self.mark_display[i].config(image=self.images[number[i]])

    def start_timer(self):
        self.timer_obj.reset()
        self.update_timer()

    def stop_timer(self):
        self.game_over = True
        if self.next_id is not None:
            self.root.after_cancel(self.next_id)
        self.face_btn.config(image=self.images["dead"])

    def update_timer(self):
        overflow = False
        time = round(self.timer_obj.get_time())
        if time >= 999:
            overflow = True
            time = 999
        self.timer_str = str(time).zfill(3)
        for i in range(3):
            self.timer_display[i].config(image=self.images[self.timer_str[i]])
        if not overflow:
            self.next_id = self.root.after(100, self.update_timer)
