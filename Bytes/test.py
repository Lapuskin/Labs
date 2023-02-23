

        self.__straight__ = []
        self.__reverse__ = []
        self.__additional__ = []
        if type(number) is int:
            self.convert_to_straight_bytecode(number)
            self.convert_to_reverse_bytecode()
            #self.convert_additional()
            if number >= 0:
                self.__straight__.append(0)
                self.__reverse__.append(0)
            else:
                self.__straight__.append(1)
                self.__reverse__.append(1)
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

    def convert_to_reverse_bytecode(self):
        self.__reverse__ = []
        for bit in self.__straight__:
            self.__reverse__.append(abs(bit - 1))

    def convert_to_additional_bytecode(self):
        for bit in self.__reverse__:
           self.__additional__.append(abs(bit - 1))
        index = 1
        while True:
            if self.__additional__[-index] == 1:
                self.__additional__[-index - 1] += 1

    def __add__(self, other):
        size = max(len(self.__straight__), len(other.__straight__))
        self.__straight__ += [0] * (size - len(self.__straight__))
        other.__straight__ += [0] * (size - len(other.__straight__))
        overflow = 0
        res = []
        for obj in zip(self.__straight__, other.__straight__):
            value = obj[0] + obj[1] + overflow
            overflow = value // 2
            res.append(value % 2)
        if overflow == 1:
            res.append(1)
        print(res)
        self.convert_to_reverse_bytecode()

    def __setattr__(self, key, value):
            self.__dict__[key] = value





