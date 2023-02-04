# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.
#
# An input string is valid if:
#
#     Open brackets must be closed by the same type of brackets.
#     Open brackets must be closed in the correct order.
#     Every close bracket has a corresponding open bracket of the same type.
from typing import Dict


def isValid(stringWithParenthesis: str) -> bool:
    checkings: Dict[str: int] = {
        '(': 0,
        ')': 0,
        '{': 0,
        '}': 0,
        '[': 0,
        ']': 0,
    }

    for typeOfParenthesis in checkings.keys():
        for char in stringWithParenthesis:
            if char == typeOfParenthesis:
                checkings[typeOfParenthesis] += 1

    if checkings['('] == checkings[')'] and \
            checkings['['] == checkings[']'] and \
            checkings['{'] == checkings['}']:

        return True

    return False


if __name__ == '__main__':
    stringToBeChecked = '()()()[][[[[]]]]{}}}}'
    stringToBeCheckedWrong = '([)]'
    assert(isValid(stringToBeChecked))
