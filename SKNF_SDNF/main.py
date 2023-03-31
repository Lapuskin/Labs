from table_of_truth import Table_of_truth
from tree import Tree


def main():
    expression = "A * (B + !C)"
    tree = Tree(expression)
    tree.build()
    table = Table_of_truth()
    table.build(tree)
    table.print()

if __name__ == '__main__':
    main()