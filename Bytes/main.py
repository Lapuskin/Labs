class ByteNum:
    def __init__(self, number=0):
        self.__straight__ = []
        self.__reverse__ = []
        self.__additional__ = []
        if type(number) is int:
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
        #elif type(number) is float:
                #do_smth2()

    def convert_to_straight_bytecode(self, number):
        dividend = abs(number)  # делимое
        while dividend != 1:
            divider = 2  # делитель
            quotient = 1  # частное
            while divider <= dividend:
                divider += 2
                quotient += 1
            remainder = dividend - divider + 2
            quotient -= 1
            self.__straight__.append(remainder)
            dividend = quotient
        self.__straight__.append(1)
        if len(self.__straight__) < 7:
            iter = 7 - len(self.__straight__)
            while iter != 0:
                self.__straight__.append(0)
                iter -= 1

    def convert_to_reverse_bytecode(self):
        self.__reverse__ = []
        for bit in self.__straight__:
            self.__reverse__.append(abs(bit - 1))

    def convert_to_additional_bytecode(self):
        self.__additional__ = self.__reverse__
        self.sum([1], '__additional__')

    def convert_to_int(self, key):
        index = 0
        result = 0
        for bit in self.__dict__[key]:
            result += bit * 2 ** index
            index += 1
        result += self.__dict__[key][-1] * -2 ** (index - 1)
        if self.__dict__[key][-1] == 1:
            result *=-1
        print(result)
        return result

    def sum(self, other, key_self = '__straight__', key_other = '__straight__'):
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
            size = max(len(self.__dict__[key_self]), len(other.__dict__[key_other]))
            self.__dict__[key_self] += [0] * (size - len(self.__dict__[key_self]))
            other.__dict__[key_other] += [0] * (size - len(other.__dict__[key_other]))
            overflow = 0
            result = []
            for obj in zip(self.__dict__[key_self], other.__dict__[key_other]):
                value = obj[0] + obj[1] + overflow
                overflow = value // 2
                result.append(value % 2)
            if overflow == 1:
                result.append(1)
            while len(result) > 8: result.pop()
            self.__straight__ = result

    def __iadd__(self, other):
        if self.__straight__[-1] == other.__straight__[-1]:
            self.sum(other)
            self.__straight__[-1] = other.__straight__[-1]
        elif self.__straight__[-1] == 1:
            self.sum(other, '__additional__', '__straight__')
            self.convert_to_reverse_bytecode()
            self.__reverse__[-1] = self.__straight__[-1]
            self.convert_to_additional_bytecode()
            self.__straight__ = self.__additional__
        else:
            self.sum(other, '__straight__', '__additional__')
        self.convert_to_reverse_bytecode()
        self.__reverse__[-1] = self.__straight__[-1]
        self.convert_to_additional_bytecode()
        return self

    def __isub__(self, other):
        self.sum(other, '__straight__', '__additional__')
        self.convert_to_reverse_bytecode()
        self.convert_to_additional_bytecode()
        return self

    def __imul__(self, iters):
        self_straight_code = self.__straight__
        while iters != 0:
            self.sum(self_straight_code, '__straight__')
            iters -= 1
        return self

    #def __itruediv__(self, other):

    def __neg__(self):
        self.__straight__[-1] = 1
        self.__reverse__[-1] = 1
        self.__additional__[-1] = 1
        return self

if __name__ == '__main__':
    num1 = ByteNum(6)
    num2 = ByteNum(5)
    print(num1.__straight__)
    print(num1.__reverse__)
    print(num1.__additional__)
    num1 += num2
    num1.convert_to_int('__straight__')
    num1 -= num2
    print(num1.__straight__)
    print(num1.__reverse__)
    print(num1.__additional__)
    num1.convert_to_int('__straight__')



