from itertools import product


"""
The goal is to simulate a tile so I can brute force combinations
of enemy and character positions to appropriately score enemies.
The end goal of this is to be able to create a robust NG+ experience
by tweaking enemies and bosses and KNOWING what effect that will have.
"""

nodes = {}


class Node():
    def __init__(self, row, col, tile) -> None:
        self.row = row
        self.col = col
        self.coord = (row,col)
        if tile not in nodes:
            nodes[tile] = {"allCoords": set()}
        nodes[tile][self.coord] = self
        nodes[tile]["allCoords"].add(self.coord)
        # The creates all coordinates that would be in range of this node.
        # These nodes might not exist, so it goes through afterwards to compare to nodes[tile]["allCoords"].
        self.coordsInRange = {
            1: set([(row+n[0],col+n[1]) for n in product(range(-2,3), range(-2,3)) if (row+n[0],col+n[1]) != (row,col) and abs(row - (row+n[0])) + abs(col - (col+n[1])) <= 2]),
            2: set([(row+n[0],col+n[1]) for n in product(range(-3,5), range(-3,5)) if (row+n[0],col+n[1]) != (row,col) and abs(row - (row+n[0])) + abs(col - (col+n[1])) <= 4]),
            3: set([(row+n[0],col+n[1]) for n in product(range(-4,6), range(-4,6)) if (row+n[0],col+n[1]) != (row,col) and abs(row - (row+n[0])) + abs(col - (col+n[1])) <= 6])
        }

# Standard tile
for row in range(5):
    for col in range(5):
        if col%2 == row%2:
            Node(row=row, col=col, tile="standard")

# Level 4 tile
for row in range(7):
    for col in range(7):
        if col%2 == row%2:
            Node(row=row, col=col, tile="level4")

# Executioner's Chariot tile
for row in range(7):
    for col in range(7):
        if col%2 == row%2 and (row,col) != (3,3):
            Node(row=row, col=col, tile="Executioner's Chariot")

# Old Iron King tile
for row in range(7):
    for col in range(7):
        if col%2 == row%2 and (row,col) not in {(0,2), (0,4), (2,0), (2,6), (4,0), (4,6)}:
            Node(row=row, col=col, tile="Old Iron King")

for tile in nodes:
    for coord in nodes[tile]:
        if coord == "allCoords":
            continue
        for r in nodes[tile][coord].coordsInRange:
            nodes[tile][coord].coordsInRange[r] = nodes[tile][coord].coordsInRange[r] & nodes[tile]["allCoords"]

