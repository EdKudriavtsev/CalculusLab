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


class BinaryOperation(Operation):
    def __init__(self, operation, left_expression, right_expression):
        super().__init__(operation, left_expression, right_expression)

    def string_value(self, sign):
        return "(" + self.arguments[0].string_value() + " " + sign + " " + self.arguments[1].string_value() + ")"


class UnaryOperation(Operation):
    def __init__(self, operation, expression):
        super().__init__(operation, expression)

    def string_value(self, sign):
        return sign + self.arguments[0].string_value()


class Power(BinaryOperation):
    def __init__(self, left_expression, right_expression):
        super().__init__(lambda x, y: x ** y, left_expression, right_expression)

    def string_value(self):
        return BinaryOperation.string_value(self, "^")


class Multiply(BinaryOperation):
    def __init__(self, left_expression, right_expression):
        super().__init__(lambda x, y: x * y, left_expression, right_expression)

    def string_value(self):
        return BinaryOperation.string_value(self, "*")


class Negate(UnaryOperation):
    def __init__(self, expression):
        super().__init__(lambda x: -x, expression)

    def string_value(self):
        return UnaryOperation.string_value(self, "-")


class Const:
    def __init__(self, constant):
        self.constant = constant

    def evaluate(self, *args):
        return self.constant

    def string_value(self):
        if self.constant == math.e:
            return "e"
        return str(self.constant)


class Variable:
    def __init__(self, variable):
        self.variable = variable

    def evaluate(self, *args):
        return args[["x", "y", "z"].index(self.variable)]

    def string_value(self):
        return str(self.variable)


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

    def string_value(self):
        return "[" + str(self.segment_start) + ", " + str(self.segment_end) + "]"


class Integral:
    def __init__(self, function):
        self.function = function

    def evaluate(self, equipment):
        integral_sum = 0
        for x in equipment.points:
            integral_sum += self.function.evaluate(x) * equipment.delta
        return integral_sum


    def string_value(self):
        return self.function.string_value()


    def graphic(self, equipment):
        sum_x = []
        for i in range(0, equipment.split_points_number):
            sum_x.append(equipment.segment_start + i * equipment.delta)
        sum_y = []
        for i in range(equipment.split_points_number):
            sum_y.append(self.function.evaluate(equipment.points[i]))
        plt.bar(sum_x, sum_y, equipment.delta, align='edge', edgecolor='black')
        x = []
        y = []
        curr = equipment.segment_start
        delta = (equipment.segment_end - equipment.segment_start) / 1000
        while curr < equipment.segment_end:
            x.append(curr)
            y.append(self.function.evaluate(curr))
            curr += delta
        plt.plot(x, y, color='r')
        plt.title("f(x) = " + self.function.string_value())
        plt.show()


split_points = int(input("Input number of split points: "))
equipment_type = EquipmentType(int(input("Choose number of equipment selection method: 1 - left, 2 - middle, "
                                         "3 - right, 4 - random: ")))

first_equipment = Equipment(0, 3, split_points, equipment_type)
second_equipment = Equipment(0, 1, split_points, equipment_type)
third_equipment = Equipment(-1, 1, split_points, equipment_type)
fourth_equipment = Equipment(0, 0.5, split_points, equipment_type)
fifth_equipment = Equipment(0, 1, split_points, equipment_type)

first_integral = Integral(Power(Const(5), Variable("x")))
second_integral = Integral(Power(Const(math.e), Variable("x")))
third_integral = Integral(Power(Const(math.e), Negate(Variable("x"))))
fourth_integral = Integral(Power(Const(math.e), Multiply(Const(3), Variable("x"))))
fifth_integral = Integral(Power(Const(math.e), Multiply(Const(2), Variable("x"))))

sys.stdout.write("Function: f(x) = " + first_integral.string_value())
sys.stdout.write(" Integration interval: " + first_equipment.string_value())
sys.stdout.write(" Calculated value: " + str(first_integral.evaluate(first_equipment)) + "\n")
first_integral.graphic(first_equipment)

sys.stdout.write("Function: f(x) = " + second_integral.string_value())
sys.stdout.write(" Integration interval: " + second_equipment.string_value())
sys.stdout.write(" Calculated value: " + str(second_integral.evaluate(second_equipment)) + "\n")
second_integral.graphic(second_equipment)

sys.stdout.write("Function: f(x) = " + third_integral.string_value())
sys.stdout.write(" Integration interval: " + third_equipment.string_value())
sys.stdout.write(" Calculated value: " + str(third_integral.evaluate(third_equipment)) + "\n")
third_integral.graphic(third_equipment)

sys.stdout.write("Function: f(x) = " + fourth_integral.string_value())
sys.stdout.write(" Integration interval: " + fourth_equipment.string_value())
sys.stdout.write(" Calculated value: " + str(fourth_integral.evaluate(fourth_equipment)) + "\n")
fourth_integral.graphic(fourth_equipment)

sys.stdout.write("Function: f(x) = " + fifth_integral.string_value())
sys.stdout.write(" Integration interval: " + fifth_equipment.string_value())
sys.stdout.write(" Calculated value: " + str(fifth_integral.evaluate(fifth_equipment)) + "\n")
fifth_integral.graphic(fifth_equipment)
