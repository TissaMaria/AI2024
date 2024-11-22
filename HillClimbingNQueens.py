
import random

def is_safe(board, row, col, n):
  for i in range(row):
    if board[i] == col or abs(board[i] - col) == row - i:
      return False
  return True

def calculate_cost(board, n):
  cost = 0
  for i in range(n):
    for j in range(i + 1, n):
      if abs(board[i] - board[j]) == abs(i - j):
        cost += 1
  return cost

def hill_climbing(n):
  board = list(range(n))
  random.shuffle(board)
  current_cost = calculate_cost(board, n)

  while True:
    best_neighbor = None
    best_neighbor_cost = current_cost

    for i in range(n):
      for j in range(n):
        if i != j:
          neighbor = list(board)
          neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
          neighbor_cost = calculate_cost(neighbor, n)
          if neighbor_cost < best_neighbor_cost:
            best_neighbor_cost = neighbor_cost
            best_neighbor = neighbor

    if best_neighbor is None or best_neighbor_cost >= current_cost:
      break

    board = best_neighbor
    current_cost = best_neighbor_cost

  return board

def print_board(board):
  n = len(board)
  for row in range(n):
    line = ""
    for col in range(n):
      if board[row] == col:
        line += "Q "
      else:
        line += ". "
    print(line)

n = 4
solution = hill_climbing(n)
print("Solution:")
print_board(solution)
print("Cost:", calculate_cost(solution, n))