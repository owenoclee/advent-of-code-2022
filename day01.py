import sys
import unittest


def calculate_inventory_totals(input: str) -> list[int]:
    return [
        sum(int(cal) for cal in inv)
        for inv in (inv.split("\n") for inv in input.strip().split("\n\n"))
    ]


class TestDay01(unittest.TestCase):
    sample_input = (
        "1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000\n"
    )

    def test_calculate_inventory_totals(self) -> None:
        assert calculate_inventory_totals(self.sample_input) == [
            1000 + 2000 + 3000,
            4000,
            5000 + 6000,
            7000 + 8000 + 9000,
            10000,
        ]


if __name__ == "__main__":
    totals = calculate_inventory_totals(sys.stdin.read())
    sorted_totals = sorted(totals, reverse=True)

    print(f"Part 1: {sorted_totals[0]}")
    print(f"Part 2: {sum(sorted_totals[0:3])}")
