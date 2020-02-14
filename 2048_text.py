import numpy as np
from random import choice, choices
from copy import deepcopy
from enum import Enum
from console.screen import sc
from console import utils

BOARD_SIZE = 4


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


# Switches the rows and columns of a table
def rotate_table(table):
    return np.array(np.transpose(table)).tolist()


# Merges adjacent tiles from a row with the same value in
# the specified direction (left or right)
# e.g. [2, 2, 4, 4] merged Left ==> [4, 8]
# e.g. [8, 8, 8, 16] merged Right ==> [8, 16, 16]
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


# Moves and merges tiles from a row in the specified direction
def reduce_row(row: list, direction: Direction):
    # Tiles with no value are ignored when merging, as numbered tiles
    # simply move across them
    number_tiles = [tile for tile in row if tile != 0]
    reduced = __merge_adjacent_tiles(number_tiles, direction)
    # The 0's are then added back to restore the row to the size of the
    # board. They are placed at either the start or end of the row.
    filler_loc = 0 if direction is Direction.Right else len(reduced)
    while len(reduced) < BOARD_SIZE:
        reduced.insert(filler_loc, 0)
    return reduced


# Decides whether a row can be reduced (i.e. tiles can be either
# moved or merged)
def reducible(row: list):
    if 0 in row:
        return True
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            return True
    return False


# Represents the game board holding the tiles.
# It's size is adjustable using the BOARD_SIZE constant (default is 4)
class Board:
    def __init__(self):
        self.tiles = []
        # Initialises the board with empty values
        for _ in range(BOARD_SIZE):
            row = []
            for _ in range(BOARD_SIZE):
                row.append(0)
            self.tiles.append(row)
        self.spawn_tiles(2)


    # Returns a list of the positions on the board not occupied by
    # numbered tiles
    def __get_empty_positions(self):
        empty_positions = []
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile == 0:
                    empty_positions.append((i, j))
        return empty_positions


    # Spawns a specified number of tiles in random positions.
    # Tiles of value '2' have a 75% chance of spawning compared to a
    # 25% chance for '4' tiles
    def spawn_tiles(self, count=1):
        for _ in range(count):
            tile = 2 if choices([True, False], [0.75, 0.25])[0] else 4
            tile_pos = choice(self.__get_empty_positions())
            self.tiles[tile_pos[0]][tile_pos[1]] = tile


    # Reorders the tiles in the board based on a player move
    def process_move(self, direction: Direction):
        if direction.value > 2: # Left or Right
            # Reduces each row
            for i, row in enumerate(self.tiles):
                self.tiles[i] = reduce_row(row, direction)
        else:
            # If the direction of the player move is vertical (Up or Down),
            # the tiles are 'rotated' (the columns become the rows)
            # The new 'rows' are then reduced, before the board is rotated
            # back to normal
            transposed_tiles = rotate_table(self.tiles)
            # Up ==> Left, Down ==> Right
            new_direction = Direction(direction.value + 2)
            for i, row in enumerate(transposed_tiles):
                transposed_tiles[i] = reduce_row(row, new_direction)
            self.tiles = rotate_table(transposed_tiles)


    # Decides if there are any reducible rows or columns left in the board.
    # If this returns False, the player has lost
    def is_reducible(self):
        all_rows = self.tiles + rotate_table(self.tiles)
        return any(reducible(row) for row in all_rows)


    def __str__(self):
        # The longest item in each column is used to calculate the padding
        # between tiles when printing
        max_column_widths = []
        columns = rotate_table(self.tiles)
        for col in columns:
            max_column_widths.append(max([len(str(tile)) for tile in col]))
        output = ""
        for row in self.tiles:
            for i, tile in enumerate(row):
                tile = str(tile) if tile != 0 else "-"
                padding_amount = max_column_widths[i] - len(tile)
                output += tile + " " * (padding_amount + 1)
            output += "\n"
        return output


CONTROLS = {
    "w": Direction.Up,
    "a": Direction.Left,
    "s": Direction.Down,
    "d": Direction.Right
}

board = Board()

# Runs until the player cannot make any more moves
while board.is_reducible():
    utils.cls()
    print(board)
    move_direction = CONTROLS.get(input("\nMove: ").lower())
    if move_direction is None:
        continue
    # The values of the tiles are saved before a move is processed, then
    # compared to the board state afterwards. If these are equal (meaning that
    # no 'move' has actually occured), then a new tile isn't spawned
    last_tiles = deepcopy(board.tiles)
    board.process_move(move_direction)
    if board.tiles != last_tiles:
        board.spawn_tiles(1)
print(f"Game over! Your best tile was {np.amax(board.tiles)}.")
