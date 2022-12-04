import sys
import unittest

shape_values_map = {
    "X": 1,  # rock
    "Y": 2,  # paper
    "Z": 3,  # scissors
}

win_map = {
    "A": "Y",  # rock       beaten by paper
    "B": "Z",  # paper      beaten by scissors
    "C": "X",  # scissors   beaten by rock
}

lose_map = {
    "A": "Z",  # rock       beats scissors
    "B": "X",  # paper      beats rock
    "C": "Y",  # scissors   beats paper
}

draw_map = {
    "A": "X",
    "B": "Y",
    "C": "Z",
}

LOSE_VALUE = 0
DRAW_VALUE = 3
WIN_VALUE = 6

LOSE_NEEDED_SHAPE = "X"
DRAW_NEEDED_SHAPE = "Y"
WIN_NEEDED_SHAPE = "Z"


def score_for_line_part_1(line: str) -> int:
    opp, own = line[0], line[2]
    shape_value = shape_values_map[own]
    if win_map[opp] == own:
        return shape_value + WIN_VALUE
    if draw_map[opp] == own:
        return shape_value + DRAW_VALUE
    return shape_value + LOSE_VALUE


def score_for_line_part_2(line: str) -> int:
    opp, desired_outcome = line[0], line[2]
    if desired_outcome == LOSE_NEEDED_SHAPE:
        return shape_values_map[lose_map[opp]] + LOSE_VALUE
    if desired_outcome == DRAW_NEEDED_SHAPE:
        return shape_values_map[draw_map[opp]] + DRAW_VALUE
    return shape_values_map[win_map[opp]] + WIN_VALUE


class TestDay02(unittest.TestCase):
    def test_score_for_line_part_1(self) -> None:
        assert score_for_line_part_1("A Y") == 8
        assert score_for_line_part_1("B X") == 1
        assert score_for_line_part_1("C Z") == 6

    def test_score_for_line_part_2(self) -> None:
        assert score_for_line_part_2("A Y") == 4
        assert score_for_line_part_2("B X") == 1
        assert score_for_line_part_2("C Z") == 7


if __name__ == "__main__":
    lines = sys.stdin.read().strip().split("\n")
    part_1_score = sum(score_for_line_part_1(line) for line in lines)
    part_2_score = sum(score_for_line_part_2(line) for line in lines)

    print(f"Part 1: {part_1_score}")
    print(f"Part 2: {part_2_score}")
