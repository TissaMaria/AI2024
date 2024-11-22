

import random
import math

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


def simulated_annealing(n):
  board = list(range(n))
  random.shuffle(board)

  temperature = 1.0
  cooling_rate = 0.995

  current_cost = calculate_cost(board, n)

  while temperature > 0.0001 :
    neighbor = list(board)
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)

    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

    neighbor_cost = calculate_cost(neighbor, n)
    delta_e = neighbor_cost - current_cost

    if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / temperature):
      board = neighbor
      current_cost = neighbor_cost
    temperature *= cooling_rate
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

n = 16
solution = simulated_annealing(n)
print("Solution:")
print_board(solution)
print("Cost:",calculate_cost(solution,n))
