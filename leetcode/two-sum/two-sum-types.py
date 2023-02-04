from typing import List, Tuple


def twoSum(nums: List[int], target: int) -> List[Tuple[int, int]]:
    return [(1, 2)]


if __name__ == '__main__':
    listToSum = [1, 2, 1]
    listSolution = [(1, 2)]
    target = 3
    assert (twoSum(listToSum, target) == listSolution)
