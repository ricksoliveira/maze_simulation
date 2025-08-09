import heapq

def a_star(start, goal, maze):
    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    open_set = [(0 + heuristic(start, goal), 0, start, [])]
    visited = set()

    while open_set:
        _, cost, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        path = path + [current]

        if current == goal:
            return path

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] == " ":
                neighbor = (nx, ny)
                if neighbor not in visited:
                    heapq.heappush(open_set, (cost+1+heuristic(neighbor, goal), cost+1, neighbor, path))

    return None
