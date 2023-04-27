import js2py
context = js2py.EvalJs({})

currentTag = ""
classes = ""

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

    def to_html(self, indentation=""):
        global currentTag
        global classes
        string = ""

        if self.type == 'lines': 
            # lines : line line line ...
            for line in self.trees:
                string += indentation + line.to_html() + "\n" # TODO INDENTATION
        
        elif self.type == 'line1': 
            # line : tagline
            string += self.trees[0].to_html() 

        elif self.type == 'line2':
            pass
        
        elif self.type == 'line3': 
            # line : comment
            string += self.trees[0].to_html()
        
        elif self.type == 'line4':
            pass # TODO

        elif self.type == 'comment1':
            # comment : COMMENT comment_text
            string += self.trees[0].value + '\n' + self.trees[1].to_html()
        
        elif self.type == 'comment2':
            # comment : COMMENT
            string += self.trees[0].value

        elif self.type == 'comment_text':
            # comment_text : TEXT TEXT ...
            for subtree in self.trees:
                string += "// " + subtree.value + '\n'
        
        elif self.type == 'tagline1': 
            # tagline : tag content INDENT lines DEDENT 
            string += '<' + self.trees[0].to_html() + '>' + self.trees[1].to_html() + '\n' + \
                            self.trees[3].to_html(indentation=indentation+"  ")
            self.trees[0].to_html() # to update the currentTag
            string += indentation + '</' + currentTag + '>'
        
        elif self.type == 'tagline2':
            # tagline : tag INDENT lines DEDENT 
            string += '<' + self.trees[0].to_html() + '>' + '\n' + \
                            self.trees[2].to_html(indentation=indentation+"  ")
            self.trees[0].to_html() # to update the currentTag
            string += indentation + '</' + currentTag + '>'
                            
        
        elif self.type == 'tagline3':
            # tagline : tag content
            string += '<' + self.trees[0].to_html() + '>' + self.trees[1].to_html() + '</' + currentTag + '>' 
        
        elif self.type == 'tagline4': 
            # tagline : tag BAR
            string += '<' + self.trees[0].to_html() + '/>'
       
        elif self.type == 'tagline5':
            pass # TODO

        elif self.type == 'tagline6': 
            # tagline : tag
            string += '<' + self.trees[0].to_html() + '>' + '</' + currentTag + '>' 
        
        elif self.type == 'tag1': 
            # tag : class_id_attributes LPAREN pug_attributes RPAREN 
            string += 'div' + self.trees[0].to_html() + self.trees[2].to_html()
            currentTag = "div"
        
        elif self.type == 'tag2': 
            # tag : TAG attributes
            string += self.trees[0].value + self.trees[1].to_html()
            currentTag = self.trees[0].value
        
        elif self.type == 'tag3': 
            # tag : class_id_attributes
            string += 'div' + self.trees[0].to_html()
            currentTag = "div"
        
        elif self.type == 'tag4': 
            # tag : TAG
            string += self.trees[0].value
            currentTag = self.trees[0].value
        
        elif self.type == 'attributes1':
            # attributes : class_id_attributes LPAREN pug_attributes RPAREN 
            string += self.trees[0].to_html() + self.trees[2].to_html()
        
        elif self.type == 'attributes2': 
            # attributes : LPAREN pug_attributes RPAREN
            string += self.trees[1].to_html()
        
        elif self.type == 'attributes3':
            # attributes : class_id_attributes
            string += self.trees[0].to_html()
        
        elif self.type == 'class_id_attributes1': 
            # class_id_attributes : class ID CLASS
            self.trees[0].to_html()
            classes += " " + self.trees[2].value
            string += f' class="{classes}" id="{self.trees[1].value}"'
        
        elif self.type == 'class_id_attributes2': 
            # class_id_attributes : class ID 
            self.trees[0].to_html() 
            string += f' class="{classes}" id="{self.trees[1].value}"'
        
        elif self.type == 'class_id_attributes3': 
            # class_id_attributes : ID class
            self.trees[1].to_html()
            string += f'class="{classes}" id="{self.trees[0].value}"'
        
        elif self.type == 'class_id_attributes4': 
            # class_id_attributes : ID
            string += f'id="{self.trees[0].value}"'
        
        elif self.type == 'class_id_attributes5': 
            # class_id_attributes : class
            self.trees[0].to_html()
            string += f'class="{classes}"'
        
        elif self.type == 'class': 
            # class : CLASS CLASS ...
            for subtree in self.trees:
                classes += " " + subtree.value
        
        elif self.type == 'pug_attributes': 
            # pug_attributes : pug_attribute pug_attribute ...
            for subtree in self.trees:
                string += " " + subtree.to_html()
        
        elif self.type == 'pug_attribute1': 
            # pug_attribute : ATTRIBUTENAME EQUALS attribute_value
            string += self.trees[0].value + self.trees[1].value + self.trees[2].to_html()
        
        elif self.type == 'attribute_value1': 
            # attribute_value : STRING
            string += self.trees[0].value
        
        elif self.type == 'attribute_value2': 
            # attribute_value : BOOLEAN
            string += self.trees[0].value
        
        elif self.type == 'attribute_value3': 
            # attribute_value : NUMBER
            string += self.trees[0].value
        
        elif self.type == 'content1': 
            # content : EQUALS interpolation
            string += self.trees[1].to_html()
        
        elif self.type == 'content2': 
            # content : text
            string += self.trees[0].to_html()
        
        elif self.type == 'interpolation1':
            # interpolation : STRING
            string += self.trees[0].value
        
        elif self.type == 'interpolation2':
            # interpolation : IDENTIFIER
            string += str(self.trees[0].value)
        
        elif self.type == 'interpolation3':
            # # interpolation : NUMBER
            string += str(self.trees[0].value)
        
        elif self.type == 'text':
            # text : TEXT TEXT ...
            for subtree in self.trees:
                string += subtree.value
        

        #string = ""
        #tag = ""
        #classes = ""
        #previuos_identation = indentation
        #if self.type == 'tags':
        #    i = 0
        #    number_trees = len(self.trees)
        #    while i < number_trees:
        #        if self.trees[i].type == 'TAG':
        #            tag = self.trees[i].value
        #            string += indentation + "<" + self.trees[i].value
        #            if len(self.trees) == i+1 or self.trees[i+1].type == 'TAG':
        #                string += ">" + "</" + tag + ">"
        #        elif self.trees[i].type == 'INDENT':
        #            if classes != "":
        #                classes = classes[:-1]
        #                string += ' class="' + classes + '"'
        #                classes = ""
        #            string += '>'
        #            indentation = self.trees[i].value
        #        elif self.trees[i].type == 'DEDENT':
        #            string += previuos_identation + '</' + tag + '>'
        #            indentation = previuos_identation
        #        elif self.trees[i].type == 'CLASS':
        #            classes += self.trees[i].value + " "
        #            #string += " class=" + f'"{self.trees[i].value}"' 
        #        elif self.trees[i].type == 'ID':
        #            string += " id=" + f'"{self.trees[i].value}"'
        #        elif self.trees[i].type == 'JSOCDE':
        #            pass
        #        elif self.trees[i].type == 'IDENTIFIER':
        #            if self.trees[i-1].type != 'EQUALS':
        #                string += self.trees[i].value
        #            else:    
        #                string += self.trees[i].value + '</' + tag + '>'
        #        elif self.trees[i].type == 'ATTRIBUTENAME':
        #            string += f" {self.trees[i].value}"
        #        elif self.trees[i].type == 'EQUALS':
        #            if self.trees[i-1].type != 'ATTRIBUTENAME': # Interpolation =
        #                if classes != "":
        #                    classes = classes[:-1]
        #                    string += ' class="' + classes + '"'
        #                    classes = ""
        #                string += '>'
        #            else: # atributos
        #                string += '='
        #        elif self.trees[i].type == 'BOOLEAN':
        #            string += self.trees[i].value
        #        elif self.trees[i].type == 'STRING':
        #            string += self.trees[i].value
        #        elif self.trees[i].type == 'BAR':
        #            string += '/>'
        #        elif self.trees[i].type == 'BEGININTERP':
        #            if self.trees[i-1].type != 'TEXT':
        #                string += '>'
        #        elif self.trees[i].type == 'ENDINTERP':
        #            if len(self.trees) == i + 1 or self.trees[i+1].type != 'TEXT':
        #                string += '</' + tag + '>' 
        #        elif self.trees[i].type == 'TEXT':
        #            if self.trees[i-1].type != 'ENDINTERP':
        #                if classes != "":
        #                    classes = classes[:-1]
        #                    string += ' class="' + classes + '"'
        #                    classes = ""
        #                string += '>' + self.trees[i].value[1:]
        #                if (len(self.trees)-1 == i) or ((self.trees[i+1].type != 'BEGININTERP') and (self.trees[i+1].type != 'INDENT')):
        #                    string += '</' + tag + '>'
        #            elif len(self.trees) > i+1 and self.trees[i+1].type == 'BEGININTERP':
        #                string += self.trees[i].value
        #            elif self.trees[i-1].type == 'ENDINTERP':
        #                string += self.trees[i].value + '</' + tag + '>'
        #            
        #        elif self.trees[i].type == 'COMMENT':
        #            pass
        #        elif self.trees[i].type == 'NUMBER':
        #            if self.trees[i-2].type != 'ATTRIBUTENAME': # Interpolation =
        #                string += self.trees[i].value + '</' + tag + '>'
        #            else: # Attribute
        #                string += '"' + self.trees[i].value + '"'
#
        #        elif self.trees[i].type == 'tags':
        #            string +=self.trees[i].to_html(indentation)
        #        i += 1 


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
        self.trees.append(tree)
        return self
