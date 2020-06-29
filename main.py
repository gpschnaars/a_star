
from tkinter import *

from GUI import CellGrid

def main():

    app = Tk()

    grid = CellGrid(app, 64, 20)
    grid.pack()

    start_button = Button(app, text = "Start", command = grid.solve)
    start_button.pack()

    app.mainloop()


if __name__ == '__main__':

    main()