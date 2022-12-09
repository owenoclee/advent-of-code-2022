import sys
from typing import Union, cast
from copy import deepcopy, copy
import unittest

FileSystem = dict[str, Union["FileSystem", int]]


def add_to_filesystem(
    fs: FileSystem,
    path: list[str],
    item: tuple[str, FileSystem | int],
) -> FileSystem:
    _fs = deepcopy(fs)
    fs_cur = _fs
    for d in path:
        if d not in cast(FileSystem, fs_cur):
            fs_cur[d] = {}
        fs_cur = cast(FileSystem, fs_cur[d])
    fs_cur[item[0]] = item[1]
    return _fs


def generate_filesystem(input: str) -> FileSystem:
    fs: FileSystem = {}
    path: list[str] = []
    for line in input.strip().split("\n")[1:]:
        if line.startswith("$ cd "):
            target = line[5:]
            if target == "..":
                path.pop()
            else:
                fs = add_to_filesystem(fs, path, (target, {}))
                path.append(target)
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir "):
            name = line[4:]
            fs = add_to_filesystem(fs, path, (name, {}))
        else:
            size, name = line.split(" ")
            fs = add_to_filesystem(fs, path, (name, int(size)))
    return fs


def populate_sizes(fs: FileSystem) -> FileSystem:
    _fs = deepcopy(fs)
    for (k, v) in ((k, v) for (k, v) in _fs.items() if isinstance(v, dict)):
        _fs[k] = populate_sizes(v)
    else:
        size = 0
        for item in _fs.values():
            if isinstance(item, int):
                size += item
            else:
                subdir_size = item["_size"]
                if isinstance(subdir_size, int):
                    size += subdir_size
                else:
                    raise ValueError
        _fs["_size"] = size
    return _fs


def get_path_sizes(fs: FileSystem, path: list[str] = []) -> list[tuple[list[str], int]]:
    paths: list[tuple[list[str], int]] = []
    for (k, v) in fs.items():
        if not isinstance(v, dict):
            continue
        paths += get_path_sizes(v, path + [k])
    if "_size" in fs:
        return paths + [(path, cast(int, fs["_size"]))]

    return paths


class TestDay07(unittest.TestCase):
    sample_input = (
        "$ cd /\n"
        "$ ls\n"
        "dir a\n"
        "14848514 b.txt\n"
        "8504156 c.dat\n"
        "dir d\n"
        "$ cd a\n"
        "$ ls\n"
        "dir e\n"
        "29116 f\n"
        "2557 g\n"
        "62596 h.lst\n"
        "$ cd e\n"
        "$ ls\n"
        "584 i\n"
        "$ cd ..\n"
        "$ cd ..\n"
        "$ cd d\n"
        "$ ls\n"
        "4060174 j\n"
        "8033020 d.log\n"
        "5626152 d.ext\n"
        "7214296 k\n"
    )
    sample_filesystem: FileSystem = {
        "a": {
            "e": {
                "i": 584,
            },
            "f": 29116,
            "g": 2557,
            "h.lst": 62596,
        },
        "b.txt": 14848514,
        "c.dat": 8504156,
        "d": {
            "j": 4060174,
            "d.log": 8033020,
            "d.ext": 5626152,
            "k": 7214296,
        },
    }
    sample_filesystem_with_sizes: FileSystem = {
        "_size": 48381165,
        "a": {
            "_size": 94853,
            "e": {
                "_size": 584,
                "i": 584,
            },
            "f": 29116,
            "g": 2557,
            "h.lst": 62596,
        },
        "b.txt": 14848514,
        "c.dat": 8504156,
        "d": {
            "_size": 24933642,
            "j": 4060174,
            "d.log": 8033020,
            "d.ext": 5626152,
            "k": 7214296,
        },
    }

    def test_generate_filesystem(self) -> None:
        fs = generate_filesystem(self.sample_input)

        assert fs == self.sample_filesystem

    def test_populate_sizes(self) -> None:
        fs = populate_sizes(cast(FileSystem, self.sample_filesystem))

        assert fs == self.sample_filesystem_with_sizes

    def test_get_path_sizes(self) -> None:
        paths = get_path_sizes(self.sample_filesystem_with_sizes)
        print(paths)

        assert paths == [
            (["a", "e"], 584),
            (["a"], 94853),
            (["d"], 24933642),
            ([], 48381165),
        ]


MAX_SIZE = 100_000
MAX_FILESYSTEM_SIZE = 70_000_000
REQUIRED_FREE_SPACE = 30_000_000
if __name__ == "__main__":
    fs = generate_filesystem(sys.stdin.read().strip())
    fs = populate_sizes(fs)
    paths_with_sizes = get_path_sizes(fs)
    sizes = [size for (_, size) in paths_with_sizes]

    part_1 = sum(size for size in sizes if size <= MAX_SIZE)

    used_space = list(filter(lambda p: p[0] == [], paths_with_sizes))[0][1]
    free_space = MAX_FILESYSTEM_SIZE - used_space
    space_needed = REQUIRED_FREE_SPACE - free_space
    part_2 = min(sorted(filter(lambda s: s >= space_needed, sizes)))

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
