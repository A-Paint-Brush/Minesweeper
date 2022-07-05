import tkinter
import tkinter.messagebox as msg
import Help
import Custom
# TODO: Function on clicking both mouse buttons at the same time
# TODO: Bug testing
# TODO: Write README file


class Menu(tkinter.Menu):
    def __init__(self, root, reset_game):
        super().__init__(root)
        self.root = root
        self.reset_game = reset_game
        game_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New{}F2".format(" " * 25), command=self.reset_game)
        game_menu.add_separator()
        self.options = (("Beginner", (8, 8), 10), ("Intermediate", (16, 16), 40), ("Expert", (30, 16), 99))
        self.board_size = tkinter.IntVar()
        self.custom_option = None
        self.prev_opt = 0
        for index, option in enumerate(self.options):
            game_menu.add_radiobutton(label=option[0], value=index, variable=self.board_size, command=self.option_confirm)
        game_menu.add_radiobutton(label="Custom", value=3, variable=self.board_size, command=self.launch_custom_dialog)
        self.board_size.set(0)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        self.help_menu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Help Topics", command=self.launch_help_dialog)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.about)

    def launch_help_dialog(self):
        self.help_menu.entryconfigure(0, state="disabled")
        Help.Help(self.root, self.close_help_dialog)

    def launch_custom_dialog(self):
        Custom.Dialog(self.root, self.set_custom_option, self.cancel_custom_option, self.options[self.prev_opt][1:] if self.custom_option is None else self.custom_option)

    def close_help_dialog(self):
        self.help_menu.entryconfigure(0, state="normal")

    def option_confirm(self):
        self.prev_opt = self.board_size.get()
        self.custom_option = None
        self.reset_game()

    def get_option(self):
        return self.options[self.board_size.get()][1:]

    def set_custom_option(self, data):
        self.custom_option = data
        self.reset_game()

    def check_if_custom(self):
        if self.custom_option is None:
            return False
        else:
            return True

    def get_custom_option(self):
        return self.custom_option

    def cancel_custom_option(self):
        if self.custom_option is None:
            self.board_size.set(self.prev_opt)

    def about(self):
        msg.showinfo("Minesweeper", "This is a recreation of the Windows 95 Minesweeper written in Python.", master=self.root)
