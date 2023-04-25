import js2py
context = js2py.EvalJs({})

class Tree:
    def __init__(self, type, value, trees):
        self.type = type
        self.value = value
        self.trees = trees


    def print_tree(self):
        print(self.type + '  ' +  self.value + '(')
        for tree in self.trees:
            tree.print_tree()
        print(')')

    def to_html(self, indentation=0):
        string = ""
        if self.type == 'tags':
            for tree in self.trees:
                string += tree.to_html() + "\n"
        elif self.type == 'tag_code1':
            string += self.trees[0].to_html()
        elif self.type == 'tag_code2':
            pass
        # tag : TAG attributes content INDENT tags DEDENT 
        elif self.type == 'tag1':
            string = ' ' * indentation + '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() +'\n' +\
                    self.trees[4].to_html(indentation+2) + '\n' + \
                  ' ' * indentation + '</' + self.trees[0].to_html() + '>'
        # tag : TAG attributes content 
        elif self.type == 'tag2':
            string = ' ' * indentation + '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() + '</' + self.trees[0].to_html() + '>'
        # tag: TAG attributes BAR
        elif self.type == 'tag3':
            string = ' ' * indentation + '<' + self.trees[0].to_html() + '/>'
        elif self.type == 'TAG':
            return self.value
        elif self.type == 'attributes':
            for tree in self.trees:
                string += tree.to_html()
        # pug_attributes : pug_attributes sep pug_attribute
        #                | pug_attribute
        elif self.type == 'pug_attributes':
            for tree in self.trees:
                string += tree.to_html() 
        elif self.type == 'pug_sep_attribute':
            string = self.trees[0].to_html() + self.trees[1].to_html()
        elif self.type == 'sep':
            string = ""
        elif self.type == 'COMMA':
            string = ", "
        elif self.type == 'pug_attribute':
            string = " " + self.trees[0].to_html() + self.trees[1].to_html() + self.trees[2].to_html()
        elif self.type == 'ATTRIBUTENAME':
            string = self.value
        elif self.type == 'EQUALS':
            string = self.value
        elif self.type == 'stringING' or self.type == 'BOOLEAN' or self.type == 'NUMBER':
            string = self.value
        # class : class CLASS 
        #       | 
        elif self.type == 'class':
            if len(self.trees) > 0:
                string += ' class="'
                for tree in self.trees:
                    string += tree.to_html() + ' '
                string += '"'
        elif self.type == 'CLASS':
            string += self.value
        # id : 
        
        elif self.type == 'id':
            pass
        elif self.type == 'ID':
            string += " " + 'id="' + self.value + '"'
        elif self.type == 'content1':
            string += self.trees[1].to_html()
        # content : text
        elif self.type == 'content2':
            string = self.trees[0].to_html()
        # interpolation : stringING
        elif self.type == 'interpolation1':
            string = self.value[1:-1]
        # interpolation : VARIABLE
        elif self.type == 'interpolation2':
            string = str(context.eval(self.value))
        elif self.type == 'text1':
            pass
        elif self.type == 'text2':
            pass
        elif self.type == 'text':
            for tree in self.trees:
                string += tree.to_html() + " "
        elif self.type == 'TEXT':
            string = self.value
        else:
            pass
        return string

    def addSubTree(self, tree):
        self.trees += tree
        return self
