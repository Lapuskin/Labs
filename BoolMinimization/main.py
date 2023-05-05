def main():
    '''    expression_table = [["A", "B", "C", "F"],
                        [ 0,   0,   0,   0],
                        [ 0,   0,   1,   1],
                        [ 0,   1,   0,   1],
                        [ 0,   1,   1,   0],
                        [ 1,   0,   0,   1],
                        [ 1,   0,   1,   0],
                        [ 1,   1,   0,   0],
                        [ 1,   1,   1,   1]]
    '''
    expression_table = [["A", "B", "C", "F"],
                        [0, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 1, 0, 1],
                        [0, 1, 1, 1],
                        [1, 0, 0, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]
    mini(expression_table)


def mini(table):
    makklasky(table, 1)
    print(' ')
    karno(table, 1)
    print(' ')
    analytik(table, 1)



def analytik(table, bool_val):
        snf = create_snf(table, bool_val)
        min_snf = []
        if snf:
            for cur_kit_place in range(len(snf)):
                for mapping_kit_place in range(1, len(snf)):
                    counter = 0
                    kit = []
                    for i in range(len(snf[0])):
                        for j in range(len(snf[0])):
                            if snf[cur_kit_place][i] == snf[mapping_kit_place][j]:
                                counter += 1
                                kit.append(snf[cur_kit_place][i])
                    if counter == len(snf[cur_kit_place]) - 1:
                        min_snf.append(kit)
        for kit in min_snf:
            print(kit, end='')
            print('+', end='')





def create_snf(table, bool_val):
    snf = []

    for i in range(1, len(table)):
        kit = []
        if table[i][-1] is bool_val:
            for j in range(len(table[0]) - 1):
                if table[i][j] != bool_val:
                    kit.append('~'+table[0][j])
                else:
                    kit.append(table[0][j])
            snf.append(kit)
    return snf



def partition(table, bool_val):
    constituents = []
    row_size = len(table)
    column_size = len(table[0])

    for row in range(row_size):
        if table[row][column_size - 1] == bool_val:
            constituent = []
            for i in range(column_size - 1):
                constituent.append(table[row][i])
            constituents.append(constituent)
    return constituents


def karno(table, bool_val):
    # создание карты
    map = []
    variables_count = len(table[0]) - 1
    vars_left = variables_count % 2
    vars_top = variables_count - (variables_count % 2)
    map_row_size = 2 ** vars_left + 1
    map_column_size = 2 ** vars_top + 1

    clasters = partition(table, bool_val)

    top_gray_code = gray_code(vars_top)
    left_gray_code = gray_code(vars_left)

    for i in range(len(top_gray_code)):
        for j in range(len(top_gray_code[0])):
            top_gray_code[i] = list(top_gray_code[i])
            top_gray_code[i][j] = int(top_gray_code[i][j])
    for i in range(len(left_gray_code)):
        for j in range(len(left_gray_code[0])):
            left_gray_code[i] = list(left_gray_code[i])
            left_gray_code[i][j] = int(left_gray_code[i][j])
    for i in range(map_row_size - 1):
        map.append([])
        for j in range(map_column_size - 1):
            map[i].append(0)

    for i in range(map_row_size - 1):
        for j in range(map_column_size - 1):
            if top_gray_code[j] + left_gray_code[i] in clasters:
                map[i][j] = 1

    selected_area = [[], []]
    counter = 0
    for i in range(map_row_size - 1):
        for j in range(map_column_size - 1):
            if map[i][j] == 1:
                counter += 1
    if counter == (map_row_size - 1) * (map_column_size - 1):
        print("just!")
    elif counter == 0:
        print("no min")

    for i in range(map_row_size - 1):
        for j in range(map_column_size - 1):
            if map[i][j] == 1 & map[i - 1][j] == 1 & map[i - 1][j - 1] == 1 & map[i][j - 1] == 1:
                dif_i = i
                dif_j = j
                if i - 1 < 0:
                    dif_i += map_row_size - 1
                if j - 1 < 0:
                    dif_j += map_column_size - 1
                square = {(i, j), (dif_i - 1, j), (dif_i - 1, dif_j - 1), (i, dif_j - 1)}
                selected_area[0].append(square)

    for i in range(map_row_size - 1):
        for j in range(map_column_size - 1):
            if map[i][j] == 1 & map[i - 1][j] == 1:
                dif_i = i
                if i-1 < 0:
                    dif_i += map_row_size - 1
                rect = {(i, j), (dif_i - 1, j)}
                selected_area[1].append(rect)
            if map[i][j] == 1 & map[i][j - 1] == 1:
                dif_j = j
                if j-1 < 0:
                    dif_j += map_column_size - 1
                rect = {(i, j), (i, dif_j - 1)}
                selected_area[1].append(rect)
    min_selected_area = [[], []]
    for layer in range(len(selected_area)):
        for figure in selected_area[layer]:
            if figure not in min_selected_area[layer]:
                min_selected_area[layer].append(figure)
    selected_area = [min_selected_area[0], []]
    if min_selected_area[0]:
        for square in min_selected_area[0]:
            for rect in min_selected_area[1]:
                if not rect <= square:
                    selected_area[1].append(rect)
    else:
        selected_area[1] = min_selected_area[1]

    for layer in selected_area:
        for figure in layer:
            figure = list(figure)
            priority = []
            for i in range(variables_count):
                priority.append(0)
            for block in range(1, len(figure)):
                back_block = []
                for index in range(variables_count):
                    back_block = top_gray_code[figure[block - 1][1]] + left_gray_code[figure[block - 1][0]]
                    cur_block = top_gray_code[figure[block][1]] + left_gray_code[figure[block][0]]
                    if cur_block[index] == back_block[index]:
                        priority[index] += 1
            max = priority[0]
            for i in range(len(priority)):
                if priority[i] > max: max = priority[i]
            for i in range(len(priority)):

                if priority[i] == max:
                    if cur_block[i] != bool_val:
                        print("~", end='')
                    print(table[0][i], end='')
            print('+', end='')


def gray_code(n):
    if n == 0:
        return ['']
    lower_gray = gray_code(n - 1)
    return ['0' + code for code in lower_gray] + ['1' + code for code in reversed(lower_gray)]


def makklasky(table, bool_val):
    constituents = []
    constituents_layers = []
    iplicants_layer = []
    row_size = len(table)
    column_size = len(table[0])
    for i in range(column_size):
        constituents_layers.append([])
        iplicants_layer.append([])
    iplicants_layer.pop()
    # разбиение на конституэнты и по слоям

    constituents = partition(table, bool_val)

    for constituent_tuple in constituents:
        group_id = 0
        for item in constituent_tuple:
            if item == bool_val:
                group_id += 1
        constituents_layers[group_id].append(constituent_tuple.copy())

    for layer_number in range(len(constituents_layers) - 1):
        if constituents_layers[layer_number] and constituents_layers[layer_number + 1]:
            for i in range(len(constituents_layers[layer_number])):
                for j in range(len(constituents_layers[layer_number + 1])):
                    ineq_count = 0
                    place = 0
                    for element in range(column_size - 1):
                        if constituents_layers[layer_number][i][element] != constituents_layers[layer_number + 1][j][
                            element]:
                            place = element
                            ineq_count += 1
                    if ineq_count == 1:
                        iplicants_layer[place].append(constituents_layers[layer_number][i].copy())
                        iplicants_layer[place][-1][place] = "*"

    final_iplicants = []
    for layer in iplicants_layer:
        if len(layer) == 1:
            final_iplicants.append(layer[0])
        elif len(layer) > 1:
            for i in range(len(layer)):
                for j in range(i + 1, len(layer)):
                    for sign in range(column_size - 1):
                        if layer[i][sign] != layer[j][sign]:
                            final_iplicants.append(layer[i].copy())
                            final_iplicants[-1][sign] = "*"
    if not final_iplicants:
        for constituent in constituents:
            final_iplicants.append(constituent)

    tuple_list = [tuple(implicant) for implicant in final_iplicants]
    my_set = set(tuple_list)
    iplicants = [list(x) for x in my_set]

    for iplicant in iplicants:
        for element in range(len(iplicant)):
            if iplicant[element] != bool_val:
                if iplicant[element] != "*":
                    elem = table[0][element]
                    print("(~" + elem + ")", end='')
            else:
                print(table[0][element], end='')

        if bool_val == 1:
            print("+", end='')
        else:
            print("*", end='')


if __name__ == '__main__':
    main()
