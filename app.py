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


    def __get_empty_positions(self):
        empty_positions = []
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile == 0:
                    empty_positions.append((i, j))
        return empty_positions


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


    def is_reducible(self):
        all_rows = self.tiles + rotate_table(self.tiles)
        return any(reducible(row) for row in all_rows)


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


def rotate_table(table):
    return np.array(np.transpose(table)).tolist()


def __merge_adjacent_tiles(row: list, direction: Direction):
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
    reduced = __merge_adjacent_tiles(number_tiles, direction)
    filler_loc = 0 if direction is Direction.Right else len(reduced)
    while len(reduced) < BOARD_SIZE:
        reduced.insert(filler_loc, 0)
    return reduced


def reducible(row: list):
    if 0 in row:
        return True
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            return True
    return False


CONTROLS = {
    "w": Direction.Up,
    "a": Direction.Left,
    "s": Direction.Down,
    "d": Direction.Right
}

print("Welcome to 2048 text!")
BOARD = Board()
BOARD.print()
while BOARD.is_reducible():
    move_direction = CONTROLS.get(input("\nMove: ").lower())
    if move_direction is None:
        print("Invalid move! Use the WASD keys to move the tiles.")
        continue
    last_tiles = deepcopy(BOARD.tiles)
    BOARD.process_move(move_direction)
    if BOARD.tiles != last_tiles:
        BOARD.spawn_tiles(1)
    BOARD.print()
print(f"Game over! Your best tile was {np.amax(BOARD.tiles)}.")
