


class Cell():
    FILLED_COLOR_BG = "black"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, col, row, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.col = col
        self.row = row
        self.size = size
        self.fill = False
        # designate whether this cell is an obstacle
        self.is_obstacle = False
        # create attributes designating start/end cells
        self.is_start = False
        self.is_end = False

        self.parents = []

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill
        self.is_obstacle = not self.is_obstacle

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None and not self.immutable:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.col * self.size
            xmax = xmin + self.size
            ymin = self.row * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)


    def fill_color(self, color):
        if not self.immutable: 
            xmin = self.col * self.size
            xmax = xmin + self.size
            ymin = self.row * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = color, outline = 'black')

    @property
    def immutable(self):
        return self.is_start or self.is_end

    def get_neighbors(self):
        # given self's col/row indices, return the indices of neighbors
        # excludes diagonals
        max_len = self.master.side_length
        # # non-diagonals
        # combos = ((self.row - 1, self.col),
        #         (self.row, self.col + 1),
        #         (self.row + 1, self.col),
        #         (self.row, self.col - 1))

        # including diagonals 
        combos = ((self.row  - 1, self.col - 1),
                (self.row  - 1, self.col),
                (self.row  - 1, self.col + 1),
                (self.row , self.col + 1),
                (self.row  + 1, self.col + 1),
                (self.row  + 1, self.col),
                (self.row  + 1, self.col - 1),
                (self.row , self.col - 1))
        return [item for item in combos if all(0<=i<max_len for i in item)]


