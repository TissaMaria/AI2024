#Manhattan
import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0):
        self.state = state          # Current state of the board
        self.parent = parent        # Parent node for path tracking
        self.action = action        # Move taken to reach this state
        self.depth = depth          # Depth of the node in the search tree
        self.cost = cost            # Total cost (f = g + h) for A* search

    def __lt__(self, other):
        return self.cost < other.cost

def get_manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(goal.index(state[i][j]), 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def generate_successors(state):
    moves = []
    x, y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]

    directions = {
        "UP": (x - 1, y),
        "DOWN": (x + 1, y),
        "LEFT": (x, y - 1),
        "RIGHT": (x, y + 1)
    }

    for action, (new_x, new_y) in directions.items():
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            moves.append((action, new_state))
    return moves

def a_star_search(initial, goal):
    goal_flat = sum(goal, [])
    start = PuzzleNode(initial, cost=get_manhattan_distance(initial, goal_flat))
    frontier = []
    heapq.heappush(frontier, start)
    explored = set()

    while frontier:
        current = heapq.heappop(frontier)

        # Display current state and cost
        print("Expanding node with state:")
        for row in current.state:
            print(row)
        print(f"Cost (f = g + h): {current.cost} (Depth: {current.depth}, Heuristic: {current.cost - current.depth})\n")

        if current.state == goal:
            path = []
            while current.parent:
                path.append(current.action)
                current = current.parent
            print("Goal reached!\n")
            return path[::-1]  # Return reversed path from start to goal

        explored.add(tuple(map(tuple, current.state)))

        for action, state in generate_successors(current.state):
            if tuple(map(tuple, state)) in explored:
                continue

            depth = current.depth + 1
            cost = depth + get_manhattan_distance(state, goal_flat)
            child = PuzzleNode(state, current, action, depth, cost)

            # Display successor info
            print(f"Generated successor by moving {action}:")
            for row in state:
                print(row)
            print(f"Successor cost (f = g + h): {cost} (Depth: {depth}, Heuristic: {cost - depth})\n")

            heapq.heappush(frontier, child)

    print("No solution found.")
    return None  # Return None if no solution is found

# Example usage
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solution = a_star_search(initial_state, goal_state)
if solution:
    print("Solution path:", solution)
else:
    print("No solution could be found.")
