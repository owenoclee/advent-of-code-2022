import sys
import unittest


def find_marker(input: str, n: int) -> int:
    for i in range(n, len(input) + 1):
        if len(set(input[i - n : i])) == n:
            return i
    raise ValueError


class TestDay06(unittest.TestCase):
    def test_find_marker(self) -> None:
        assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
        assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
        assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6

        assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
        assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
        assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23


if __name__ == "__main__":
    input = sys.stdin.read().strip()

    print(f"Part 1: {find_marker(input, 4)}")
    print(f"Part 2: {find_marker(input, 14)}")
