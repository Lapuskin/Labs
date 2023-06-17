def convert_to_number(bytes_array):
    index = 0
    result = 0
    bytes_array.reverse()
    for bit in bytes_array:
        result += bit * 2 ** index
        index += 1
    bytes_array.reverse()
    return result


class Table_of_truth:
    table = []
    rows_size = 0
    columns_size = 0
    sknf_form = []
    sdnf_form = []
    index_byte_form = []

    def __init__(self):
        self.num_sdnf = None
        self.bytes_sdnf = None
        self.num_sknf = None
        self.header = None
        self.index_num_form = None
        self.bytes_sknf = None
        self.tree = None
        self.expression = None

    def create_min_table(self):
        self.min_table = []
        for i in range(len(self.table)):
            self.min_table.append([])
            for j in range(len(self.tree.variables)):
                if i != 0:
                    self.min_table[i].append(int(self.table[i][j]))
                else:
                    self.min_table[i].append(self.table[i][j])
            if i != 0:
                self.min_table[i].append(int(self.table[i][-1]))
            else:
                self.min_table[i].append(self.table[i][-1])

        self.print_min_table()


    def print_min_table(self):
        for row in range(self.rows_size):
            for column in range(len(self.tree.variables) +1):
                print(self.min_table[row][column], end=' | ')
            print()
        print()


    def build(self, tree):
        self.expression = tree.expression
        self.tree = tree
        self.rows_size = 1 + 2 ** len(tree.values)
        self.columns_size = len(tree.operations) + len(tree.values)
        self.table = []
        for i in range(0, self.rows_size):
            self.table.append([])
            for j in range(0, self.columns_size):
                self.table[i].append(False)

        tree.variables.reverse()
        tree.operations.reverse()
        variables_in_table = list(tree.values.keys())
        operations = []
        # variables_in_table.reverse()
        for operation in tree.operations:
            operations.append(operation.expression)
        self.header = variables_in_table + operations

        for i in range(0, self.columns_size):
            self.table[0][i] = ''.join(self.header[i])
        self.calc()

    def calc(self):
        offset = 1
        for i in range(len(self.tree.values) - 1, -1, -1):
            j = 1
            while j < self.rows_size:
                for elem in range(offset):
                    self.table[j][i] = False
                    j += 1
                if j != self.rows_size:
                    for elem in range(offset):
                        self.table[j][i] = True
                        j += 1
            offset = 2 ** (len(self.tree.values) - i)

        for i in range(1, self.rows_size):
            for j in range(len(self.tree.values)):
                self.tree.values[str(self.table[0][j])] = self.table[i][j]
            self.tree.calc()
            for j in range(len(self.tree.values), self.columns_size):
                self.table[i][j] = self.tree.operations[j - len(self.tree.values)].value

    def create_sknf_form(self):
        sknf_rows = []
        for i in range(self.rows_size):
            if self.table[i][self.columns_size - 1] is False:
                sknf_rows.append(i)

        self.sknf_form = ''
        self.bytes_sknf = []
        self.num_sknf = []
        for row in sknf_rows:
            byte_num = []
            for i in range(len(self.tree.values)):
                byte_num.append(int(self.table[row][i]))
                self.sknf_form += str(int(self.table[row][i]))
            self.sknf_form += '*'
            self.bytes_sknf.append(byte_num)
            self.num_sknf.append(convert_to_number(byte_num))

        print(self.sknf_form)
        print(self.num_sknf)
        print(self.bytes_sknf)

    def create_sdnf_form(self):
        sdnf_rows = []
        for i in range(self.rows_size):
            if self.table[i][self.columns_size - 1] is True:
                sdnf_rows.append(i)

        self.sdnf_form = ''
        self.bytes_sdnf = []
        self.num_sdnf = []
        for row in sdnf_rows:
            byte_num = []
            for i in range(len(self.tree.values)):
                byte_num.append(int(self.table[row][i]))
                self.sdnf_form += str(int(self.table[row][i]))
            self.bytes_sdnf.append(byte_num)
            self.num_sdnf.append(convert_to_number(byte_num))
            self.sdnf_form += '+'

        return self.format_sdnf(self.bytes_sdnf)


    def format_sdnf(self, lst):
        result = ""
        for i in lst:
            result +="( "
            for j in range(len(i)):
                if i[j] == 0:
                    result += "!x" + str(j+1) + " * "
                else:
                    result += "x" + str(j+1) + " * "
            result = result[:-2]
            result += ")+"
        return result[:-2]  # удаляем последний "+" из строки

    # ( !x1 * !x2 * !x3 )+( !x1 * !x2 * x3 )+( !x1 * x2 * x3 )+( x1 * x2 * x3 )

    def create_index(self):
        for row in range(1, self.rows_size):
            self.index_byte_form.append(int(self.table[row][self.columns_size - 1]))

        self.index_num_form = convert_to_number(self.index_byte_form)
        print(self.index_byte_form)
        print(self.index_num_form)

    def print_table(self):
        for row in range(self.rows_size):
            for column in range(self.columns_size):
                print(self.table[row][column], end=' | ')
            print()
