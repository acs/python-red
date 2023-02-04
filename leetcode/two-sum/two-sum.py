from typing import List, Tuple


def twoSum(nums, target):
    twoSumTargetTuples = []
    for (i, number) in enumerate(nums):
        for otherNumber in nums[i+1:]:
            print(number, otherNumber)
            # Move this logic to a function
            if (number + otherNumber) == target:
                if [number, otherNumber] not in twoSumTargetTuples and [otherNumber, number] not in twoSumTargetTuples:
                    twoSumTargetTuples.append([number, otherNumber])
    return twoSumTargetTuples


if __name__ == '__main__':
    listToSum = [1, 2, 1, 0, 3]
    listSolution = [(1, 2)]
    target = 3
    solution = twoSum(listToSum, target)
    if solution != listSolution:
        print(f'{solution} is not {listSolution}')
