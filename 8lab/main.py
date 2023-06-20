import random


from matrix import Matrix

WORD_LEN = 16
DISCHARGE_LEN = 16
SERACH_WORD_INDEX = 1
TOP_LINE = 7
BOTTOM_LINE = 2
NEW_WORD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def f1(first, second):
    res: list[int] = []
    for i in range(len(first)):
        res.append(int(first[i] and second[i]))
    return res

def f12(first):
    res: list[int] = []
    for i in range(len(first)):
        res.append(int(not first[i]))
    return res

def f14(first, second):
    return f12(f1(first, second))

def f3(first):
    return first

def gen_dict(word_len: int, discharge_len: int) -> list:
    # генерация случайного двоичного массива
    memory: list[list[int]] = []
    for i in range(word_len):
        word:list[int] = []
        for j in range(discharge_len):
            bit = random.randint(0, 1)
            word.append(int(bit))
        memory.append(word)
    return memory


def main():
    dict: list[list[int]] = gen_dict(WORD_LEN, DISCHARGE_LEN)
    print(dict)
    search_word = dict[SERACH_WORD_INDEX]
    matrix = Matrix(dict)
    print("From matrix to dict")
    print(matrix.get_dict())
    matrix.add_word(NEW_WORD, 0)
    matrix.print()

    print(matrix.get_word(2))
    print()
    print("for", search_word, "closest from bottom ->", matrix.get_closest_from_bottom(search_word))
    print()
    print("for", search_word, "closest from above ->", matrix.get_closest_from_above(search_word))
    print()
    print( "for", matrix.get_word(2),"and", matrix.get_word(4))
    print("and", f1(matrix.get_word(2), matrix.get_word(4)))
    print("not (and)", f14(matrix.get_word(2), matrix.get_word(4)))
    print("not x1", f12(matrix.get_word(2)))


if __name__ == '__main__':
    main()
