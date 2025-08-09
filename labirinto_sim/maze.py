def load_maze(filename):
    maze = []
    start = None
    goal = None

    with open(filename, "r") as f:
        for y, line in enumerate(f.readlines()):
            row = []
            for x, char in enumerate(line.strip()):
                if char == "S":
                    start = (x, y)
                    row.append(" ")
                elif char == "G":
                    goal = (x, y)
                    row.append(" ")
                else:
                    row.append(char)
            maze.append(row)

    return maze, start, goal
