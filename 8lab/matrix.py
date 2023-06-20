
def calc_q_and_l(word: list[int], seraching_word: list[int]) -> tuple:
    size: int = len(word)
    g = l = 0
    for i in range(size-1, -1, -1):
        new_g = g or (not seraching_word[i] and word[i] and not l)
        #print(int(new_g), "=", g, "+", "( !", seraching_word[i], "*", word[i], "*", "!", l," )")
        new_l = l or (seraching_word[i] and not word[i] and not g)
        #print(int(new_l), "=", l, "+ (", seraching_word[i], "*", '!', word[i], "*", "!", g, " )")
        g = int(new_g)
        l = int(new_l)
    return (g, l)



class Matrix:
    def __init__(self, dict: list[list[int]]):
        self.base_dict = dict
        self.matrix = self.create_matrix(dict)
        self.print()

    def get_closest_from_above(self, mask) -> list[int]:
        print("Search closest from above...")
        result_dict: list[list[int]] = []
        dict = self.get_dict()
        for word in dict:
            g_and_l = calc_q_and_l(word, mask)
            g = g_and_l[0]
            l = g_and_l[1]
            if g == 1 and l == 0:
                print(word, ">", mask)
                result_dict.append(word)
                print(word, "was added to the results dictionary.")
        return self.find_max_or_min(result_dict, 0)

    def get_closest_from_bottom(self, mask) -> list[int]:
        print("Search closest from bottom...")
        result_dict: list[list[int]] = []
        dict = self.get_dict()
        for word in dict:
            g_and_l = calc_q_and_l(word, mask)
            g = g_and_l[0]
            l = g_and_l[1]
            if l == 1 and g == 0:
                print(word, "<", mask)
                result_dict.append(word)
                print(word, "was added to the results dictionary.")
        return self.find_max_or_min(result_dict, 1)

    def create_matrix(self, dict: list[list[int]]) -> list[list[int]]:
        size: int = len(dict)
        matrix = []
        for i in range(size):
            matrix.append([])
            for j in range(size):
                matrix[i].append(dict[j][i + j * (-1)])
        return matrix

    def find_max_or_min(self, results_dict:list[list[int]], flag: bool):
        if results_dict:
             sorted_dict:list[list[int]] = []
             for i in range(len(results_dict[0]) - 1, 0, -1):
                for word in results_dict:
                    if word[i] == flag and word not in sorted_dict:
                        sorted_dict.append(word)
             if sorted_dict:
                return sorted_dict[0]
             else: return None
        else:
            print("Not found!")

    def add_word(self, word:list[int], place_index: int) -> None:
        print("Set", word, "in place", place_index)
        size = len(self.matrix)
        for i in range(size):
            self.matrix[i + place_index * (-1)][place_index] = word[i]

    def get_word(self, place_index: int) -> list[int]:
        print("Word from", place_index, "is:")
        size = len(self.matrix)
        word: list[int] = []
        for j in range(size):
             word.append(self.matrix[j + place_index - size][place_index])
        return word

    def get_dict(self) -> list[list[int]]:
        size: int = len(self.matrix)
        dict: list[list[int]] = []
        matrix = self.matrix
        for i in range(size):
            dict.append([])
            for j in range(size):
                dict[i].append(matrix[j + i - size][i])
        return dict

    def print(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])
        print()

