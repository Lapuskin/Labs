
class Table_of_truth:

    def build(self, tree):
        n = 1 + 2 ** len(tree.operations)
        m = len(tree.operations) + len(tree.variables)
        matrix = []
        for i in range(0, n):
            matrix.append([])
            for j in range(0, m):
                matrix[i].append(0)

        header = tree.operations + tree.variables
        header.reverse()

        for i in range(0, m):
            matrix[0][i] = ''.join(header[i].expression)



        print(matrix)


