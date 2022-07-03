import tkinter
import tkinter.messagebox as msg
# TODO: Win detection
# TODO: Add custom board size window
# TODO: Bug testing
# TODO: Write README file
# FIXME: Window is too small for title to fit in title bar


class Menu(tkinter.Menu):
    def __init__(self, root, reset_game):
        super().__init__(root)
        game_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New{}F2".format(" " * 25), command=reset_game)
        game_menu.add_separator()
        self.options = (("Beginner", (8, 8), 10), ("Intermediate", (16, 16), 40), ("Expert", (30, 16), 99))
        self.board_size = tkinter.IntVar()
        for index, option in enumerate(self.options):
            game_menu.add_radiobutton(label=option[0], value=index, variable=self.board_size, command=reset_game)
        self.board_size.set(0)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)
        help_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)

    def get_option(self):
        return self.options[self.board_size.get()][1:]

    def about(self):
        msg.showinfo("Minesweeper", "This is a recreation of the Windows 95 Minesweeper written in Python.")
