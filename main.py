import math
import sys
import random


class Operation:
    def __init__(self, operation, *args):
        self.arguments = args
        self.operation = operation

    def evaluate(self, *args):
        return self.operation(*map(lambda x: x.evaluate(*args), self.arguments))


class Degree(Operation):
    def __init__(self, left_expression, right_expression):
        Operation.__init__(self, lambda x, y: x ** y, left_expression, right_expression)


class Multiply(Operation):
    def __init__(self, left_expression, right_expression):
        Operation.__init__(self, lambda x, y: x * y, left_expression, right_expression)


class UnaryMinus(Operation):
    def __init__(self, expression):
        Operation.__init__(self, lambda x: -x, expression)


class Const:
    def __init__(self, constant):
        self.constant = constant

    def evaluate(self, *args):
        return self.constant


class Variable:
    def __init__(self, variable):
        self.variable = variable

    def evaluate(self, *args):
        return args[["x", "y", "z"].index(self.variable)]


class Integral:
    def __init__(self, function):
        self.function = function

    def evaluate(self, segment_start, segment_end, split_points_number, equipment):
        rimans_sum = 0
        delta = (segment_end - segment_start) / split_points_number
        while segment_start < segment_end:
            if equipment == 1:
                rimans_sum += delta * self.function.evaluate(segment_start)
            elif equipment == 2:
                rimans_sum += delta * self.function.evaluate(segment_start + (delta / 2))
            elif equipment == 3:
                rimans_sum += delta * self.function.evaluate(segment_start + delta)
            elif equipment == 4:
                rimans_sum += delta * self.function.evaluate(random.uniform(segment_start, segment_start + delta))
            else:
                raise Exception("Invalid format of equipment")
            segment_start += delta
        return rimans_sum


split_points = int(input("Input number of split points: "))
equipment_num = int(input("Choose number of equipment selection method : 1 - left, 2 - middle, 3 - right, 4 - random: "))

sys.stdout.write(str(Integral(Degree(Const(5), Variable("x"))).evaluate(0, 3, split_points, equipment_num)) + "\n")
sys.stdout.write(str(Integral(Degree(Const(math.e), Variable("x"))).evaluate(0, 1, split_points, equipment_num)) + "\n")
sys.stdout.write(str(Integral(Degree(Const(math.e), UnaryMinus(Variable("x")))).evaluate(-1, 1, split_points, equipment_num)) + "\n")
sys.stdout.write(str(Integral(Degree(Const(math.e), Multiply(Const(3), Variable("x")))).evaluate(0, 0.5, split_points, equipment_num)) + "\n")
sys.stdout.write(str(Integral(Degree(Const(math.e), Multiply(Const(2), Variable("x")))).evaluate(0, 1, split_points, equipment_num)) + "\n")