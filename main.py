import os
import Menu
import Board
import Topbar
import tkinter


class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.resolution = None
        self.min_resolution = (245, 245)
        self.title("Minesweeper")
        self.resizable(False, False)
        self.iconbitmap(os.path.normpath(".\\Images\\icon\\Icon.ico"))
        self.top_bar = None
        self.board = None
        self.menu = Menu.Menu(self, self.reset_game)
        self.config(menu=self.menu)
        self.init_game(False)
        self.bind("<F2>", self.reset_game)
        self.mainloop()

    def init_game(self, custom_size):
        option = self.menu.get_custom_option() if custom_size else self.menu.get_option()
        self.resolution = [16 * (option[0][0] if custom_size else option[1][0]) + 20, 16 * (option[0][1] if custom_size else option[1][1]) + 54]
        if self.resolution[0] < self.min_resolution[0]:
            self.resolution[0] = self.min_resolution[0]
        if self.resolution[1] < self.min_resolution[1]:
            self.resolution[1] = self.min_resolution[1]
        self.geometry("{}x{}".format(*self.resolution))
        self.top_bar = Topbar.Topbar(self, option[1] if custom_size else option[2], self.reset_game, "Custom" if custom_size else option[0])
        self.top_bar.pack(pady=5)
        if custom_size:
            self.board = Board.Board(self, *option, self.start_timer, self.stop_timer, self.set_mark_number, self.win)
        else:
            self.board = Board.Board(self, option[1], option[2], self.start_timer, self.stop_timer, self.set_mark_number, self.win)
        self.board.pack()
        self.bind("<Button-1>", self.top_bar.start_o)
        self.bind("<ButtonRelease-1>", self.top_bar.stop_o)

    def start_timer(self):
        self.top_bar.start_timer()

    def stop_timer(self):
        self.top_bar.stop_timer()

    def set_mark_number(self, number):
        self.top_bar.set_mark_number(number)

    def win(self):
        self.top_bar.win()

    def reset_game(self, event=None):
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")
        self.top_bar.stop_timer()
        self.top_bar.destroy()
        self.board.destroy()
        self.init_game(self.menu.check_if_custom())


if __name__ == "__main__":
    Window()
