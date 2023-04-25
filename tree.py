import js2py
context = js2py.EvalJs({})

class Tree:
    def __init__(self, type, value, trees):
        self.type = type
        self.value = value
        self.trees = trees


    def print_tree(self):
        print(self.type + '  ' +  self.value + '(', end='')
        for tree in self.trees:
            tree.print_tree()
        print(')',end='')

    def to_html(self, indentation="\n"):
        string = ""
        tag = ""
        classes = ""
        previuos_identation = indentation
        if self.type == 'tags':
            i = 0
            number_trees = len(self.trees)
            while i < number_trees:
                if self.trees[i].type == 'TAG':
                    tag = self.trees[i].value
                    string += indentation + "<" + self.trees[i].value
                    if len(self.trees) == i+1 or self.trees[i+1].type == 'TAG':
                        string += ">" + "</" + tag + ">"
                elif self.trees[i].type == 'INDENT':
                    if classes != "":
                        classes = classes[:-1]
                        string += ' class="' + classes + '"'
                        classes = ""
                    string += '>'
                    indentation = self.trees[i].value
                elif self.trees[i].type == 'DEDENT':
                    string += previuos_identation + '</' + tag + '>'
                    indentation = previuos_identation
                elif self.trees[i].type == 'CLASS':
                    classes += self.trees[i].value + " "
                    #string += " class=" + f'"{self.trees[i].value}"' 
                elif self.trees[i].type == 'ID':
                    string += " id=" + f'"{self.trees[i].value}"'
                elif self.trees[i].type == 'JSOCDE':
                    pass
                elif self.trees[i].type == 'IDENTIFIER':
                    if self.trees[i-1].type != 'EQUALS':
                        string += self.trees[i].value
                    else:    
                        string += self.trees[i].value + '</' + tag + '>'
                elif self.trees[i].type == 'ATTRIBUTENAME':
                    string += f" {self.trees[i].value}"
                elif self.trees[i].type == 'EQUALS':
                    if self.trees[i-1].type != 'ATTRIBUTENAME': # Interpolation =
                        if classes != "":
                            classes = classes[:-1]
                            string += ' class="' + classes + '"'
                            classes = ""
                        string += '>'
                    else: # atributos
                        string += '='
                elif self.trees[i].type == 'BOOLEAN':
                    string += self.trees[i].value
                elif self.trees[i].type == 'STRING':
                    string += self.trees[i].value
                elif self.trees[i].type == 'BAR':
                    string += '/>'
                elif self.trees[i].type == 'BEGININTERP':
                    if self.trees[i-1].type != 'TEXT':
                        string += '>'
                elif self.trees[i].type == 'ENDINTERP':
                    if len(self.trees) == i + 1 or self.trees[i+1].type != 'TEXT':
                        string += '</' + tag + '>' 
                elif self.trees[i].type == 'TEXT':
                    if self.trees[i-1].type != 'ENDINTERP':
                        if classes != "":
                            classes = classes[:-1]
                            string += ' class="' + classes + '"'
                            classes = ""
                        string += '>' + self.trees[i].value[1:]
                        if (len(self.trees)-1 == i) or ((self.trees[i+1].type != 'BEGININTERP') and (self.trees[i+1].type != 'INDENT')):
                            string += '</' + tag + '>'
                    elif len(self.trees) > i+1 and self.trees[i+1].type == 'BEGININTERP':
                        string += self.trees[i].value
                    elif self.trees[i-1].type == 'ENDINTERP':
                        string += self.trees[i].value + '</' + tag + '>'
                    
                elif self.trees[i].type == 'COMMENT':
                    pass
                elif self.trees[i].type == 'NUMBER':
                    if self.trees[i-2].type != 'ATTRIBUTENAME': # Interpolation =
                        string += self.trees[i].value + '</' + tag + '>'
                    else: # Attribute
                        string += '"' + self.trees[i].value + '"'

                elif self.trees[i].type == 'tags':
                    string +=self.trees[i].to_html(indentation)
                i += 1 


        # tag : TAG attributes content INDENT tags DEDENT         
        #     string = ' ' * indentation + '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() +'\n' +\
        #             self.trees[4].to_html(indentation+2) + '\n' + \
        #           ' ' * indentation + '</' + self.trees[0].to_html() + '>'
        # # tag : TAG attributes content 
        # elif self.type == 'tag2':
        #     string = ' ' * indentation + '<' + self.trees[0].to_html() + self.trees[1].to_html() + '>' + self.trees[2].to_html() + '</' + self.trees[0].to_html() + '>'
        # # tag: TAG attributes BAR
        # elif self.type == 'tag3':
        #     string = ' ' * indentation + '<' + self.trees[0].to_html() + '/>'
        # elif self.type == 'TAG':
        #     return self.value
        # elif self.type == 'attributes':
        #     for tree in self.trees:
        #         string += tree.to_html()
        # # pug_attributes : pug_attributes sep pug_attribute
        # #                | pug_attribute
        # elif self.type == 'pug_attributes':
        #     for tree in self.trees:
        #         string += tree.to_html() 
        # elif self.type == 'pug_sep_attribute':
        #     string = self.trees[0].to_html() + self.trees[1].to_html()
        # elif self.type == 'sep':
        #     string = ""
        # elif self.type == 'COMMA':
        #     string = ", "
        # elif self.type == 'pug_attribute':
        #     string = " " + self.trees[0].to_html() + self.trees[1].to_html() + self.trees[2].to_html()
        # elif self.type == 'ATTRIBUTENAME':
        #     string = self.value
        # elif self.type == 'EQUALS':
        #     string = self.value
        # elif self.type == 'stringING' or self.type == 'BOOLEAN' or self.type == 'NUMBER':
        #     string = self.value
        # # class : class CLASS 
        # #       | 
        # elif self.type == 'class':
        #     if len(self.trees) > 0:
        #         string += ' class="'
        #         for tree in self.trees:
        #             string += tree.to_html() + ' '
        #         string += '"'
        # elif self.type == 'CLASS':
        #     string += self.value
        # # id : 
        
        # elif self.type == 'id':
        #     pass
        # elif self.type == 'ID':
        #     string += " " + 'id="' + self.value + '"'
        # elif self.type == 'content1':
        #     string += self.trees[1].to_html()
        # # content : text
        # elif self.type == 'content2':
        #     string = self.trees[0].to_html()
        # # interpolation : stringING
        # elif self.type == 'interpolation1':
        #     string = self.value[1:-1]
        # # interpolation : VARIABLE
        # elif self.type == 'interpolation2':
        #     string = str(context.eval(self.value))
        # elif self.type == 'text1':
        #     pass
        # elif self.type == 'text2':
        #     pass
        # elif self.type == 'text':
        #     for tree in self.trees:
        #         string += tree.to_html() + " "
        # elif self.type == 'TEXT':
        #     string = self.value
        # else:
        #     pass
        return string

    def addSubTree(self, tree):
        self.trees += tree
        return self
