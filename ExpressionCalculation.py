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
            if len(subExp) > 0 and subExp[0] == '~':
                subExp = '-' + subExp[1:]
            return float(subExp)
        except ValueError:  # if try doesn't work, deal with the expression
            subExp = self.__negval_split(subExp)
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

    # helper function to split and calculate
    def __split_cal(self, subExp, op):
        subExp_split = subExp.split(op)
        res = self.__calculation(subExp_split[0])
        for split in subExp_split[1:]:
            ret = self.__calculation(split)
            if isinstance(ret, str) and 'ERR' in ret:
                return ret
            if op == '+':
                res += ret
            elif op == '-':
                res -= ret
            elif op == '*':
                res *= ret
            elif op == '/':
                try:
                    res /= ret
                except ZeroDivisionError:
                    return "ERROR: division by 0"
            elif op == '%':
                try:
                    res %= ret
                except ZeroDivisionError:
                    return "ERROR: modular by 0"
            elif op == '^':
                if res == 0 and ret <= 0:
                    return "ERROR: 0 cannot be raise to 0 or negative power"
                res = pow(res, ret)
            elif op == 'root':
                if res == 0 and ret != 0:
                    return "ERROR: 0 cannot root anything but 0"
                elif res < 0 and ret == 0:
                    return "ERROR: negative number cannot root 0"
                elif res == 0 and ret == 0:
                    res = 0
                else:
                    res = ret ** (1/res)
            elif op == 'sin':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before sin() -> use 3*sin(5) not 3sin(5)"
                res = math.sin(ret)
            elif op == 'cos':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before cos() -> use 3*cos(5) not 3cos(5)"
                res = math.cos(ret)
            elif op == 'tan':
                if subExp_split[0] != "":
                    return "ERROR: invalid expression before tan() -> use 3*tan(5) not 3tan(5)"
                res = math.tan(ret)
        return res

    # helper to determine if '-' is negative or subtract, then deal with it appropriately
    def __negval_split(self, subExp):
        newExp = ""
        for i in range(0, len(subExp)):
            if subExp[i] == '-':
                if i == 0 or (subExp[i-1] != ')' and not subExp[i-1].isdigit()):
                    newExp += '~'
                    continue
            newExp += subExp[i]

        return newExp


if __name__ == '__main__':
    expr = '-8%13'
    result = ExpCalc(expr).calculate()
    res = (-3) ** (1/2)
    print(result, ' ', res)
