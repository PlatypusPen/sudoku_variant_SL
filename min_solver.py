from typing import List, Optional
from collections import defaultdict


def is_valid(board, row, col, num):
    # 检查行
    for i in range(9):
        if board[row][i] == num:
            return False
    # 检查列
    for i in range(9):
        if board[i][col] == num:
            return False
    # 检查 3x3 宫格
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def is_gw_valid(board, gw_cons_lists, r_gw_cons, row, col, num):
    if r_gw_cons is None:
        return True
    # 检查 German Whisper 约束

    if (row, col) not in r_gw_cons:
        return True  # 当前位置不在路径中，直接通过

    idxs = r_gw_cons[(row, col)]
    neighbors = []
    for cons_id, idx in idxs:
        if idx > 0:
            neighbors.append(gw_cons_lists[cons_id][idx - 1])
        if idx < len(gw_cons_lists[cons_id]) - 1:
            neighbors.append(gw_cons_lists[cons_id][idx + 1])

    for nx, ny in neighbors:
        x, y = nx - 1, ny - 1
        val = board[x][y]
        if val != 0 and abs(val - num) < 5:
            return False
    return True


def solve_sudoku(board, gw_cons_lists=None):
    r_gw_cons = rev_gw(gw_cons_lists)
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num) and is_gw_valid(
                        board, gw_cons_lists, r_gw_cons, row, col, num
                    ):
                        board[row][col] = num
                        if solve_sudoku(board, gw_cons_lists):
                            return True
                        board[row][col] = 0
                return False
    return True


def rev_gw(gw_cons_lists):
    if gw_cons_lists is None:
        return None
    # 反转 German Whisper 约束列表
    r_gw_cons = defaultdict(list)
    for i, cons_list in enumerate(gw_cons_lists):
        for j, (x, y) in enumerate(cons_list):
            r_gw_cons[(x - 1, y - 1)].append((i, j))
    return r_gw_cons


def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))


# 示例：一个待解的数独谜题
sudoku_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 2, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 5, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 8, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

from testyaml import parse_line
import yaml
with open('test.yaml', 'r') as f:
    data = yaml.safe_load(f)
    gw_cons_lists = [parse_line(nodes) for nodes in data['german_whisper']]

if solve_sudoku(sudoku_board, gw_cons_lists):
    print("解出的数独如下：")
    print_board(sudoku_board)
else:
    print("没有可行解。")
