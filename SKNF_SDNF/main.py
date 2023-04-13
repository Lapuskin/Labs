from table_of_truth import Table_of_truth
from tree import Tree


def main():
    expression = "!((A+B)*(B+C))"
    tree = Tree(expression)
    tree.build()
    table = Table_of_truth()
    table.build(tree)
    table.create_sknf_form()
    table.create_sdnf_form()
    table.create_index()


if __name__ == '__main__':
    main()
