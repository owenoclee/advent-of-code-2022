import sys
from copy import deepcopy
from typing import TypedDict
import unittest


class Instruction(TypedDict):
    quantity: int
    start: int
    end: int


def parse(input: str) -> tuple[list[list[str]], list[Instruction]]:
    crates_input, instructions_input = input.split("\n\n")

    crates_lines = crates_input.split("\n")
    crate_rows = [
        [line[i] for i in range(1, len(crates_lines[0]), 4)] for line in crates_lines
    ][:-1]
    crate_columns = [
        [crate for crate in col if crate != " "] for col in zip(*crate_rows)
    ]

    instructions_lines = instructions_input.split("\n")[:-1]
    instruction_rows: list[Instruction] = [
        {"quantity": int(row[1]), "start": int(row[3]), "end": int(row[5])}
        for row in (line.split(" ") for line in instructions_lines)
    ]

    return crate_columns, instruction_rows


def process(
    crates: list[list[str]], instructions: list[Instruction], cm_enabled: bool
) -> list[list[str]]:
    _crates = deepcopy(crates)
    step = 1 if cm_enabled else -1
    for i in instructions:
        _crates[i["end"] - 1][0:0] = _crates[i["start"] - 1][: i["quantity"]][::step]
        del _crates[i["start"] - 1][: i["quantity"]]
    return _crates


class TestDay05(unittest.TestCase):
    sample_input = (
        "    [D]    \n"
        "[N] [C]    \n"
        "[Z] [M] [P]\n"
        " 1   2   3 \n"
        "\n"
        "move 1 from 2 to 1\n"
        "move 3 from 1 to 3\n"
        "move 2 from 2 to 1\n"
        "move 1 from 1 to 2\n"
    )
    sample_crates = [["N", "Z"], ["D", "C", "M"], ["P"]]
    sample_instructions: list[Instruction] = [
        {"quantity": 1, "start": 2, "end": 1},
        {"quantity": 3, "start": 1, "end": 3},
        {"quantity": 2, "start": 2, "end": 1},
        {"quantity": 1, "start": 1, "end": 2},
    ]

    def test_parse(self) -> None:
        crates, instructions = parse(self.sample_input)

        assert crates == [["N", "Z"], ["D", "C", "M"], ["P"]]
        assert instructions == [
            {"quantity": 1, "start": 2, "end": 1},
            {"quantity": 3, "start": 1, "end": 3},
            {"quantity": 2, "start": 2, "end": 1},
            {"quantity": 1, "start": 1, "end": 2},
        ]

    def test_process_without_cratemover_9001(self) -> None:
        crates = process(self.sample_crates, self.sample_instructions, False)

        assert crates == [["C"], ["M"], ["Z", "N", "D", "P"]]

    def test_process_with_cratemover_9001(self) -> None:
        crates = process(self.sample_crates, self.sample_instructions, True)

        assert crates == [["M"], ["C"], ["D", "N", "Z", "P"]]


if __name__ == "__main__":
    crates, instructions = parse(sys.stdin.read())
    part_1_crates = process(crates, instructions, False)
    part_2_crates = process(crates, instructions, True)

    print(f"Part 1: {''.join(crates[0] for crates in part_1_crates)}")
    print(f"Part 2: {''.join(crates[0] for crates in part_2_crates)}")
