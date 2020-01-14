import random


class Board:
    def __init__(self):
        self.__gen_starting_tiles()
        for i in range(2):
            self.spawn_new_tile()


    def spawn_new_tile(self):
        # TODO Give 2 a greater probability of spawning?
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
