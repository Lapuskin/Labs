from copy import deepcopy

def check_size(formula):
    if len(formula) > 0:
        size = len(formula[0])
    else:
        return False
    for i in formula:
        if len(i) != size:
            return False
    return True


def calaculation_method(formula):
    if len(formula) == 0:
        return '-'
    formula_after_glue, base_formula, form_of_formula = glue_implicants(formula)
    formula_after_glue_again = formula_after_glue
    while True:
        size = len(formula_after_glue_again)
        formula_after_glue_again, base_formula, form_of_formula = two_imp_connect(
            formula_after_glue_again, form_of_formula)
        if len(formula_after_glue_again[0]) == 1:
            formula_in_list = set([j for i in formula_after_glue_again for j in i])
            formula_in_list = del_extra_args(list(formula_in_list))
            return formula_in_list
        if size == len(formula_after_glue_again):
            break
        size_of_implicat = len(formula_after_glue_again[0])
        for i in formula_after_glue_again:
            if len(i) != size_of_implicat:
                temp_formula_after_glue_again = deepcopy(formula_after_glue_again)
                for i in temp_formula_after_glue_again:
                    if formula_after_glue_again.count(i) > 1:
                        formula_after_glue_again.remove(i)
                return rem_extra_impl(formula_after_glue_again, form_of_formula)
    return rem_extra_impl(formula_after_glue, form_of_formula)


def del_extra_args(formula):
    temp = deepcopy(formula)
    for i in formula:
        if i in temp and '!' + i in temp:
            temp.remove(i)
            temp.remove('!' + i)
    return [[i] for i in temp]


def glue_implicants(formula):
    if ')+(' in formula or ' * ' in formula:
        form_of_formula = 'pdnf'
    elif ')*(' in formula or ' + ' in formula:
        form_of_formula = 'pcnf'
    else:
        form_of_formula = ''
    tempalte_for_delete = ['(', ')', '+', '*']
    formula_without_extra_characters = [[]]
    formula = [i * (not (i == ')+(' or i == ')*('))
               or ' ' for i in formula.split() if i not in tempalte_for_delete]
    index_of_space = 0

    for i in formula:
        if i == ' ':
            formula_without_extra_characters.append([])
            index_of_space += 1
        else:
            formula_without_extra_characters[index_of_space].append(i)
    return two_imp_connect(
        formula_without_extra_characters,
        form_of_formula)




def replace_arguments_on_0_1_pdnf(temp_formula, current_implicat, formula):
    values_of_arguments = dict()
    for j in range(len(formula[current_implicat])):
        values_of_arguments[formula[current_implicat][j]] = '1'
        if temp_formula[current_implicat][j][0] == 'x':
            values_of_arguments['!' + formula[current_implicat][j]] = '0'
        else:
            values_of_arguments[formula[current_implicat][j][1:]] = '0'
        temp_formula[current_implicat][j] = '1'
    return (temp_formula, values_of_arguments)


def connect_arguments(first_implicat, second_implicant):
    glued_arguments = []
    for i in range(len(first_implicat)):
        if first_implicat[i] == second_implicant[i]:
            glued_arguments.append(first_implicat[i])
    return glued_arguments



def replace_arguments_on_0_1_pcnf(temp_formula, current_implicat, formula):
    values_of_arguments = dict()
    for j in range(len(formula[current_implicat])):
        values_of_arguments[formula[current_implicat][j]] = '0'
        if temp_formula[current_implicat][j][0] == 'x':
            values_of_arguments['!' + formula[current_implicat][j]] = '1'
        else:
            values_of_arguments[formula[current_implicat][j][1:]] = '1'
        temp_formula[current_implicat][j] = '0'
    return (temp_formula, values_of_arguments)


def rem_extra_impl(expr, form_of_expr):
    after_formula = []
    if len(expr) == 1 or len(expr[0]) == 1:
        return expr
    for i in range(len(expr)):
        temp = deepcopy(expr)
        if form_of_expr == 'pdnf':
            temp, vals_of_args = replace_arguments_on_0_1_pdnf(
                temp, i, expr)
        else:
            temp, vals_of_args = replace_arguments_on_0_1_pcnf(
                temp, i, expr)
        for j in range(len(temp)):
            for z in range(len(temp[j])):
                if temp[j][z] in vals_of_args:
                    temp[j][z] = vals_of_args[temp[j][z]]
        if cut_back_args(temp, form_of_expr):
            after_formula.append(expr[i])
    return after_formula


def check_on_extra_implicants_pdnf(cut_back_formula):
    temp_expression = ''
    temp_cut_back_formula = deepcopy(cut_back_formula)
    for i in cut_back_formula:
        if str(i).isdigit():
            continue
        if i[0] != '!' and '!' + i in temp_cut_back_formula:
            temp_cut_back_formula.remove(i)
            temp_cut_back_formula.remove('!' + i)
            temp_expression = '1'
    for i in temp_cut_back_formula:
        temp_expression = logic_or(i, temp_expression)

    if temp_expression == '1':
        return True
    return False



def two_imp_connect(expr, form_of_expr):
    formula_after_glue, append_later, use_implicats, differense = [], [], [], []
    if not check_size(expr) or len(expr) == 1:
        return  (expr, expr, form_of_expr)
    for i in range(0, len(expr) - 1):
        formula_size = len(formula_after_glue)
        for k in range(i + 1, len(expr)):
            for j in range(0, len(expr[i])):
                if expr[i][j] != expr[k][j]:
                    differense.append((expr[i][j], expr[k][j]))
            if len(differense) == 1 and differense[0][0][-1] == differense[0][1][-1]:
                formula_after_glue.append(
                    connect_arguments(expr[i], expr[k]))
                use_implicats.append(expr[k])
            differense.clear()
        if len(formula_after_glue) == formula_size and expr[i] not in use_implicats:
            append_later.append(expr[i])
    if len(formula_after_glue) == 0:
        return (expr, expr, form_of_expr)
    else:
        formula_after_glue = append_later + formula_after_glue + ([expr[-1]] \
            if expr[-1] not in use_implicats else [])
    return (formula_after_glue, expr, form_of_expr)


def check_on_extra_pcnf(cut_back_formula):
    for i in cut_back_formula:
        if i[0] != '!' and '!' + i in cut_back_formula:
            return True
    return False

def logic_and(first_argument, second_argument):
    if first_argument == second_argument:
        return first_argument
    if first_argument.isdigit() and second_argument.isdigit():
        return str(int(first_argument) and int(second_argument))
    if first_argument[0] == 'x' or first_argument[0] == '!':
        if second_argument == '1':
            return first_argument
        else:
            return '0'
    else:
        if first_argument == '1':
            return second_argument
        else:
            return '0'



def cut_back_args(temp, form):
    formula_after_open_staples = []
    for i in temp:
        if ''.join(i).isdigit():
            continue
        expression_in_staples = i[0]
        for j in i[1:]:
            if form != 'pdnf':
                expression_in_staples = logic_or(expression_in_staples, j)
            else:
                expression_in_staples = logic_and(expression_in_staples, j)
        formula_after_open_staples.append(expression_in_staples)
    if form == 'pdnf':
        if check_on_extra_implicants_pdnf(formula_after_open_staples):
            return []
        else:
            return True
    else:
        if check_on_extra_pcnf(formula_after_open_staples):
            return []
        else:
            return True



def in_pdnf(expr):
    output = []
    if isinstance(expr, str):
        print(expr)
        return
    elif len(expr) == 0:
        print(0)
        return
    if len(expr[0]) == 1:
        output.append('(')
    for i in expr:
        if len(i) != 1:
            implicat = f'({" * ".join(i)})+'
        else:
            implicat = f'{" * ".join(i)}+'
        output.append(implicat)
    if len(expr[0]) == 1:
        output[-1] = output[-1][:-1] + ')'
        print(''.join(output))
    else:
        print(''.join(output)[:-1])



def logic_or(first, second):
    if first == second:
        return first
    if second.isdigit() and first.isdigit():
        return str(int(first) or int(second))
    if first[0] == 'x' or first[0] == '!':
        if second == '1':
            return '1'
        else:
            return first
    else:
        if first != '1':
            return second
        else:
            return '1'
