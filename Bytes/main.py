import math

MANTISSA_SIZE = 24
BIG_INT = 120
INT_BIT_COUNT = 8
EXP_OFFSET = 127


def convert_float_to_bytecode(number, size):
    result = []
    for index in range(0, size):
        number *= 2
        if number >= 1:
            result.append(1)
            number -= 1
        else:
            result.append(0)
    result.reverse()
    return result


def convert_int_to_bytecode(number):
    result = []
    if number == 0:
        i = INT_BIT_COUNT
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


def first_is_bigger(self_code, other_code):
    index = len(self_code) - 1
    while index != 0:
        index -= 1
        if self_code[index] < other_code[index]:
            return False
        elif self_code[index] > other_code[index]:
            return True


class ByteNum:
    def __init__(self, number=0):
        self.mantissa = []
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
            self.exponent = []
            self.sign = 0
            if number != 0.0:
                modify_number = math.modf(number)
                int_bytecode = convert_int_to_bytecode(int(modify_number[1]))
                float_bytecode = convert_float_to_bytecode(modify_number[0], MANTISSA_SIZE - len(int_bytecode))
                self.mantissa = float_bytecode + int_bytecode
                self.set_exp(len(float_bytecode))
                self.mantissa.reverse()
                while len(self.mantissa) <= MANTISSA_SIZE - 2:
                    self.mantissa.append(0)
                self.mantissa.reverse()
                if number < 0:
                    self.sign = 1
             
    def set_exp(self, shift, increase=EXP_OFFSET):
        exp = 0
        exp_sign = 0
        mantissa_size = len(self.mantissa)
        i = len(self.mantissa)
        while i != 0:
            i -= 1
            exp += 1
            if self.mantissa[i] == 1:
                self.mantissa.pop()
                break
            else:
                self.mantissa.pop()
        temp_exponent = (mantissa_size - (shift + exp)) + increase
        self.exponent = convert_int_to_bytecode(temp_exponent)
        self.exponent.append(exp_sign)

    def convert_to_straight_bytecode(self, number):
        self.__straight__ = convert_int_to_bytecode(number)
        if len(self.__straight__) < INT_BIT_COUNT - 1:
            i = INT_BIT_COUNT - 1 - len(self.__straight__)
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

    def convert_to_number(self, key='__straight__'):
        index = 0
        result = 0
        for bit in self.__dict__[key]:
            result += bit * 2 ** index
            index += 1
        if key != 'mantissa':
            if self.__dict__[key][-1] == 1:
                result -= 2 ** (index - 1)
                result *= -1
        return result

    def convert_to_int(self, key='__straight__'):
        if self.mantissa:
            exp = self.convert_to_number('exponent')
            mantissa = self.convert_to_number('mantissa')
            res = (-1) ** self.sign * 2 ** (exp - EXP_OFFSET) * (1 + (mantissa / 2 ** MANTISSA_SIZE - 1))
            return res
        else:
            return self.convert_to_number(key)

    def sum(self, other, key_self='__straight__', key_other='__straight__', size=INT_BIT_COUNT):
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

    def add_integer_numbers(self, other):
        res = ByteNum(1)
        if self.__straight__[-1] == other.__straight__[-1]:
            res.__straight__ = self.sum(other)
            res.__straight__[-1] = self.__straight__[-1]
            res.convert_to_reverse_bytecode()
            res.convert_to_additional_bytecode()
        elif self.__straight__[-1] == 0:
            if first_is_bigger(self.__straight__, other.__straight__):
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
            if first_is_bigger(self.__straight__, other.__straight__):
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

    def add_float_numbers(self, other):
        res = ByteNum(0.0)
        self.mantissa.append(1)
        other.mantissa.append(1)
        if self.exponent == other.exponent:
            res.exponent = other.exponent
            res.mantissa = self.sum(other, 'mantissa', 'mantissa', BIG_INT)
            res.set_exp(len(self.mantissa) - 1, res.convert_to_number('exponent'))
            while len(res.mantissa) >= MANTISSA_SIZE:
                res.mantissa.pop(0)
        elif self.convert_to_number('exponent') > other.convert_to_number('exponent'):
            iters = self.convert_to_number('exponent') - other.convert_to_number('exponent')
            for i in range(0, iters):
                other.mantissa.append(0)
            other.exponent = self.exponent
            res.exponent = self.exponent
            while len(self.mantissa) > len(other.mantissa):
                self.mantissa.pop(0)
            while len(self.mantissa) < len(other.mantissa):
                other.mantissa.pop(0)
            res.mantissa = self.sum(other, 'mantissa', 'mantissa', BIG_INT)
            res.set_exp(len(self.mantissa) - 1, res.convert_to_number('exponent'))
            while len(res.mantissa) >= MANTISSA_SIZE:
                res.mantissa.pop(0)
        else:
            iters = other.convert_to_number('exponent') - self.convert_to_number('exponent')
            for i in range(0, iters):
                self.mantissa.append(0)
            res.exponent = other.exponent
            self.exponent = other.exponent
            while len(self.mantissa) > len(other.mantissa):
                self.mantissa.pop(0)
            while len(self.mantissa) < len(other.mantissa):
                other.mantissa.pop(0)
            res.mantissa = self.sum(other, 'mantissa', 'mantissa', BIG_INT)
            res.set_exp(len(other.mantissa) - 1, res.convert_to_number('exponent'))
            while len(res.mantissa) >= MANTISSA_SIZE:
                res.mantissa.pop(0)
        self.mantissa.pop()
        other.mantissa.pop()
        return res

    def __add__(self, other):
        if not self.mantissa:
            return self.add_integer_numbers(other)
        else:
            return self.add_float_numbers(other)

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
        while first_is_bigger(last_result.__straight__, temp_result.__straight__):
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

    def __str__(self):
        stri = []
        if not self.mantissa:
            self.__straight__.reverse()
            self.__reverse__.reverse()
            self.__additional__.reverse()
            stri.append(self.__straight__)
            stri.append(self.__reverse__)
            stri.append(self.__additional__)
            result = ''
            for i in stri:
                result += ''.join(str(i))
                result += " "
            self.__straight__.reverse()
            self.__reverse__.reverse()
            self.__additional__.reverse()
        else:
            self.mantissa.reverse()
            self.exponent.reverse()
            stri.append(self.exponent)
            stri.append(self.mantissa)
            result = ''
            for i in stri:
                result += ''.join(str(i))
                result += " "
            self.mantissa.reverse()
            self.exponent.reverse()
        return result


if __name__ == '__main__':
    num1 = ByteNum(5)
    num2 = ByteNum(10)
    print(num1)
    print(num1.convert_to_int())
    print(num2)
    print(num2.convert_to_int())
    num3 = num1 + num2
    print(num3)
    print(num3.convert_to_int())
