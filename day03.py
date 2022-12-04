import sys
from math import floor
from collections import defaultdict
import unittest

LOWERCASE_OFFSET = 96  # chr("a") == 97
UPPERCASE_OFFSET = 38  # chr("A") == 65


def split_compartments(rucksack: str) -> tuple[str, str]:
    midpoint = floor(len(rucksack) / 2)
    return (rucksack[:midpoint], rucksack[midpoint:])


def find_duplicate_item_in_compartments(compartments: tuple[str, str]) -> str:
    items_map = {item: True for item in compartments[0]}
    for item in compartments[1]:
        if items_map.get(item):
            return item
    raise ValueError


def find_common_item_in_rucksacks(rucksacks: list[str]) -> str:
    items_map: dict[str, list[bool]] = defaultdict(lambda: [False, False, False])
    for i, sack in enumerate(rucksacks):
        for item in sack:
            items_map[item][i] = True
            if i == 2 and items_map[item] == [True, True, True]:
                return item
    raise ValueError


def item_priority(char: str) -> int:
    char_code = ord(char)
    if char_code <= 90:
        return char_code - UPPERCASE_OFFSET
    return char_code - LOWERCASE_OFFSET


class TestDay03(unittest.TestCase):
    def test_split_compartments(self) -> None:
        (first, second) = split_compartments("vJrwpWtwJgWrhcsFMMfFFhFp")
        assert first == "vJrwpWtwJgWr"
        assert second == "hcsFMMfFFhFp"

    def test_find_duplicate_item_in_compartments(self) -> None:
        assert (
            find_duplicate_item_in_compartments(("vJrwpWtwJgWr", "hcsFMMfFFhFp")) == "p"
        )

    def test_find_common_item_in_rucksacks(self) -> None:
        assert (
            find_common_item_in_rucksacks(
                [
                    "vJrwpWtwJgWrhcsFMMfFFhFp",
                    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                    "PmmdzqPrVvPwwTWBwg",
                ]
            )
            == "r"
        )

    def test_item_priority(self) -> None:
        assert item_priority("a") == 1
        assert item_priority("z") == 26
        assert item_priority("A") == 27
        assert item_priority("Z") == 52


if __name__ == "__main__":
    rucksacks = sys.stdin.read().strip().split("\n")
    part_1_solution = sum(
        item_priority(find_duplicate_item_in_compartments(split_compartments(rucksack)))
        for rucksack in rucksacks
    )

    sack_triplets = [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]
    part_2_solution = sum(
        item_priority(find_common_item_in_rucksacks(sack_triplet))
        for sack_triplet in sack_triplets
    )

    print(f"Part 1: {part_1_solution}")
    print(f"Part 2: {part_2_solution}")
