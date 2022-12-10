from __future__ import annotations
import sys
from enum import Enum
from copy import deepcopy
import unittest


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def compute_tallest_seen_from_direction_matrix(
    matrix: list[list[int]], from_dir: Direction
) -> list[list[int]]:
    _matrix = deepcopy(matrix)
    length = len(_matrix[0])
    reversed_rows = False
    transposed = False

    if from_dir in [Direction.NORTH, Direction.SOUTH]:
        _matrix = list(list(l) for l in zip(*_matrix))
        transposed = True
    if from_dir in [Direction.EAST, Direction.SOUTH]:
        _matrix = [l[::-1] for l in _matrix]
        reversed_rows = True

    tallest_seen_matrix = [[-1] * length for _ in range(length)]
    if from_dir:
        for row in range(length):
            tallest_seen = -1
            for col in range(length):
                tallest_seen_matrix[row][col] = tallest_seen
                cur_tree_height = _matrix[row][col]
                tallest_seen = (
                    cur_tree_height if cur_tree_height > tallest_seen else tallest_seen
                )

    if reversed_rows:
        tallest_seen_matrix = [row[::-1] for row in tallest_seen_matrix]
    if transposed:
        tallest_seen_matrix = list(list(l) for l in zip(*tallest_seen_matrix))

    return tallest_seen_matrix


def min_of_matrices(matrices: list[list[list[int]]]) -> list[list[int]]:
    length = len(matrices[0][0])
    summary_matrix = [[99] * length for _ in range(length)]
    for matrix in matrices:
        for row in range(length):
            for col in range(length):
                cur_summary_height = summary_matrix[row][col]
                cur_matrix_height = matrix[row][col]
                summary_matrix[row][col] = (
                    cur_matrix_height
                    if cur_matrix_height < cur_summary_height
                    else cur_summary_height
                )

    return summary_matrix


def count_matrix_filtered_by_min_matrix(
    matrix: list[list[int]], min_matrix: list[list[int]]
) -> int:
    length = len(matrix[0])
    return sum(
        1
        for _ in filter(
            lambda t: t[0] > t[1],
            (
                (pm[i], mm[i])
                for i in range(length)
                for (pm, mm) in zip(matrix, min_matrix)
            ),
        )
    )


class TestDay08(unittest.TestCase):
    sample_matrix = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]

    def test_compute_tallest_seen_from_direction_matrix(self) -> None:
        z = -1

        from_west = compute_tallest_seen_from_direction_matrix(
            self.sample_matrix, Direction.WEST
        )
        assert from_west == [
            [z, 3, 3, 3, 7],
            [z, 2, 5, 5, 5],
            [z, 6, 6, 6, 6],
            [z, 3, 3, 5, 5],
            [z, 3, 5, 5, 9],
        ]

        from_east = compute_tallest_seen_from_direction_matrix(
            self.sample_matrix, Direction.EAST
        )
        assert from_east == [
            [7, 7, 7, 3, z],
            [5, 5, 2, 2, z],
            [5, 3, 3, 2, z],
            [9, 9, 9, 9, z],
            [9, 9, 9, 0, z],
        ]

        from_north = compute_tallest_seen_from_direction_matrix(
            self.sample_matrix, Direction.NORTH
        )
        assert from_north == [
            [z, z, z, z, z],
            [3, 0, 3, 7, 3],
            [3, 5, 5, 7, 3],
            [6, 5, 5, 7, 3],
            [6, 5, 5, 7, 9],
        ]

        from_south = compute_tallest_seen_from_direction_matrix(
            self.sample_matrix, Direction.SOUTH
        )
        assert from_south == [
            [6, 5, 5, 9, 9],
            [6, 5, 5, 9, 9],
            [3, 5, 5, 9, 9],
            [3, 5, 3, 9, 0],
            [z, z, z, z, z],
        ]

    def test_min_of_matrices(self) -> None:
        min_matrix = min_of_matrices(
            [
                [
                    [1, 2, 3],
                    [3, 2, 1],
                    [5, 4, 3],
                ],
                [
                    [3, 2, 1],
                    [1, 2, 3],
                    [2, 3, 4],
                ],
            ]
        )

        assert min_matrix == [
            [1, 2, 1],
            [1, 2, 1],
            [2, 3, 3],
        ]

    def test_count_matrix_filtered_by_min_matrix(self) -> None:
        count = count_matrix_filtered_by_min_matrix(
            [
                [1, 2, 3],
                [2, 3, 4],
                [3, 4, 5],
            ],
            [
                [3, 3, 3],
                [3, 3, 3],
                [3, 3, 3],
            ],
        )

        assert count == 3


if __name__ == "__main__":
    input_matrix = [
        [int(c) for c in row] for row in sys.stdin.read().strip().split("\n")
    ]

    matrices: list[list[list[int]]] = []
    for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
        matrices.append(compute_tallest_seen_from_direction_matrix(input_matrix, d))
    min_matrix = min_of_matrices(matrices)
    count = count_matrix_filtered_by_min_matrix(input_matrix, min_matrix)

    print(f"Part 1: {count}")
