import math
class ByteNum:
    def __init__(self, number=0):
        if type(number) is int:
            self.__straight__ = []
            self.__reverse__ = []
            self.__additional__ = []
            self.convert_to_straight_bytecode(number)
            self.convert_to_reverse_bytecode()
            self.convert_to_additional_bytecode()
            if number >= 0:
                self.__straight__.append(0)
                self.__reverse__.append(0)
                self.__additional__.append(0)
            else:
                self.__straight__.append(1)
                self.__reverse__.append(1)
                self.__additional__.append(1)
        elif type(number) is float:
            self.mantissa = []
            self.exponent = []
            self.sign = 0


    def convert_int_to_bytecode(self, number):
        result = []
        if number == 0:
            i = 8
            while i != 0:
                result.append(0)
                i -= 1
        else:
            dividend = abs(number)  # делимое
            while dividend != 1:
                divider = 2  # делитель
                quotient = 1  # частное
                while divider <= dividend:
                    divider += 2
                    quotient += 1
                remainder = dividend - divider + 2
                quotient -= 1
                result.append(remainder)
                dividend = quotient
            result.append(1)
        return result

    def convert_float_to_bytecode(self, number):
        result = []
        for index in range(0, 5):
            number *= 2
            if number >= 1:
                result.append(1)
                number -= 1
            else:
                result.append(0)
        return result.reverse()
    def convert_to_straight_bytecode(self, number):
        self.__straight__ = self.convert_int_to_bytecode(number)
        if len(self.__straight__) < 7:
            i = 7 - len(self.__straight__)
            while i != 0:
                self.__straight__.append(0)
                i -= 1

    def convert_to_reverse_bytecode(self):
        self.__reverse__ = []
        for bit in self.__straight__:
            self.__reverse__.append(abs(bit - 1))

    def convert_to_additional_bytecode(self):
        self.__additional__ = self.__reverse__
        self.sum([1], '__additional__')

    def unconvert_additional_bytecode(self):
        self.__reverse__ = []
        for bit in self.__additional__:
            self.__reverse__.append(abs(bit - 1))
        self.__straight__ = self.__reverse__
        self.sum([1], '__straight__')

    def convert_to_int(self, key='__straight__'):
        index = 0
        result = 0
        for bit in self.__dict__[key]:
            result += bit * 2 ** index
            index += 1
        result += self.__dict__[key][-1] * -2 ** (index - 1)
        if self.__dict__[key][-1] == 1:
            result *= -1
        return result

    def sum(self, other, key_self='__straight__', key_other='__straight__', size=8):
        if type(other) is list:
            size = max(len(self.__dict__[key_self]), len(other))
            self.__dict__[key_self] += [0] * (size - len(self.__dict__[key_self]))
            other += [0] * (size - len(other))
            overflow = 0
            result = []
            for obj in zip(self.__dict__[key_self], other):
                value = obj[0] + obj[1] + overflow
                overflow = value // 2
                result.append(value % 2)
            if overflow == 1:
                result.append(1)
            self.__dict__[key_self] = result
        else:
            overflow = 0
            result = []
            for obj in zip(self.__dict__[key_self], other.__dict__[key_other]):
                value = obj[0] + obj[1] + overflow
                overflow = value // 2
                result.append(value % 2)
            if overflow == 1:
                result.append(1)
            while len(result) > size:
                result.pop()
            return result

    def first_is_biger(self, self_code, other_code):
        index = len(self_code) - 1
        while index != 0:
            index -= 1
            if self_code[index] < other_code[index]:
                return False
            elif self_code[index] > other_code[index]:
                return True

    def __add__(self, other):
        res = ByteNum(1)
        if self.__straight__[-1] == other.__straight__[-1]:
            res.__straight__ = self.sum(other)
            res.__straight__[-1] = self.__straight__[-1]
            res.convert_to_reverse_bytecode()
            res.convert_to_additional_bytecode()
        elif self.__straight__[-1] == 0:
            if self.first_is_biger(self.__straight__, other.__straight__):
                res.__straight__ = self.sum(other, '__straight__', '__additional__')
                res.convert_to_reverse_bytecode()
                res.convert_to_additional_bytecode()
            else:
                res.__additional__ = self.sum(other, '__straight__', '__additional__')
                res.unconvert_additional_bytecode()
                res.__additional__[-1] = 1
                res.__straight__[-1] = 1
                res.__reverse__[-1] = 1
        else:
            if self.first_is_biger(self.__straight__, other.__straight__):
                res.__additional__ = self.sum(other, '__additional__', '__straight__')
                res.unconvert_additional_bytecode()
                res.__additional__[-1] = 1
                res.__straight__[-1] = 1
                res.__reverse__[-1] = 1
            else:
                res.__straight__ = self.sum(other, '__additional__', '__straight__')
                res.convert_to_reverse_bytecode()
                res.convert_to_additional_bytecode()
                res.__additional__[-1] = 0
                res.__straight__[-1] = 0
                res.__reverse__[-1] = 0
        return res

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        result = ByteNum(0)
        iters = other.convert_to_int()
        if other.__straight__[-1] == 1:
            iters *= -1
            while iters != 0:
                iters -= 1
                result = result + self
            return -result
        else:
            while iters != 0:
                iters -= 1
                result = result + self
            return result

    def __truediv__(self, other):
        if self.__straight__[-1] != other.__straight__[-1]:
            result = ByteNum(-1)
        else:
            result = ByteNum(1)
        quotient = 0
        last_result = ByteNum(123)
        temp_result = self
        while self.first_is_biger(last_result.__straight__, temp_result.__straight__):
            last_result = ByteNum(0)
            last_result = last_result + temp_result
            temp_result.__straight__ = temp_result.sum(other, '__straight__', '__additional__')
            temp_result.convert_to_reverse_bytecode()
            temp_result.convert_to_additional_bytecode()
            quotient += 1
        result *= ByteNum(quotient - 1)
        result.__reverse__[-1] = result.__straight__[-1]
        result.__additional__[-1] = result.__reverse__[-1]
        return result

    def __neg__(self):
        self.__straight__[-1] = abs(self.__straight__[-1] - 1)
        self.__reverse__[-1] = abs(self.__straight__[-1] - 1)
        self.__additional__[-1] = abs(self.__straight__[-1] - 1)
        return self


if __name__ == '__main__':
    num1 = ByteNum(5)
    num2 = ByteNum(-10)
    num3 = num1 + num2
    print(num3.mantissa)
    print(num3.exponent)

    print(num3.convert_to_int())
