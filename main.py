from enum import Enum
import math
import sys
import random
import matplotlib.pyplot as plt


class Operation:
    def __init__(self, operation, *args):
        self.arguments = args
        self.operation = operation

    def evaluate(self, *args):
        return self.operation(*map(lambda x: x.evaluate(*args), self.arguments))


class Degree(Operation):
    def __init__(self, left_expression, right_expression):
        super().__init__(lambda x, y: x ** y, left_expression, right_expression)


class Multiply(Operation):
    def __init__(self, left_expression, right_expression):
        super().__init__(lambda x, y: x * y, left_expression, right_expression)


class UnaryMinus(Operation):
    def __init__(self, expression):
        super().__init__(lambda x: -x, expression)


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


class EquipmentType(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    RANDOM = 4


class Equipment:
    def __init__(self, segment_start, segment_end, split_points_number, equipment):
        self.segment_start = segment_start
        self.segment_end = segment_end
        self.split_points_number = split_points_number
        self.delta = (segment_end - segment_start) / split_points_number
        self.points = []
        while segment_start < segment_end:
            if equipment == EquipmentType.LEFT:
                self.points.append(segment_start)
            elif equipment == EquipmentType.MIDDLE:
                self.points.append(segment_start + (self.delta / 2))
            elif equipment == EquipmentType.RIGHT:
                self.points.append(segment_start + self.delta)
            elif equipment == EquipmentType.RANDOM:
                self.points.append(random.uniform(segment_start, segment_start + self.delta))
            else:
                raise Exception("Invalid format of equipment")
            segment_start += self.delta


class Integral:
    def __init__(self, function):
        self.function = function

    def evaluate(self, equipment):
        integral_sum = 0
        for x in equipment.points:
            integral_sum += self.function.evaluate(x) * equipment.delta
        return integral_sum

    def graphic(self, equipment):
        sum_x = []
        for i in range(0, equipment.split_points_number):
            sum_x.append(equipment.segment_start + i * equipment.delta)
        sum_y = []
        for i in range(equipment.split_points_number):
            sum_y.append(self.function.evaluate(equipment.points[i]))
        plt.bar(sum_x, sum_y, equipment.delta, align='edge')
        x = []
        y = []
        curr = equipment.segment_start
        delta = (equipment.segment_end - equipment.segment_start) / 1000
        while curr < equipment.segment_end:
            x.append(curr)
            y.append(self.function.evaluate(curr))
            curr += delta
        plt.plot(x, y, color='r')
        plt.show()


split_points = int(input("Input number of split points: "))
equipment_type = EquipmentType(int(input("Choose number of equipment selection method: 1 - left, 2 - middle, "
                                         "3 - right, 4 - random: ")))

first_equipment = Equipment(0, 3, split_points, equipment_type)
second_equipment = Equipment(0, 1, split_points, equipment_type)
third_equipment = Equipment(-1, 1, split_points, equipment_type)
fourth_equipment = Equipment(0, 0.5, split_points, equipment_type)
fifth_equipment = Equipment(0, 1, split_points, equipment_type)

first_integral = Integral(Degree(Const(5), Variable("x")))
second_integral = Integral(Degree(Const(math.e), Variable("x")))
third_integral = Integral(Degree(Const(math.e), UnaryMinus(Variable("x"))))
fourth_integral = Integral(Degree(Const(math.e), Multiply(Const(3), Variable("x"))))
fifth_integral = Integral(Degree(Const(math.e), Multiply(Const(2), Variable("x"))))

sys.stdout.write("Function: f(x) = 5^x     Integration interval: [0, 3]    Calculated value: ")
sys.stdout.write(str(first_integral.evaluate(first_equipment)) + "\n")
sys.stdout.write("Function: f(x) = e^x     Integration interval: [0, 1]    Calculated value: ")
sys.stdout.write(str(second_integral.evaluate(second_equipment)) + "\n")
sys.stdout.write("Function: f(x) = e^(-x)  Integration interval: [-1, 1]   Calculated value: ")
sys.stdout.write(str(third_integral.evaluate(third_equipment)) + "\n")
sys.stdout.write("Function: f(x) = e^(3x)  Integration interval: [0, 0.5]  Calculated value: ")
sys.stdout.write(str(fourth_integral.evaluate(fourth_equipment)) + "\n")
sys.stdout.write("Function: f(x) = 2^(2x)  Integration interval: [0, 1]    Calculated value: ")
sys.stdout.write(str(fifth_integral.evaluate(fifth_equipment)) + "\n")

first_integral.graphic(first_equipment)
second_integral.graphic(second_equipment)
third_integral.graphic(third_equipment)
fourth_integral.graphic(fourth_equipment)
fifth_integral.graphic(fifth_equipment)
