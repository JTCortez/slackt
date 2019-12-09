import unittest
from unittest.mock import MagicMock
import math
from ExpressionCalculation import ExpCalc


class ExpressCalculationTestCase(unittest.TestCase):
    # set up numbers to be tested
    # also set up test for each operations
    def setUp(self):
        self.number_1 = ["-8", "0", "172"]
        self.number_2 = ["-103", "0", "13"]
        self.op_for_1 = ["sin", "tan", "cos"]
        self.op_for_2 = ["+", "-", "*", "/", "%", "^", "root"]
        #white box coverage
        self.whitebox_input = ["1","-1","","-","--","(-","(-)","-5*6"]

    # test calculate method
    def test_calculate(self):
        # test sin
        for number in self.number_1:
            expr = "sin" + number
            self.assertAlmostEqual(math.sin(float(number)), ExpCalc(expr).calculate())

        # test cos
        for number in self.number_1:
            expr = "cos" + number
            self.assertAlmostEqual(math.cos(float(number)), ExpCalc(expr).calculate())

        # test tan
        for number in self.number_1:
            expr = "tan" + number
            self.assertAlmostEqual(math.tan(float(number)), ExpCalc(expr).calculate())

        # test addition
        add_expected_output = ['-', '-', '-0+', '-', '0', '+', '-0+', '+', '+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "+" + number2
                res = ExpCalc(expr).calculate()
                self.assertAlmostEqual(float(number1) + float(number2), res)
                # check domain
                res = self.__transformToDomain(res)
                self.assertIn(res, add_expected_output[index])
                index += 1

        # test subtraction
        sub_expected_output = ['-0+', '-', '-', '+', '0', '-', '+', '+', '-0+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "-" + number2
                res = ExpCalc(expr).calculate()
                self.assertAlmostEqual(float(number1) - float(number2), res)
                # check domain
                res = self.__transformToDomain(res)
                self.assertIn(res, sub_expected_output[index])
                index += 1

        # test multiplication
        mul_expected_output = ['+', '0', '-', '0', '0', '0', '-', '0', '+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "*" + number2
                res = ExpCalc(expr).calculate()
                self.assertAlmostEqual(float(number1) * float(number2), res)
                # check domain
                res = self.__transformToDomain(res)
                self.assertIn(res, mul_expected_output[index])
                index += 1

        # test division
        div_expected_output = ['+', 'ERR', '-', '0', 'ERR', '0', '-', 'ERR', '+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "/" + number2
                res = ExpCalc(expr).calculate()
                if number2 != '0':
                    self.assertAlmostEqual(float(number1) / float(number2), res)
                # check domain when not error (type = str when error)
                if not isinstance(res, str):
                    res = self.__transformToDomain(res)
                    self.assertIn(res, div_expected_output[index])
                else:
                    self.assertIn(div_expected_output[index], res)
                index += 1

        # test modular
        mod_expected_output = ['-0', 'ERR', '0+', '0', 'ERR', '0', '-0', 'ERR', '0+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "%" + number2
                res = ExpCalc(expr).calculate()
                if number2 != '0':
                    self.assertAlmostEqual(float(number1) % float(number2), res)
                # check domain when not error (type = str when error)
                if not isinstance(res, str):
                    res = self.__transformToDomain(res)
                    self.assertIn(res, mod_expected_output[index])
                else:
                    self.assertIn(mod_expected_output[index], res)
                index += 1

        # test power
        pow_expected_output = ['-+', '1', '-+', 'ERR', 'ERR', '0', '+', '1', '+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "^" + number2
                res = ExpCalc(expr).calculate()
                if number1 != '0' or float(number2) > 0:
                    self.assertAlmostEqual(float(number1) ** float(number2), res)
                # check domain when not error (type = str when error)
                if not isinstance(res, str):
                    if pow_expected_output[index] == '1':
                        self.assertAlmostEqual(res, float(pow_expected_output[index]))
                    else:
                        res = self.__transformToDomain(res)
                        self.assertIn(res, pow_expected_output[index])
                else:
                    self.assertIn(pow_expected_output[index], res)
                index += 1

        # test root
        root_expected_output = ['j', 'ERR', '+', 'ERR', '0', 'ERR', 'j', '0', '+']
        index = 0
        for number1 in self.number_1:
            for number2 in self.number_2:
                expr = number1 + "root" + number2
                res = ExpCalc(expr).calculate()
                if (float(number1) > 0 or number2 != '0') and (number1 != '0' or number2 == '0'):
                    self.assertAlmostEqual(float(number2) ** (1/float(number1)), res)
                # check if it's complex number
                if isinstance(res, complex):
                    self.assertEqual('j', root_expected_output[index])
                # or check domain if not error
                elif not isinstance(res, str):
                    res = self.__transformToDomain(res)
                    self.assertIn(res, root_expected_output[index])
                else:
                    self.assertIn(root_expected_output[index], res)
                index += 1
            
        # white box testimg
        whitebox_expected_output = ["1","~1","","~","~~","(~","(~)","~5*6"]
        index = 0
        for expr in self.whitebox_input:
            #negval_split is only public for the white box testing
            res = ExpCalc(expr).negval_split(expr)
            self.assertEqual(whitebox_expected_output[index], res)
            index += 1


        # integration testing

        # test calculation() and split_cal() first
        # Mock negval_split
        expcalc_1 = ExpCalc('')
        expcalc_1.negval_split = MagicMock(return_value='~1+~2')
        
        self.assertEqual(expcalc_1.calculation('-1+-2'), -3.0)
        self.assertEqual(expcalc_1.negval_split.call_count, 1)

        # test calculation() and negval_split()
        # Mock split_cal()
        expcalc_2 = ExpCalc('-1+-2')
        expcalc_2.split_cal = MagicMock(return_value=1.0)
    
        self.assertEqual(expcalc_2.calculation('(-1+-2)*3/-9'), 1.0)



    def __transformToDomain(self, number):
        if number < 0:
            return '-'
        elif number == 0:
            return '0'
        elif number > 0:
            return '+'
        return self


if __name__ == '__main__':
    unittest.main()
