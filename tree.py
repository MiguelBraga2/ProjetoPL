class Tree:
    def __init__(self, type, indentation, value, trees):
        self.type = type
        self.indentation = indentation
        self.value = value
        self.trees = trees


    def print_tree(self):
        print(self.indentation + self.type)
        print(self.indentation + self.value)
        for tree in self.trees:
            tree.print_tree()


