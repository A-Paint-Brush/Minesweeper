import os
import random
import tkinter
from functools import partial


class Board(tkinter.Frame):
    def __init__(self, root, board_size, mine_number, start_timer, stop_timer, set_mark_number):
        super().__init__(root)
        self.board_size = board_size
        self.mine_number = mine_number
        self.mine_list = list(list(0 for column in range(self.board_size[0])) for row in range(self.board_size[1]))
        self.visual_list = list(list("unopened" for column in range(self.board_size[0])) for row in range(self.board_size[1]))
        image_dir = os.path.normpath(".\\Images")
        self.images = dict((image[:-4], tkinter.PhotoImage(file=os.path.join(image_dir, image))) for image in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, image)))
        self.buttons = []
        self.number_list = []
        self.mark_counter = 10
        self.gameover = False
        self.first_click = False
        self.start_func = start_timer
        self.stop_func = stop_timer
        self.set_mark_func = set_mark_number
        for row in range(self.board_size[1]):
            temp_frame = tkinter.Frame(self)
            temp_frame.pack()
            self.buttons.append([])
            for column in range(self.board_size[0]):
                self.buttons[row].append(tkinter.Button(temp_frame, image=self.images["unopened"], highlightthickness=0, bd=0, command=partial(self.button_click, row, column)))
                self.buttons[row][column].pack(side="left")
                self.buttons[row][column].bind("<Button-3>", partial(self.mark_flag, row, column))
        self.choose_mines()

    def mark_flag(self, row, column, event=None):
        if not self.gameover:
            states = ("unopened", "mark", "unsure")
            if self.visual_list[row][column] in states:
                if self.visual_list[row][column] == "unopened":
                    if self.mark_counter <= 0:
                        return None
                    else:
                        self.mark_counter -= 1
                elif self.visual_list[row][column] == "mark":
                    self.mark_counter += 1
                self.set_mark_func(self.mark_counter)
                self.visual_list[row][column] = states[(states.index(self.visual_list[row][column]) + 1) % 3]
                self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])

    def choose_mines(self):
        indexes = []
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                indexes.append((row, column))
        for mine in range(self.mine_number):
            row, column = indexes.pop(random.randrange(len(indexes)))
            self.mine_list[row][column] = 1
        for row in range(self.board_size[1]):
            self.number_list.append([])
            for column in range(self.board_size[0]):
                self.number_list[row].append(0)
                if self.mine_list[row][column]:
                    continue
                for r, c in ((row - 1, column),
                             (row - 1, column + 1),
                             (row, column + 1),
                             (row + 1, column + 1),
                             (row + 1, column),
                             (row + 1, column - 1),
                             (row, column - 1),
                             (row - 1, column - 1)):
                    if r < 0 or r >= self.board_size[1] or c < 0 or c >= self.board_size[0]:
                        continue
                    if self.mine_list[r][c]:
                        self.number_list[row][column] += 1

    def button_click(self, row, column):
        if not self.first_click:
            self.first_click = True
            self.start_func()
        if (self.visual_list[row][column] != "unopened" and self.visual_list[row][column] != "unsure") or self.gameover:
            return None
        if self.mine_list[row][column]:
            self.game_over(row, column)
        elif self.number_list[row][column]:
            self.visual_list[row][column] = str(self.number_list[row][column])
            self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
        else:
            self.visited = list(list(0 for c in range(self.board_size[0])) for r in range(self.board_size[1]))
            self.reveal(row, column)

    def game_over(self, r, c):
        self.gameover = True
        self.stop_func()
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                if self.mine_list[row][column]:
                    if row == r and column == c:
                        self.visual_list[row][column] = "triggered mine"
                        self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
                    else:
                        self.visual_list[row][column] = "revealed mine"
                        self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
                else:
                    if self.visual_list[row][column] == "mark":
                        self.visual_list[row][column] = "incorrect mark"
                        self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])

    def reveal(self, row, column):
        if self.visited[row][column] or row < 0 or row >= self.board_size[1] or column < 0 or column >= self.board_size[0]:
            return None
        if self.mine_list[row][column]:
            return None
        self.visited[row][column] = 1
        for r, c in ((row - 1, column), (row - 1, column + 1), (row, column + 1), (row + 1, column + 1), (row + 1, column), (row + 1, column - 1), (row, column - 1), (row - 1, column - 1)):
            if r < 0 or r >= self.board_size[1] or c < 0 or c >= self.board_size[0]:
                continue
            if self.number_list[r][c] == 0:
                self.reveal(r, c)
            else:
                if not self.visited[r][c]:
                    self.visited[r][c] = 1
                    self.visual_list[r][c] = str(self.number_list[r][c])
                    self.buttons[r][c].config(image=self.images[self.visual_list[r][c]])
        self.visual_list[row][column] = "0"
        self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
