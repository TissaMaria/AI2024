import numpy as np
import heapq

class PuzzleState:
    def __init__(self, board, zero_pos, moves=0, path=None):
        self.board = board
        self.zero_pos = zero_pos
        self.moves = moves
        self.heuristic = self.calculate_heuristic()
        self.path = path if path is not None else []

    def calculate_heuristic(self):
        """Calculate the number of misplaced tiles."""
        misplaced = 0
        target = 1  # The first tile should be 1
        for r in range(3):
            for c in range(3):
                value = self.board[r][c]
                if value != 0 and value != target:
                    misplaced += 1
                target += 1
        return misplaced

    def __lt__(self, other):
        return (self.moves + self.heuristic) < (other.moves + other.heuristic)

def get_neighbors(state):
    """Generate neighboring states by sliding tiles and log the actions."""
    neighbors = []
    r, c = state.zero_pos
    directions = [(0, 1, 'RIGHT'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (-1, 0, 'UP')]  # (dr, dc, action)

    for dr, dc, action in directions:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_board = np.copy(state.board)
            # Swap zero with the adjacent tile
            new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
            new_path = state.path + [action]  # Store the path taken
            neighbor_state = PuzzleState(new_board, (new_r, new_c), state.moves + 1, new_path)

            # Log the generated successor
            f_cost = neighbor_state.moves + neighbor_state.heuristic
            print(f"Generated successor by moving {action}:")
            print(neighbor_state.board)
            print(f"Successor cost (f = g + h): {f_cost} (Depth: {neighbor_state.moves}, Heuristic: {neighbor_state.heuristic})\n")
            neighbors.append(neighbor_state)

    return neighbors

def a_star(initial_board):
    """A* algorithm to solve the 8-puzzle."""
    zero_pos = tuple(np.argwhere(initial_board == 0)[0])  # Find the position of zero
    initial_state = PuzzleState(initial_board, zero_pos)

    open_set = []
    closed_set = set()
    heapq.heappush(open_set, initial_state)

    while open_set:
        current_state = heapq.heappop(open_set)

        # Print the state being expanded
        f_cost = current_state.moves + current_state.heuristic
        print("Expanding node with state:")
        print(current_state.board)
        print(f"Cost (f = g + h): {f_cost} (Depth: {current_state.moves}, Heuristic: {current_state.heuristic})\n")

        # Check if the current state is the goal state
        if np.array_equal(current_state.board, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])):
            print("Goal reached!")
            return current_state.moves, current_state.path  # Return the number of moves and path

        closed_set.add(tuple(map(tuple, current_state.board)))

        for neighbor in get_neighbors(current_state):
            if tuple(map(tuple, neighbor.board)) in closed_set:
                continue
            heapq.heappush(open_set, neighbor)

    return -1, []  # Return -1 if the puzzle is unsolvable

# Example usage:
initial_board = np.array([[1, 2, 3], [4, 0, 5], [7, 8, 6]])
moves, path = a_star(initial_board)

print(f'Solution path: {path}')
