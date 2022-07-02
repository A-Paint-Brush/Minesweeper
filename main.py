import tkinter
import Board
import Topbar


class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.resolution = (245, 245)
        self.title("Minesweeper")
        self.geometry("{}x{}".format(*self.resolution))
        self.resizable(False, False)
        self.top_bar = None
        self.board = None
        self.init_game()
        self.mainloop()

    def init_game(self):
        self.top_bar = Topbar.Topbar(self, self.reset_game)
        self.top_bar.pack(pady=5)
        self.board = Board.Board(self, (8, 8), 10, self.start_timer, self.stop_timer, self.set_mark_number)
        self.board.pack()
        self.bind("<Button-1>", self.top_bar.start_o)
        self.bind("<ButtonRelease-1>", self.top_bar.stop_o)

    def start_timer(self):
        self.top_bar.start_timer()

    def stop_timer(self):
        self.top_bar.stop_timer()

    def set_mark_number(self, number):
        self.top_bar.set_mark_number(number)

    def reset_game(self):
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")
        self.top_bar.destroy()
        self.board.destroy()
        self.init_game()


if __name__ == "__main__":
    Window()
