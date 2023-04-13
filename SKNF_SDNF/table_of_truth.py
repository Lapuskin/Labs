

class Table_of_truth:
    matrix=[]
    rows_size = 0
    columns_size = 0
    sknf_form = []
    sdnf_form = []
    index_byte_form = []
    index_num_form = 0

    def build(self, tree):
        self.tree = tree
        self.rows_size = 1 + 2 ** len(tree.variables)
        self.columns_size = len(tree.operations) + len(tree.variables)
        self.matrix = []
        for i in range(0, self.rows_size):
            self.matrix.append([])
            for j in range(0, self.columns_size):
                self.matrix[i].append(False)

        tree.variables.reverse()
        tree.operations.reverse()
        self.header = tree.variables + tree.operations


        for i in range(0, self.columns_size):
            self.matrix[0][i] = ''.join(self.header[i].expression)

        self.calc()

    def calc(self):
        offset = 1
        for i in range(len(self.tree.variables) - 1, -1, -1):
            j = 1
            while j < self.rows_size:
                for elem in range(offset):
                    self.matrix[j][i] = False
                    j += 1
                if j != self.rows_size:
                    for elem in range(offset):
                        self.matrix[j][i] = True
                        j += 1
            offset = 2 ** (len(self.tree.variables) - i)

        for i in range(1, self.rows_size):
            for j in range(len(self.tree.variables)):
                self.tree.variables[j].set_value(self.matrix[i][j])
            self.tree.calc()
            for j in range(len(self.tree.variables), self.columns_size):
                self.matrix[i][j] = self.tree.operations[j - len(self.tree.variables)].value

        self.print_table()


    def create_sknf_form(self):
        sknf_rows = []
        for i in range(self.rows_size):
            if self.matrix[i][self.columns_size - 1] is False:
                sknf_rows.append(i)

        self.sknf_form = ''
        self.bytes_sknf = []
        self.num_sknf = []
        for row in sknf_rows:
            byte_num = []
            for i in range(len(self.tree.variables)):
                byte_num.append(int(self.matrix[row][i]))
                self.sknf_form += str(int(self.matrix[row][i]))
            self.sknf_form += '*'
            self.bytes_sknf.append(byte_num)
            self.num_sknf.append(self.convert_to_number(byte_num))

        print(self.sknf_form)
        print(self.num_sknf)
        print(self.bytes_sknf)

    def create_sdnf_form(self):
        sdnf_rows = []
        for i in range(self.rows_size):
            if self.matrix[i][self.columns_size - 1] is True:
                sdnf_rows.append(i)

        self.sdnf_form = ''
        self.bytes_sdnf = []
        self.num_sdnf = []
        for row in sdnf_rows:
            byte_num = []
            for i in range(len(self.tree.variables)):
                byte_num.append(int(self.matrix[row][i]))
                self.sdnf_form += str(int(self.matrix[row][i]))
            self.bytes_sdnf.append(byte_num)
            self.num_sdnf.append(self.convert_to_number(byte_num))
            self.sdnf_form += '+'

        print(self.sdnf_form)
        print(self.num_sdnf)
        print(self.bytes_sdnf)

    def create_index(self):
        for row in range(1, self.rows_size):
            self.index_byte_form.append(int(self.matrix[row][self.columns_size - 1]))

        self.index_num_form = self.convert_to_number(self.index_byte_form)
        print(self.index_byte_form)
        print(self.index_num_form)

    def convert_to_number(self, bytes_array):
        index = 0
        result = 0
        bytes_array.reverse()
        for bit in bytes_array:
            result += bit * 2 ** index
            index += 1
        bytes_array.reverse()
        return result


    def print_table(self):
        for row in range(self.rows_size):
            for column in range(self.columns_size):
                print(self.matrix[row][column], end=' | ')
            print()