import random
import enum
from copy import deepcopy


class Direction(enum.Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


def merge_adjacent_tiles(tiles, direction):
    merged = deepcopy(tiles)
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


def reduce_row(row, direction):
    number_tiles = [tile for tile in row if tile != 0]
    reduced = merge_adjacent_tiles(number_tiles, direction)
    filler_loc = 0 if direction is Direction.Right else len(reduced)
    while len(reduced) < 4:
        reduced.insert(filler_loc, 0)
    return reduced


class Board:
    def __init__(self):
        self.__gen_starting_tiles()
        for _ in range(2):
            self.spawn_new_tile()


    # TODO Give 2 a greater probability of spawning?
    def spawn_new_tile(self):
        tile_val = 2 if random.choice([True, False]) else 4
        tile_pos = random.choice(self.__get_empty_positions())
        self.tiles[tile_pos[0]][tile_pos[1]] = tile_val


    def fmt_print(self):
        for row in self.tiles:
            for col in row:
                print("-" if col == 0 else col, end=" ")
            print("")


    def __get_empty_positions(self):
        empty_positions = []
        for i, _ in enumerate(self.tiles):
            for j, _ in enumerate(self.tiles[i]):
                if self.tiles[i][j] == 0:
                    empty_positions.append((i, j))
        return empty_positions


    def __gen_starting_tiles(self):
        self.tiles = []
        for _ in range(4):
            row = []
            for _ in range(4):
                row.append(0)
            self.tiles.append(row)
