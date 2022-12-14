from __future__ import annotations
import sys
from enum import Enum
from collections import defaultdict
from functools import reduce
import unittest


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class TreeMatrix:
    def __init__(self, matrix: list[list[int]]):
        self._matrix = matrix
        self.dimensions = len(matrix[0])

    def get_trees_in_direction_of(self, dir: Direction, x: int, y: int) -> list[int]:
        if dir == Direction.EAST:
            return self._matrix[y][x + 1 :]
        if dir == Direction.WEST:
            return self._matrix[y][::-1][self.dimensions - x :]

        transposed = [[row for row in col] for col in zip(*self._matrix)]
        if dir == Direction.SOUTH:
            return transposed[x][y + 1 :]
        return transposed[x][::-1][self.dimensions - y :]

    def get_trees_in_all_directions_of(
        self, x: int, y: int
    ) -> dict[Direction, list[int]]:
        return {
            Direction.NORTH: self.get_trees_in_direction_of(Direction.NORTH, x, y),
            Direction.EAST: self.get_trees_in_direction_of(Direction.EAST, x, y),
            Direction.SOUTH: self.get_trees_in_direction_of(Direction.SOUTH, x, y),
            Direction.WEST: self.get_trees_in_direction_of(Direction.WEST, x, y),
        }

    def get_tree(self, x: int, y: int) -> int:
        return self._matrix[y][x]


class TestDay08(unittest.TestCase):
    def test_get_trees_in_direction_of__east(self) -> None:
        m = TreeMatrix(
            [
                [2, 7, 6],
                [9, 5, 1],
                [4, 3, 8],
            ]
        )
        assert m.get_trees_in_direction_of(Direction.EAST, 0, 0) == [7, 6]
        assert m.get_trees_in_direction_of(Direction.EAST, 1, 0) == [6]
        assert m.get_trees_in_direction_of(Direction.EAST, 2, 0) == []

        assert m.get_trees_in_direction_of(Direction.WEST, 0, 0) == []
        assert m.get_trees_in_direction_of(Direction.WEST, 1, 0) == [2]
        assert m.get_trees_in_direction_of(Direction.WEST, 2, 0) == [7, 2]

        assert m.get_trees_in_direction_of(Direction.SOUTH, 0, 0) == [9, 4]
        assert m.get_trees_in_direction_of(Direction.SOUTH, 0, 1) == [4]
        assert m.get_trees_in_direction_of(Direction.SOUTH, 0, 2) == []

        assert m.get_trees_in_direction_of(Direction.NORTH, 0, 0) == []
        assert m.get_trees_in_direction_of(Direction.NORTH, 0, 1) == [2]
        assert m.get_trees_in_direction_of(Direction.NORTH, 0, 2) == [9, 2]


if __name__ == "__main__":
    input_matrix = [
        [int(c) for c in row] for row in sys.stdin.read().strip().split("\n")
    ]

    tree_matrix = TreeMatrix(input_matrix)

    visible_trees = 0
    highest_scenic_score = 0
    for y in range(tree_matrix.dimensions):
        for x in range(tree_matrix.dimensions):
            cur_tree = tree_matrix.get_tree(x, y)
            line_of_sight_trees = tree_matrix.get_trees_in_all_directions_of(x, y)
            blocked_direction_count = 0
            scenic_scores: dict[Direction, int] = defaultdict(int)
            for (d, trees) in line_of_sight_trees.items():
                for tree in trees:
                    scenic_scores[d] += 1
                    if cur_tree <= tree:
                        blocked_direction_count += 1
                        break
            if blocked_direction_count < 4:
                visible_trees += 1
            # edges would be multiplied by zero, so skip
            if len(scenic_scores) < 4:
                continue
            scenic_score = reduce(lambda t, s: t * s, scenic_scores.values(), 1)
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score

    print(f"Part 1: {visible_trees}")
    print(f"Part 2: {highest_scenic_score}")
