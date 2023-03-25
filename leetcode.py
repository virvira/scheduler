class Solution:
    def isValid(self, s: str) -> bool:
        brackets = {
            '(': ')',
            '{': '}',
            '[': ']'
        }

        brackets_list = []

        for item in s:
            if item in brackets.keys():
                brackets_list.append(item)
            elif len(brackets_list) == 0 or brackets[brackets_list.pop()] != item:
                return False

        return len(brackets_list) == 0


sol = Solution()
print(sol.isValid('()'))
