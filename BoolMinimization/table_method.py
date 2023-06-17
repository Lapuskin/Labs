from prettytable import PrettyTable
from calculation_method import *
from tabular_calculation_method import tab_calc_method
import math

def print_map(map, row, column):
    print("Karnaugh Map:")
    print(' x1/x2,x3 ', end='')
    for i in range(len(row)):
        print(str(row[i]), end=' ')
    print()
    for item in range(len(map)):
        print(column[item], end="      ")
        for cell in map[item]:
            print(cell, end='      ')
        print()


def table_method(func, table, bool_val=1):
    # создание карты

    map = []
    variables_count = int(math.log(len(table) - 1, 2))
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
            if left_gray_code[i] + top_gray_code[j] in clasters:
                map[i][j] = 1

    selected_area = [[], []]
    print_map(map, top_gray_code, left_gray_code)

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
                if i - 1 < 0:
                    dif_i += map_row_size - 1
                rect = {(i, j), (dif_i - 1, j)}
                selected_area[1].append(rect)
            if map[i][j] == 1 & map[i][j - 1] == 1:
                dif_j = j
                if j - 1 < 0:
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
    ltable = in_pdnf(
        tab_calc_method(*glue_implicants(func)))

    # for figure in range(len(min_selected_area)):
    #     for tup1 in min_selected_area[figure]:
    #         for tup2 in min_selected_area[figure]:
    #             if tup1 != tup2 and any(elem in tup2 for elem in tup1):
    #                 min_selected_area[figure].remove(tup1)


    if selected_area:
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
    else:
        return(ltable)
    print()

def gray_code(n):
    if n == 0:
        return ['']
    lower_gray = gray_code(n - 1)
    return ['0' + code for code in lower_gray] + ['1' + code for code in reversed(lower_gray)]


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



def create_table(amount_values, formula, table_data, form_of_formula):
    amount_rows = len(amount_values) // 2
    amount_columns = len(amount_values) - amount_rows
    table = PrettyTable()
    rows = create_line(amount_rows, amount_values[:amount_rows])
    columns = create_line(amount_columns, amount_values[-amount_columns:])
    table.field_names = [f'{"".join(amount_values[:amount_rows])}/{"".join(amount_values[-amount_columns:])}',
                         *[''.join(map(str, i)) for i in transform_dict_in_list(columns)]]
    table_in_list_form = transform_dict_for_table(table_data)
    temp_table, index_for_insert_cell = [], -1
    for i in rows:
        temp_table.append([])
        index_for_insert_cell += 1
        output = []
        for j in columns:
            temp_row = i | j
            for k in table_in_list_form:
                if temp_row in k:
                    temp_table[index_for_insert_cell].append((temp_row, k[1]))
                    output.append(k[1])
                    break
        table.add_row([''.join(map(str, list(i.values()))), *output])
    print(table)
    return temp_table


def transform_dict_for_table(table_data):
    table = []
    for i in table_data:
        table.append([{j: k for j, k in i.items() if j !=
                     'i' and j != 'f'}, list(i.values())[-2]])
    return table


def transform_dict_in_list(table_data):
    dict_in_list = []
    for i in table_data:
        dict_in_list.append(list(i.values()))
    return dict_in_list


def create_line(amount_arguments, values):
    line = [{i: 0 for i in values}]
    for i in range(1, 2**amount_arguments):
        for j in range(amount_arguments - 1, -1, -1):
            line_in_table = line[i - 1].copy()
            index = list(line_in_table.keys())[j]
            line_in_table[index] = 0
            if line_in_table not in line:
                line.append(line_in_table)
                break
            line_in_table[index] = 1
            if line_in_table not in line:
                line.append(line_in_table)
                break
    return line


def minimize_function(table_data, form_of_formula):
    if check_all_in_group(table_data, 1 * (form_of_formula == 'pdnf')):
        return [table_data]
    array_of_groups = [[]]
    for i in range(0, len(table_data)):
        for j in range(0, len(table_data[i])):
            choose_group(check_four_group(table_data, i, j, 1 * (form_of_formula == 'pdnf')),
                         array_of_groups,
                         table_data[i][j])
    array_of_groups.append([])
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            if all(check_one_group(table_data, i, j,
                   1 * (form_of_formula == 'pdnf'))):
                array_of_groups[-1].append((table_data[i][j], ))
    array_of_groups.append([])
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            group_result = check_two_group(
                table_data, i, j, 1 * (form_of_formula == 'pdnf'))
            choose_group(group_result, array_of_groups, table_data[i][j])
    return array_of_groups


def choose_group(group_result, array_of_groups, current_element):
    all_elements = [k for i in array_of_groups for j in i for k in j]
    if len(group_result) == 0:
        return
    if current_element not in all_elements or len(group_result[0]) == 4:
        for i in group_result:
            if (i not in all_elements and i not in array_of_groups[-1]) or len(
                    group_result) == 1:
                if isinstance(group_result[0][0], tuple):
                    array_of_groups[-1].append(i)
                else:
                    array_of_groups[-1].append((current_element, i))


def check_one_group(table_data, current_row, current_column, form_of_formula):
    top, bottom, left, right = False, False, False, False
    if table_data[current_row][current_column][1] == form_of_formula:
        if current_column != len(table_data[current_row]) - 1:
            if table_data[current_row][current_column + 1][1] != form_of_formula:
                right = True
        elif table_data[current_row][0][1] != form_of_formula:
            right = True
        if current_column != 0:
            if table_data[current_row][current_column - 1][1] != form_of_formula:
                left = True
        elif table_data[current_row][len(table_data[current_row]) - 1][1] != form_of_formula:
            left = True
        if current_row != 0:
            if table_data[current_row - 1][current_column][1] != form_of_formula:
                top = True
        else:
            top = True
        if current_row != len(table_data) - 1:
            if table_data[current_row + 1][current_column][1] != form_of_formula:
                bottom = True
        else:
            bottom = True
    return [top, bottom, left, right]


def check_two_group(table_data, current_row, current_column, form_of_formula):
    answer = []
    if table_data[current_row][current_column][1] == form_of_formula:
        if current_column != len(table_data[current_row]) - 1:
            if table_data[current_row][current_column + 1][1] == form_of_formula:
                answer.append(table_data[current_row][current_column + 1])
        elif table_data[current_row][0][1] == form_of_formula:
            answer.append(table_data[current_row][0])
        if current_column != 0:
            if table_data[current_row][current_column - 1][1] == form_of_formula:
                answer.append(table_data[current_row][current_column - 1])
        elif table_data[current_row][len(table_data[current_row]) - 1][1] == form_of_formula:
            answer.append(table_data[current_row]
                          [len(table_data[current_row]) - 1])
        if current_row != 0:
            if table_data[current_row - 1][current_column][1] == form_of_formula:
                answer.append(table_data[current_row - 1][current_column])
        if current_row != len(table_data) - 1:
            if table_data[current_row + 1][current_column][1] == form_of_formula:
                answer.append(table_data[current_row + 1][current_column])
    return answer


def check_four_group(table_data, current_row, current_column, form_of_formula):
    elements_in_group = []
    if table_data[current_row][current_column][1] == form_of_formula:
        if current_column == 0:
            group_of_elements = []
            for i in range(current_column, len(table_data[current_row])):
                if table_data[current_row][i][1] == form_of_formula:
                    group_of_elements.append(table_data[current_row][i])
                else:
                    break
            if table_data[current_row][0][1] == form_of_formula:
                for i in range(0, current_column):
                    if table_data[current_row][i][1] == form_of_formula:
                        group_of_elements.append(table_data[current_row][i])
                    else:
                        break
            if len(group_of_elements) == 4:
                elements_in_group.append(tuple(group_of_elements))
        elements_in_group += check_four_group_in_square(
            table_data, current_row, current_column, form_of_formula)
    return elements_in_group


def check_four_group_in_square(
        table_data,
        current_row,
        current_column,
        form_of_formula):
    elements_in_group = []
    if table_data[current_row][current_column][1] == form_of_formula:
        if current_row == 0:
            if current_column != len(table_data[current_row]) - 1:
                if table_data[current_row][current_column + 1][1] == form_of_formula \
                    and table_data[current_row + 1][current_column][1] == form_of_formula \
                        and table_data[current_row + 1][current_column + 1][1] == form_of_formula:
                    elements_in_group.append((table_data[current_row][current_column],
                                              table_data[current_row][current_column + 1],
                                              table_data[current_row + 1][current_column],
                                              table_data[current_row + 1][current_column + 1]))
            else:
                if table_data[current_row][0][1] == form_of_formula \
                    and table_data[current_row + 1][current_column][1] == form_of_formula \
                        and table_data[current_row + 1][0][1] == form_of_formula:
                    elements_in_group.append((table_data[current_row][current_column],
                                              table_data[current_row + 1][current_column],
                                              table_data[current_row][0],
                                              table_data[current_row + 1][0]))
    return elements_in_group


def build_implicants(data_about_argument, current_element):
    for x in range(len(current_element)):
        for k in current_element[x][0].items():
            if x == 0:
                data_about_argument[k[0]] = (True, k[1])
            elif data_about_argument[k[0]][0]:
                data_about_argument[k[0]] = (
                    bool(True * (not data_about_argument[k[0]][1] != k[1])), k[1])
    return data_about_argument


def check_all_in_group(table_data, form_of_formula):
    for i in table_data:
        for j in i:
            if j[1] != form_of_formula:
                return False
    return True


def build_pdnf(group_of_arguments):
    create_implicat = []
    data_about_argument = dict()
    for i in group_of_arguments:
        for j in i:
            data_about_argument = build_implicants(data_about_argument, j)
            create_implicat.append(['!' * (x[1][1] == 0) + x[0]
                                   for x in data_about_argument.items() if x[1][0]])
    temp_create_implicat = deepcopy(create_implicat)
    for i in temp_create_implicat:
        if create_implicat.count(i) > 1:
            create_implicat.remove(i)
    return create_implicat


def build_pcnf(group_of_arguments):
    create_implicat = []
    data_about_argument = dict()
    for i in group_of_arguments:
        for j in i:
            data_about_argument = build_implicants(data_about_argument, j)
            create_implicat.append(['!' * (x[1][1] == 1) + x[0]
                                   for x in data_about_argument.items() if x[1][0]])
    temp_create_implicat = deepcopy(create_implicat)
    for i in temp_create_implicat:
        if create_implicat.count(i) > 1:
            create_implicat.remove(i)
    return create_implicat
