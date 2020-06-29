


from tkinter import *
from queue import PriorityQueue

from cell import Cell
from priority import PriorityEntry



class CellGrid(Canvas):
    def __init__(self, master, side_length, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * side_length , height = cellSize * side_length, *args, **kwargs)

        self.master = master

        self.cellSize = cellSize
        self.side_length = side_length
        self.n_rows = side_length
        self.n_cols = side_length

        self.grid = []
        for row in range(self.n_rows):
            line = []
            for col in range(self.n_cols ):
                line.append(Cell(self, col, row, cellSize))
            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        # keep track of mouse clicks for selecting start/end/obstacle points
        self.mouse_clicks = 0

        self.found = False

        self.draw()


    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        # first click should select starting cell
        if self.mouse_clicks == 0:
            self.start_cell = cell
            self.start_cell.fill_color('green')
            self.start_cell.is_start = True
            self.mouse_clicks += 1 
        # second click should select end cell 
        elif self.mouse_clicks == 1:
            self.end_cell = cell
            self.end_cell.fill_color('red')
            self.end_cell.is_end = True
            self.mouse_clicks += 1 
        # any clicks after this should create obstacles 
        else:
            cell._switch()
            cell.draw()
            #add the cell to the list of cell switched during the click
            self.switched.append(cell)
            self.mouse_clicks += 1 

    def handleMouseMotion(self, event):
        # for click and drag, only pay attention when mouse clicks are >= 2 
        # since this is when the user is creating obstacles
        if self.mouse_clicks >= 2:
            row, column = self._eventCoords(event)
            cell = self.grid[row][column]

            if cell not in self.switched:
                cell._switch()
                cell.draw()
                self.switched.append(cell)
            self.mouse_clicks += 1


    def solve(self):
        # only go if the user has placed a start/end point and obstacles 
        if self.mouse_clicks >= 3:
            # self.recurse(self.start_cell)
            self.queue()


    def recurse(self, node, visited = set()):
        # this is DFS...
        # fill color so we know that we've visited this
        self.master.update()
        if node not in visited and not self.found:
            if node.is_end:
                print('Found')
                self.found = True
            visited.add(node)
            node.fill_color('grey')
            neighbors_idx = node.get_neighbors()
            for pos in neighbors_idx:
                sub_node = self.grid[pos[0]][pos[1]]
                self.recurse(sub_node, visited)


    def queue(self):

        visited = set()
        queue = PriorityQueue()
        final_path = []
        
        visited.add(self.start_cell)

        # dist_from_home = 0
        dist_to_goal = (self.end_cell.row - self.start_cell.row)**2 + (self.end_cell.col - self.start_cell.col)**2
        cost = dist_to_goal

        start = PriorityEntry(cost, self.start_cell)
        queue.put(start)

        while queue:
            self.master.update()
            node = queue.get().data
            
            neighbors = [self.grid[pos[0]][pos[1]] for pos in node.get_neighbors()]
            for neighbor in neighbors:
                if neighbor not in visited and not neighbor.is_obstacle:
                    # dist_from_home = (neighbor.row - self.start_cell.row)**2 + (neighbor.col - self.start_cell.col)**2
                    dist_to_goal = (self.end_cell.row - neighbor.row)**2 + (self.end_cell.col - neighbor.col)**2
                    cost = dist_to_goal
                    neighbor.parents.extend([node] + node.parents)
                    visited.add(neighbor)
                    queue.put(PriorityEntry(cost, neighbor))
                    node.fill_color('grey')
                    if node.is_end:
                        self.found = True
                        for cell in neighbor.parents:
                            cell.fill_color('blue')
                        print("Length of path found:", len(neighbor.parents), "cells")
                        return

        else:
            print("Path not found")
            return
        

