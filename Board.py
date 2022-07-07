import os
import Path
import random
import tkinter
from functools import partial


class Board(tkinter.Frame):
    def __init__(self, root, board_size, mine_number, start_timer, stop_timer, set_mark_number, set_win, allow_question_marks):
        super().__init__(root)
        self.board_size = board_size
        self.mine_number = mine_number
        self.mine_list = list(list(0 for column in range(self.board_size[0])) for row in range(self.board_size[1]))
        self.visual_list = list(list("unopened" for column in range(self.board_size[0])) for row in range(self.board_size[1]))
        image_dir = Path.resource_path(os.path.normpath("./Images"))
        self.images = dict((image[:-4], tkinter.PhotoImage(file=os.path.join(image_dir, image))) for image in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, image)) and image.endswith(".png"))
        self.buttons = []
        self.number_list = []
        self.indexes = []
        self.mouse_buttons = [False, False]
        self.mark_counter = mine_number
        self.game_over = False
        self.first_click = False
        self.skip_press = False
        self.allow_question_marks = allow_question_marks
        self.start_func = start_timer
        self.stop_func = stop_timer
        self.win_func = set_win
        self.set_mark_func = set_mark_number
        for row in range(self.board_size[1]):
            temp_frame = tkinter.Frame(self)
            temp_frame.pack()
            self.buttons.append([])
            for column in range(self.board_size[0]):
                self.buttons[row].append(tkinter.Button(temp_frame, image=self.images["unopened"], highlightthickness=0, bd=0))
                self.buttons[row][column].pack(side="left")
                self.buttons[row][column].bind("<Button-1>", self.left_mouse_down)
                self.buttons[row][column].bind("<ButtonRelease-1>", partial(self.button_click, row, column))
                self.buttons[row][column].bind("<Button-3>", partial(self.mark_flag, row, column))
                self.buttons[row][column].bind("<ButtonRelease-3>", partial(self.right_mouse_up, row, column))
        self.choose_mines()

    def mark_flag(self, row, column, event=None):
        if not self.game_over:
            self.mouse_buttons[1] = True
            if self.mouse_buttons[0]:
                return None
            states = ("unopened", "mark", "unsure") if self.allow_question_marks else ("unopened", "mark")
            if self.visual_list[row][column] in states:
                if self.visual_list[row][column] == "unopened":
                    if self.mark_counter <= 0:
                        return None
                    else:
                        self.mark_counter -= 1
                elif self.visual_list[row][column] == "mark":
                    self.mark_counter += 1
                self.set_mark_func(self.mark_counter)
                self.visual_list[row][column] = states[(states.index(self.visual_list[row][column]) + 1) % len(states)]
                self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])

    def left_mouse_down(self, event=None):
        if not self.game_over:
            self.mouse_buttons[0] = True

    def right_mouse_up(self, row, column, event=None):
        if all(self.mouse_buttons):
            self.skip_press = True
            self.mouse_buttons[1] = False
            self.auto_open(row, column)
            return None
        self.mouse_buttons[1] = False
        if self.skip_press:
            self.skip_press = False

    def auto_open(self, row, column):
        if not self.visual_list[row][column] in (str(i) for i in range(1, 9)):
            return None
        flag_count = 0
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
            if self.visual_list[r][c] == "mark":
                flag_count += 1
        if self.visual_list[row][column] != str(flag_count):
            return None
        self.skip_press = False
        dead = False
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
            if self.visual_list[r][c] != "mark":
                self.button_click(r, c, skip_death=True)
                if self.mine_list[r][c]:
                    dead = True
                    self.visual_list[r][c] = "triggered mine"
                    self.buttons[r][c].config(image=self.images[self.visual_list[r][c]])
        if dead:
            self.death(None, None, skip_mark=True)
            return None
        count = 0
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                if self.visual_list[row][column] in ("unopened", "mark", "unsure"):
                    count += 1
        if count == self.mine_number:
            self.game_over = True
            self.win_func()

    def toggle_question_marks(self, state):
        self.allow_question_marks = state
        if not state:
            for row in range(self.board_size[1]):
                for column in range(self.board_size[0]):
                    if self.visual_list[row][column] == "unsure":
                        self.visual_list[row][column] = "unopened"
                        self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])

    def choose_mines(self):
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                self.indexes.append((row, column))
        for mine in range(self.mine_number):
            row, column = self.indexes.pop(random.randrange(len(self.indexes)))
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

    def relocate_first_mine(self, r, c):
        self.mine_list[r][c] = 0
        row, column = self.indexes.pop(random.randrange(len(self.indexes)))
        self.mine_list[row][column] = 1
        self.number_list.clear()
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

    def button_click(self, row, column, event=None, skip_death=False):
        if not self.first_click:
            self.first_click = True
            self.start_func()
            if self.mine_list[row][column]:
                self.relocate_first_mine(row, column)
        if all(self.mouse_buttons):
            self.skip_press = True
            self.mouse_buttons[0] = False
            self.auto_open(row, column)
            return None
        self.mouse_buttons[0] = False
        if self.skip_press:
            self.skip_press = False
            return None
        if (self.visual_list[row][column] != "unopened" and self.visual_list[row][column] != "unsure") or self.game_over:
            return None
        if self.mine_list[row][column]:
            if not skip_death:
                self.death(row, column)
                return None
        elif self.number_list[row][column]:
            self.visual_list[row][column] = str(self.number_list[row][column])
            self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
        else:
            self.visited = list(list(0 for c in range(self.board_size[0])) for r in range(self.board_size[1]))
            self.reveal(row, column)
        if not skip_death:
            count = 0
            for row in range(self.board_size[1]):
                for column in range(self.board_size[0]):
                    if self.visual_list[row][column] in ("unopened", "mark", "unsure"):
                        count += 1
            if count == self.mine_number:
                self.game_over = True
                self.win_func()

    def death(self, r, c, skip_mark=False):
        self.game_over = True
        self.stop_func()
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                if self.mine_list[row][column]:
                    if row == r and column == c:
                        if not skip_mark:
                            self.visual_list[row][column] = "triggered mine"
                            self.buttons[row][column].config(image=self.images[self.visual_list[row][column]])
                    elif self.visual_list[row][column] == "mark":
                        continue
                    else:
                        if not self.visual_list[row][column] == "triggered mine":
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
