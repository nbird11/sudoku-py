# Sudoku

## Description

A simple terminal sudoku game written python. I created this game in a university class and decided I wanted to add some more features.

## Features

### Original

Original requirements for full credit in the university class.

- Load sudoku game files.
  - Sudoku game files are in json format.
  - Save your game to a file.
- In-terminal ascii game rendering (printing)
- Coordinate input
  - Invalid input: Recognize if the user types something other than a coordinate or the letter 'Q' to quit
  - Reversed coordinates: Handle both "B2" and "2B" in the same way
  - Lowercase coordinates: Handle both "B2" and "b2" in the same way
  - Invalid number: Warn the user if an invalid number such as 0 or 11 is entered into the board
  - Square already filled: Warn the user if the selected square already has a number
  - Row checking: Recognize if the user's number is already present on the selected row
  - Column checking: Recognize if the user's number is already present on the selected column
  - Box checking: Recognize if the user's number is already present on the selected inside square

### Planned/Possible

New stuff that I want to add.

- QoL Save/Load
  - ~~"Continue where you left off" option that loads the file that was last loaded.~~
  - ~~Save your game to a new file or the same file you loaded from.~~
  - Tkinter or other file browser for save/load
- Tkinter gui
- Turn into web app?
- Option to create a new sudoku puzzle
  - Choose difficulty
    - Easy
    - Medium
    - Hard
- Sudoku solver
  - Provide hints
    - Box hint
    - Row hint
    - Column hint

## Author

Nathan Bird  
[nathanbirdka@gmail.com](mailto:nathanbirdka@gmail.com)
