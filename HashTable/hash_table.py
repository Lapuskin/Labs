class Hash_table:

    def __init__(self, n):
        self.array = [[] for i in range(0, n)]
        self.n = n

    def polynomial_hash(self, s, p=31, m=1e9 + 9):
        hash_value = 0
        p_pow = 1
        for c in s:
            hash_value = (hash_value + (ord(c) - ord('a') + 1) * p_pow) % m
            p_pow = (p_pow * p) % m
        return hash_value

    def app(self, value):
        hash_index = self.polynomial_hash(value[0], 31, self.n)
        self.array[hash_index].append(value)

    def find(self, value):
        hash_index = self.polynomial_hash(value[0], 31, self.n)
        for val in self.array[hash_index]:
            if val == value:
                return hash_index
        return None

    def rem(self, value):
        hash_index = self.polynomial_hash(value[0], 31, self.n)
        for val in self.array[hash_index]:
            if val == value:
                self.array[hash_index].remove(value)
                return True
        return False

    def show_table(self):
        print()
        for row in range(self.n):
            print(row, self.array[row])
        print()

