from __future__ import annotations
import sys
import unittest


class IdRange:
    def __init__(self, mini: int, maxi: int):
        self.mini = mini
        self.maxi = maxi

    def contains(self, other: IdRange) -> bool:
        return self.mini <= other.mini and self.maxi >= other.maxi

    def partially_contains(self, other: IdRange) -> bool:
        return self.mini >= other.mini and self.mini <= other.maxi


def is_pair_fully_contained(range_pair: tuple[IdRange, IdRange]) -> bool:
    a, b = range_pair
    if a.contains(b) or b.contains(a):
        return True
    return False


def is_pair_overlapping(range_pair: tuple[IdRange, IdRange]) -> bool:
    a, b = range_pair
    if a.partially_contains(b) or b.partially_contains(a):
        return True
    return False


def parse_pair(line: str) -> tuple[IdRange, IdRange]:
    def id_range_from_str(s: str) -> IdRange:
        mini, maxi = [int(id) for id in s.split("-")]
        return IdRange(mini, maxi)

    id_ranges = [id_range_from_str(range_str) for range_str in line.split(",")]
    return (id_ranges[0], id_ranges[1])


class TestDay04(unittest.TestCase):
    def test_is_pair_fully_contained(self) -> None:
        assert is_pair_fully_contained((IdRange(2, 8), IdRange(3, 7))) == True
        assert is_pair_fully_contained((IdRange(6, 6), IdRange(4, 6))) == True
        assert is_pair_fully_contained((IdRange(5, 7), IdRange(7, 9))) == False

    def test_is_pair_overlapping(self) -> None:
        assert is_pair_overlapping((IdRange(5, 7), IdRange(7, 9))) == True
        assert is_pair_overlapping((IdRange(6, 6), IdRange(4, 6))) == True
        assert is_pair_overlapping((IdRange(2, 4), IdRange(6, 8))) == False

    def test_parse_pair(self) -> None:
        a, b = parse_pair("2-4,6-8")
        assert a.mini == 2
        assert a.maxi == 4
        assert b.mini == 6
        assert b.maxi == 8


if __name__ == "__main__":
    lines = sys.stdin.read().strip().split("\n")
    parsed_pairs = [parse_pair(raw_pair) for raw_pair in lines]
    contained_pairs = sum(
        1 if is_pair_fully_contained(pair) else 0 for pair in parsed_pairs
    )
    overlapping_pairs = sum(
        1 if is_pair_overlapping(pair) else 0 for pair in parsed_pairs
    )

    print(f"Part 1: {contained_pairs}")
    print(f"Part 2: {overlapping_pairs}")
