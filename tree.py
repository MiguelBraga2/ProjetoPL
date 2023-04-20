class Tree:
    def __init__(self, type, indentation, value, trees):
        self.type = type
        self.indentation = indentation
        self.value = value
        self.trees = trees


    def print_tree(self):
        #print(self.indentation + self.type)
        print(self.indentation + self.value + '(')
        for tree in self.trees:
            tree.print_tree()

        print(')')

    def to_html(self):
        str = ""
        if self.type == 'tags':
            for tree in self.trees:
                str += tree.to_html()
        
        
        # tag : TAG attributes content INDENT tags DEDENT 
        elif self.type == 'tag1':
            str = '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() + self.trees[3].to_html() +\
                    self.trees[4].to_html() + self.trees[5].to_html() + \
                   '</' + self.trees[0].to_html() + '>'
        # tag : TAG attributes content 
        elif self.type == 'tag2':
            str = '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() + '</' + self.trees[0].to_html() + '>'
        # tag: TAG attributes BAR
        elif self.type == 'tag3':
            str = '<' + self.trees[0].to_html() + '/>'
        elif self.type == 'TAG':
            return self.value
        elif self.type == 'attributes':
            for tree in self.trees:
                str += tree.to_html()
        # pug_attributes : pug_attributes sep pug_attribute
        #                | pug_attribute
        elif self.type == 'pug_attributes':
            for tree in self.trees:
                str += tree.to_html() 
        elif self.type == 'pug_sep_attribute':
            str = self.trees[0].to_html() + self.trees[1].to_html()
        elif self.type == 'sep':
            str = ""
        elif self.type == 'COMMA':
            str = ", "
        elif self.type == 'pug_attribute':
            str = " " + self.trees[0].to_html() + self.trees[1].to_html() + self.trees[2].to_html()
        elif self.type == 'ATTRIBUTENAME':
            str = self.value
        elif self.type == 'EQUALS':
            str = self.value
        elif self.type == 'STRING' or self.type == 'BOOLEAN' or self.type == 'NUMBER':
            str = self.value
        # class : class CLASS 
        #       | 
        elif self.type == 'class':
            if len(self.trees) > 0:
                str += ' class="'
                for tree in self.trees:
                    str += tree.to_html() + ' '
                str += '"'
        elif self.type == 'CLASS':
            str += self.value
        # id : 
        
        elif self.type == 'id':
            pass
        elif self.type == 'ID':
            str += " " + "id=" + self.value
        elif self.type == 'content1':
            pass
        # content : text
        elif self.type == 'content2':
            str = self.trees[0].to_html()
        # interpolation : STRING
        elif self.type == 'interpolation1':
            pass
        # interpolation : VARIABLE
        elif self.type == 'interpolation2':
            pass
        elif self.type == 'text1':
            pass
        elif self.type == 'text2':
            pass
        elif self.type == 'text':
            for tree in self.trees:
                str += tree.to_html() + " "
        elif self.type == 'TEXT':
            str = self.value
        else:
            pass
        return str

    def addSubTree(self, tree):
        self.trees.append(tree)
        return self
