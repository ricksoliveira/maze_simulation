import random
from pathfinding import a_star

class Agent:
    def __init__(self, start, goal, maze):
        self.pos = start
        self.goal = goal
        self.maze = maze
        self.path = []

    def move_random(self):
        x, y = self.pos
        options = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        random.shuffle(options)
        for nx, ny in options:
            if self._valid(nx, ny):
                self.pos = (nx, ny)
                return

    def move_directed(self):
        path = a_star(self.pos, self.goal, self.maze)
        if path and len(path) > 1:
            self.pos = path[1]

    def _valid(self, x, y):
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0]) and self.maze[y][x] == " "

    def reached_goal(self):
        return self.pos == self.goal
