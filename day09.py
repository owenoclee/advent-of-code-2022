import sys
import unittest
from typing import Iterator

Point = tuple[int, int]

DIRECTION_VECTOR_MAP = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1),
}


def simulate_h(h: Point, instruction: str) -> Iterator[Point]:
    vector = DIRECTION_VECTOR_MAP[instruction[0]]
    count = int(instruction[2:])
    for _ in range(count):
        h = (h[0] + vector[0], h[1] + vector[1])
        yield h


def simulate_t(h: Point, t: Point) -> Point:
    x, y = t

    if abs(h[0] - x) <= 1 and abs(h[1] - y) <= 1:
        return t

    if h[0] > x:
        x += 1
    if h[0] < x:
        x -= 1
    if h[1] > y:
        y += 1
    if h[1] < y:
        y -= 1

    return (x, y)


class TestDay09(unittest.TestCase):
    def test_simulate_h(self) -> None:
        r_4 = list(simulate_h((0, 0), "R 4"))
        assert r_4 == [(1, 0), (2, 0), (3, 0), (4, 0)]

        l_3 = list(simulate_h((0, 0), "L 3"))
        assert l_3 == [(-1, 0), (-2, 0), (-3, 0)]

        u_2 = list(simulate_h((0, 0), "U 2"))
        assert u_2 == [(0, -1), (0, -2)]

        d_1 = list(simulate_h((0, 0), "D 1"))
        assert d_1 == [(0, 1)]

    def test_simulate_t(self) -> None:
        r = simulate_t((2, 0), (0, 0))
        assert r == (1, 0)

        l = simulate_t((-2, 0), (0, 0))
        assert l == (-1, 0)

        u = simulate_t((0, -2), (0, 0))
        assert u == (0, -1)

        d = simulate_t((0, 2), (0, 0))
        assert d == (0, 1)

        r_u = simulate_t((2, -1), (0, 0))
        assert r_u == (1, -1)

        l_u = simulate_t((-2, -1), (0, 0))
        assert l_u == (-1, -1)

        r_d = simulate_t((2, 1), (0, 0))
        assert r_d == (1, 1)

        l_d = simulate_t((-2, 1), (0, 0))
        assert l_d == (-1, 1)


if __name__ == "__main__":
    lines = sys.stdin.read().strip().split("\n")

    visited_points: set[Point] = set()

    h = (0, 0)
    t = (0, 0)
    for instruction in lines:
        print(instruction)
        for next_h in simulate_h(h, instruction):
            h = next_h
            t = simulate_t(h, t)
            visited_points.add(t)

    print(f"Part 1: {len(visited_points)}")
