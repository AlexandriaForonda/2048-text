from random import choice, choices
from copy import deepcopy
from enum import Enum
import numpy as np

BOARD_SIZE = 4


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


class Board:
    def __init__(self):
        self.tiles = []
        for _ in range(BOARD_SIZE):
            row = []
            for _ in range(BOARD_SIZE):
                row.append(0)
            self.tiles.append(row)
        self.spawn_tiles(2)


    def spawn_tiles(self, count=1):
        for _ in range(count):
            tile = 2 if choices([True, False], [0.75, 0.25])[0] else 4
            tile_pos = choice(self.__get_empty_positions())
            self.tiles[tile_pos[0]][tile_pos[1]] = tile


    def process_move(self, direction: Direction):
        if direction.value > 2:
            for i, row in enumerate(self.tiles):
                self.tiles[i] = reduce_row(row, direction)
        else:
            transposed_tiles = rotate_table(self.tiles)
            new_direction = Direction(direction.value + 2)
            for i, row in enumerate(transposed_tiles):
                transposed_tiles[i] = reduce_row(row, new_direction)
            self.tiles = rotate_table(transposed_tiles)


    def print(self):
        max_column_widths = []
        columns = rotate_table(self.tiles)
        for col in columns:
            max_column_widths.append(max([len(str(tile)) for tile in col]))
        for row in self.tiles:
            for i, tile in enumerate(row):
                tile = str(tile) if tile != 0 else "-"
                padding_amount = max_column_widths[i] - len(tile)
                print(tile + " " * padding_amount, end=" ")
            print()


    def __get_empty_positions(self):
        empty_positions = []
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile == 0:
                    empty_positions.append((i, j))
        return empty_positions


def rotate_table(table):
    return np.array(np.transpose(table)).tolist()


def merge_adjacent_tiles(row: list, direction: Direction):
    merged = deepcopy(row)
    i = 0
    if direction is Direction.Right: merged.reverse()
    while i < len(merged) - 1:
        current_tile = merged[i]
        neighbour = merged[i + 1]
        if current_tile == neighbour:
            merged[i] = current_tile + neighbour
            merged.pop(i + 1)
        i += 1
    if direction is Direction.Right: merged.reverse()
    return merged


def reduce_row(row: list, direction: Direction):
    number_tiles = [tile for tile in row if tile != 0]
    reduced = merge_adjacent_tiles(number_tiles, direction)
    filler_loc = 0 if direction is Direction.Right else len(reduced)
    while len(reduced) < BOARD_SIZE:
        reduced.insert(filler_loc, 0)
    return reduced


board = Board()
MOVE_DIRECTION = None
while True:
    try:
        board.print()
        MOVE_DIRECTION = Direction(int(input("\nMove: ")))
        board.process_move(MOVE_DIRECTION)
        board.spawn_tiles(1)
    except ValueError:
        print("Invalid move: 1 = up, 2 = down, 3 = left, 4 = right")
