import random

WORD_LEN = 10
DISCHARGE_LEN = 4
SERACH_WORD_INDEX = 4
TOP_LINE = 7
BOTTOM_LINE = 2

def quick_sort(dict: list[list[int]]) -> list[list[int]]:
    if len(dict) <= 1:
        return dict
    pivot = dict[0]
    left = []
    right = []
    for i in range(1, len(dict)):
        q_and_l = calc_q_and_l(dict[i], pivot)
        if q_and_l[0] == 0 and q_and_l[1] == 1:
            left.append(dict[i])
        else:
            right.append(dict[i])
    return quick_sort(left) + [pivot] + quick_sort(right)


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

def find_in_interval(top_line: int, bottom_line: int,
                     dict: list[list[int]], search_word: list[int]) -> None:
    print('№2 find in interval', bottom_line, ":", top_line)
    find(dict[bottom_line : top_line], search_word)


def find(dict: list[list[int]], searching_word: list[int]):
    for word in dict:
        g_and_l = calc_q_and_l(word, searching_word)
        g = g_and_l[0]
        l = g_and_l[1]
        if l == g == 0:
            print(word, "==", searching_word)
        elif g == 1 and l == 0:
            print(word, ">", searching_word)
        elif l == 1 and g == 0:
            print(word, "<", searching_word)
        else:
            print("That's imposible!!")


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
    search_word = dict[SERACH_WORD_INDEX]
    find(dict, search_word)
    print()
    find_in_interval(TOP_LINE, BOTTOM_LINE, dict, search_word)
    print()
    res = quick_sort(dict)
    print("№3 sorted list", "\n", res)


if __name__ == '__main__':
    main()
