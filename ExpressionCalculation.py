import math


# Expression Calculation class
class ExpCalc:
    def __init__(self, exp):
        self.exp = exp

    # call calculation function which is recursive
    def calculate(self):
        return self.__calculation(self.exp)

    # recursively calculate subexpressions
    def __calculation(self, subExp):
        # abort if error
        if "ERROR" in subExp:
            return subExp

        try:    # try to directly convert to float value
            return float(subExp)
        except ValueError:  # if try doesn't work, deal with the expression
            # prioritize dealing with bracket first
            if ')' in subExp or '(' in subExp:
                level, maxLevelhead, maxLeveltail = 0, 0, 0
                for i in range(0, len(subExp)):
                    if subExp[i] == '(':
                        level += 1
                        maxLevelhead = i
                    if subExp[i] == ')':
                        level -= 1
                if level != 0:  # inequality in number of open and close bracket,return error
                    return "ERROR: brackets don't match"
                for i in range(maxLevelhead, len(subExp)):
                    if subExp[i] == ')':
                        maxLeveltail = i
                        break
                newsubExp = subExp[:maxLevelhead]
                newsubExp += str(self.__calculation(subExp[maxLevelhead+1:maxLeveltail]))
                newsubExp += subExp[maxLeveltail+1:]
                return self.__calculation(newsubExp)
            # then +
            elif '+' in subExp:
                return self.__split_cal(subExp, '+')
            # then -
            elif '-' in subExp:
                return self.__split_cal(subExp, '-')
            # then *
            elif '*' in subExp:
                return self.__split_cal(subExp, '*')
            # then /
            elif '/' in subExp:
                return self.__split_cal(subExp, '/')
            # then %
            elif '%' in subExp:
                return self.__split_cal(subExp, '%')
            # then ^
            elif '^' in subExp:
                return self.__split_cal(subExp, '^')
            # then root
            elif 'root' in subExp:
                return self.__split_cal(subExp, 'root')
            # then sin
            elif 'sin' in subExp:
                return self.__split_cal(subExp, 'sin')
            # then cos
            elif 'cos' in subExp:
                return self.__split_cal(subExp, 'cos')
            # then tan
            elif 'tan' in subExp:
                return self.__split_cal(subExp, 'tan')
            else:
                return "ERROR: invalid expression"

    # helper function to split and caculate
    def __split_cal(self, subExp, op):
        subExp_split = subExp.split(op)
        res = self.__calculation(subExp_split[0])
        for split in subExp_split[1:]:
            if op == '*':
                res *= self.__calculation(split)
            elif op == '/':
                try:
                    res /= self.__calculation(split)
                except ZeroDivisionError:
                    return "ERROR: division by 0"
            elif op == '+':
                res += self.__calculation(split)
            elif op == '-':
                res -= self.__calculation(split)
            elif op == '%':
                res %= self.__calculation(split)
            elif op == '^':
                res = pow(res, self.__calculation(split))
            elif op == 'root':
                res = self.__calculation(split) ** (1/res)
            elif op == 'sin':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before sin() -> use 3*sin(5) not 3sin(5)"
                res = math.sin(self.__calculation(split))
            elif op == 'cos':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before cos() -> use 3*cos(5) not 3cos(5)"
                res = math.cos(self.__calculation(split))
            elif op == 'tan':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before tan() -> use 3*tan(5) not 3tan(5)"
                res = math.tan(self.__calculation(split))
        return res


if __name__ == '__main__':
    expr = "sin(1+sin(1))"
    result = ExpCalc(expr).calculate()
    print(result,)
