from table_of_truth import Table_of_truth
from tree import Tree
from tabular_calculation_method import *
from table_method import *

def main():
    expression = "!((A + B)*(!C))"
    tree = Tree(expression)
    tree.build()
    table = Table_of_truth()
    table.build(tree)
    table.create_min_table()
    expr = table.create_sdnf_form()
    mini(table.min_table, expr)

def mini(table, expression):
    print("Calculation method:")
    in_pdnf(calaculation_method(expression))
    print('\n')
    print("MakKlassky method: ")
    in_pdnf(
        tab_calc_method(*glue_implicants(expression)))
    print('\n')
    print("Karnaugh method:")
    table_method(expression, table)
    print('\n')

def create_snf(table, bool_val):
    snf = []

    for i in range(1, len(table)):
        kit = []
        if table[i][-1] is bool_val:
            for j in range(len(table[0]) - 1):
                if table[i][j] != bool_val:
                    kit.append('~' + table[0][j])
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




if __name__ == '__main__':
    main()
