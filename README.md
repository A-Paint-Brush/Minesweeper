# Minesweeper

A recreation of the Windows 95 Minesweeper written in Python.

![Minesweeper Screenshot](https://user-images.githubusercontent.com/96622265/177537807-56537f96-fa31-414c-967c-ac4cdb99857b.png)

### Installation Instructions

Just place the executable into any directory you like, and then make a shortcut to it on the desktop. I recommend you don't place the executable on the desktop because the executable generates a save file in its working directory, so if you put it there the save file will also be visible on the desktop.

### Rules and Instructions

Click on a square to reveal a portion of the minefield. Some revealed squares will have a number in them, this number represents the number of mines that the 8 surrounding squares contains. Use these numbers to judge where the mines are. If you click on a square that contains a mine, you lose. You can place a flag to mark a square as a mine by right-clicking. Flagged squares do not open when clicked, so you can use this to prevent yourself from accidentally clicking on a square that you already know is a mine. Right-clicking a second time will change the flag to a question mark, which do open when clicked. Right-clicking a third time turns the square empty again. If you have already marked the mines around a numbered square, you can quickly open all the unmarked squares by pressing both the left and right mouse button on the numbered square at the same time and letting go. Open all non-mine squares to win the game.

You can change the size of the board by choosing a different difficulty option in the "Game" option of the application menu. You can also set a custom board size by choosing the "Custom" option. After winning or losing a game, restart the game by either clicking the yellow face button, pressing F2, or clicking "Game" -> "New" in the application menu.

### Credits

The images were taken from the original game, but the code is all written by me.
