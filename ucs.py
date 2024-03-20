"""
Author: Radek Jestřabík, 2024

Implementation of Uniform Cost Search algorithm to
find shortest path using recursion."""

import sys
from copy import deepcopy

class Coord:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
    
    def __eq__(self, cmp_with):
        if not isinstance(cmp_with, Coord):
            return NotImplemented
        
        return self.x == cmp_with.x and self.y == cmp_with.y
    
    def __str__(self) -> str:
        if (USING_Y_X):
            return f"[{self.y}, {self.x}]"
        else:
            return f"[{self.x}, {self.y}]"

class Tile:
    def __init__(self, coord : Coord, rating : int, predecessor : Coord):
        self.coord = coord
        self.rating = rating # -1 == wall
        self.predecessor = predecessor

    def __eq__(self, cmp_with):
        if not isinstance(cmp_with, Tile):
            return NotImplemented
        
        return self.coord == cmp_with.coord and self.rating == cmp_with.rating and self.predecessor == cmp_with.predecessor

    def __str__(self):
        return f"{self.coord}, {self.rating}, {str(self.predecessor) if self.predecessor is not None else 'NULL'}"

# 'Z' is a wall
map = """8 9 Z Z Z 3 9 6 7 8
         6 9 Z 6 5 3 8 5 7 8
         7 9 Z 2 4 3 8 7 5 8
         Z Z Z Z Z 3 Z Z Z Z
         9 9 Z 8 3 9 9 Z 8 9
         9 9 Z 9 3 4 2 Z 7 7
         9 9 Z 9 3 Z Z Z 8 7
         9 9 9 9 3 9 8 7 7 8
         9 9 7 6 3 7 9 8 9 9
         8 9 9 9 9 3 9 6 7 8"""

USING_Y_X = True # If using x for columns and y for rows set to True

# X and Y need to be set according to USING_Y_X
# If you want to set 7th column while using x for columns,
# and 3rd row while using y for rows,
# set USING_Y_X to True and Coord(6, 2)
# If USING_X_Y is False set Coord(2, 6)
start_pos = Coord(6, 5)
end_pos = Coord(3, 2)

if (USING_Y_X):
    start_pos.x, start_pos.y = start_pos.y, start_pos.x
    end_pos.x, end_pos.y = end_pos.y, end_pos.x

def parse_matrix(matrix : str) -> list[list[Tile]]:
    lines = [l.strip() for l in matrix.split("\n")]
    tiles = []

    for x, l in enumerate(lines):
        tile_line = []
        for y, t in enumerate(l.split()):
            if t == "Z":
                t = -1
            elif (not t.isdigit() or t == 0):
                print("Wrong tile rating - must be an integer greater than 0")
                sys.exit(1)
            
            t = int(t)

            tile_line.append(Tile(Coord(x, y), t, None))

        tiles.append(tile_line)
    
    return tiles

# Used to insert tile to correct index in closed list
tile_expanded_times = 0

def add_to_open(tile, x_offset, y_offset, tile_index):
    """Checks if index tiles[tile.x + x_offset, tile.y + y_offset]
    is in bounds and inserts them to global list variable 'open'
    at index tile_index + tile_expanded_times\n
    increases tile_expanded_times if added to the list"""
    global tile_expanded_times, open, closed

    is_in_bounds = True

    if x_offset < 0:
        if tile.coord.x + x_offset < 0:
            is_in_bounds = False
    elif x_offset > 0:
        if tile.coord.x + x_offset > len(tiles[0]) - 1:
            is_in_bounds = False
    
    if y_offset < 0:
        if tile.coord.y + y_offset < 0:
            is_in_bounds = False
    elif y_offset > 0:
        if tile.coord.y + y_offset > len(tiles) - 1:
            is_in_bounds = False

    # Is in bounds and is not a wall and not in closed
    if (is_in_bounds and
        tiles[tile.coord.x + x_offset][tile.coord.y + y_offset].rating != -1 and
        tile not in closed):

        new_tile = deepcopy(tiles[tile.coord.x + x_offset][tile.coord.y + y_offset])
        new_tile.predecessor = tile.coord
        new_tile.rating = tile.rating + tiles[tile.coord.x + x_offset][tile.coord.y + y_offset].rating

        open.append(new_tile)
        tile_expanded_times += 1

def find_shortest_path(closed) -> list[Coord]:
    shortest_path = []
    predecessor_tile = closed[-1]
    
    shortest_path.append(predecessor_tile.coord)

    while predecessor_tile.predecessor is not None:
        for t in closed:
            # Find first appearance of predecessor tile (= the one with lowest rating)
            if (t.coord == predecessor_tile.predecessor):
                predecessor_tile = t
                # Add to the beginning of list
                shortest_path.insert(0, predecessor_tile.coord)
                break
    
    return shortest_path


def ucs(searching, found):
    """Performs uniform cost search (Dijkstra's algorithm). 
    Recursive implementation"""
    global tile_expanded_times, open, closed, iteration

    print("======")
    print(f"ITERATION {str(iteration)}:")
    iteration += 1

    # Search ends unsuccessfully
    if len(open) == 0 or found or not searching:
        return (False, False)
    
    # Find first tile with lowest rating in open using linear search
    lowest_rating_tile = Tile(Coord(0, 0), float('inf'), None)
    lowest_rating_tile_index = -1
    
    # New open list without tiles with same coords from closed
    cleaned_open = []

    for t1 in open:
        in_closed = False
        for t2 in closed:
            if (t1.coord == t2.coord):
                in_closed = True
                break
        
        if (not in_closed):
            cleaned_open.append(t1)
    
    open = cleaned_open

    # Remove duplicate tiles with same coords
    unique_tiles = {}  # Dictionary to store unique tiles based on coordinates
    for tile in open:
        key = (tile.coord.x, tile.coord.y)
        if key not in unique_tiles or tile.rating < unique_tiles[key].rating:
            unique_tiles[key] = tile
    
    open = list(unique_tiles.values())

    # Find lowest ranking tile in open
    for i, tile in enumerate(open):
        if tile.rating < lowest_rating_tile.rating:
            lowest_rating_tile = tile
            lowest_rating_tile_index = i
    
    print("OPEN:")
    for t in open:
        print(t)

    print("CLOSED:")
    for t in closed:
        print(t)

    # If found end tile stop searching exit recursion
    if lowest_rating_tile.coord.x == end_pos.x and lowest_rating_tile.coord.y == end_pos.y:
        # Add found tile to closed
        closed.append(lowest_rating_tile)
        return (False, True)

    del open[lowest_rating_tile_index]

    add_to_open(lowest_rating_tile, -1, -1, lowest_rating_tile_index)
    add_to_open(lowest_rating_tile, -1, 0, lowest_rating_tile_index)
    add_to_open(lowest_rating_tile, -1, 1, lowest_rating_tile_index)

    add_to_open(lowest_rating_tile, 0, -1, lowest_rating_tile_index)
    add_to_open(lowest_rating_tile, 0, 1, lowest_rating_tile_index)
    
    add_to_open(lowest_rating_tile, 1, -1, lowest_rating_tile_index)
    add_to_open(lowest_rating_tile, 1, 0, lowest_rating_tile_index)
    add_to_open(lowest_rating_tile, 1, 1, lowest_rating_tile_index)

    # Add expanded tile to closed
    closed.append(lowest_rating_tile)

    tile_expanded_times = 0

    return ucs(True, False)


open = []
closed = []

tiles = parse_matrix(map)

if (len(tiles) > 0 and len(tiles[0]) > 0):
    # Set start to rating 0
    tiles[start_pos.x][start_pos.y].rating = 0
    # Add to open - iteration 0
    open.append(tiles[start_pos.x][start_pos.y])
else:
    print("Invalid map size")
    sys.exit(1)

if tiles[start_pos.x][start_pos.y] == -1 or tiles[end_pos.x][end_pos.y] == -1:
    print("Invalid start or end coordinate")
    sys.exit(1)

iteration = 0

_, found = ucs(True, False)

# If path was found reverse the list because path was added in recursion
if found:
    print("======")
    print("FOUND")

    print(f"RESULT - ITERATION: {iteration}")
    
    print("OPEN:")
    for t in open:
        print(t)
    
    print("CLOSED:")
    for t in closed:
        print(t)
    
    print("")
    
    shortest_path = find_shortest_path(closed)
    print("SHORTEST PATH:")
    for c in shortest_path:
        print(c)
else:
    print("Path not found")
