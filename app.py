from random import choice, choices
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
            for row in self.tiles:
                reduce_row(row, direction)
        else:
            transposed_tiles = rotate_table(self.tiles)
            new_direction = Direction(direction.value + 2)
            for row in transposed_tiles:
                reduce_row(row, new_direction)
            self.tiles = rotate_table(transposed_tiles)


    # FIXME
    def print(self):
        for row in self.tiles:
            for tile in row:
                print(tile if tile != 0 else "-", end=" ")
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
    i = 0
    if direction is Direction.Right: row.reverse()
    while i < len(row) - 1:
        current_tile = row[i]
        neighbour = row[i + 1]
        if current_tile == neighbour:
            row[i] = current_tile + neighbour
            row.pop(i + 1)
        i += 1
    if direction is Direction.Right: row.reverse()


# TODO Find out if anything changed from the original list;
# if not, the board should not spawn a tile
def reduce_row(row: list, direction: Direction):
    row[:] = [tile for tile in row if tile != 0]
    merge_adjacent_tiles(row, direction)
    filler_loc = 0 if direction is Direction.Right else len(row)
    while len(row) < BOARD_SIZE:
        row.insert(filler_loc, 0)


board = Board()

# TODO End game when tile spawn is impossible
while True:
    board.print()
    move = int(input("\nMove: "))
    board.process_move(Direction(move))
    board.spawn_tiles(1)
