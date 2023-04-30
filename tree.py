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

    def to_html(self, indentation="\n", condition=""):
        global currentTag
        global classes
        string = ""

        if self.type == 'lines': 
            # lines : line line line ...
            for line in self.trees:
                string += line.to_html(indentation) # TODO INDENTATION
        
        elif self.type == 'line1': 
            # line : tagline
            string += self.trees[0].to_html(indentation) 

        elif self.type == 'line2':
            pass
        
        elif self.type == 'line3': 
            # line : comment
            string += self.trees[0].to_html(indentation)
        
        elif self.type == 'line4':
            # line : conditional
            string += self.trees[0].to_html(indentation)
        
        elif self.type == 'line6':
                    # line : conditional
                    string += self.trees[0].to_html(indentation)

        elif self.type == 'conditional':
            # conditional : <lines>
            if len(self.trees) == 1:
                string += self.trees[0].to_html(indentation)

        elif self.type == 'iteration':
            # iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
            for subtree in self.trees:
                string += subtree.to_html(indentation)

        elif self.type == 'comment1':
            # comment : COMMENT comment_text
            fst_line = self.trees[0].value[2:]
            lines = [tree.value.replace('\t', '    ') for tree in self.trees[1].trees]

            min_spaces = min(len(line) - len(line.lstrip()) for line in lines) if lines else 0
            stripped_lines = [line[min_spaces:] for line in lines]
            indented_lines = [line + '\n' for line in stripped_lines[:-1]] + [stripped_lines[-1]]
            string += f"{indentation}<!--{fst_line}{''.join(indented_lines)}-->"
        
        elif self.type == 'comment2':
            # comment : COMMENT
            string += f"{indentation}<!--{self.trees[0].value[2:]}-->"

        elif self.type == 'tagline1': 
            # tagline : tag content INDENT lines DEDENT 
            string += indentation + '<' + self.trees[0].to_html(indentation) + '>' + self.trees[1].to_html(indentation) + '\n' + \
                            self.trees[3].to_html(indentation = self.trees[2].value)
            self.trees[0].to_html(indentation) # to update the currentTag
            string += indentation + '</' + currentTag + '>'
        
        elif self.type == 'tagline2':
            # tagline : tag INDENT lines DEDENT 
            string += indentation + '<' + self.trees[0].to_html(indentation) + '>' + \
                            self.trees[2].to_html(indentation = self.trees[1].value)
            self.trees[0].to_html(indentation) # to update the currentTag
            string += indentation + '</' + currentTag + '>'
                            
        
        elif self.type == 'tagline3':
            # tagline : tag content
            string += indentation + '<' + self.trees[0].to_html(indentation) + '>' + self.trees[1].to_html(indentation) + '</' + currentTag + '>' 
        
        elif self.type == 'tagline4': 
            # tagline : tag BAR
            string += indentation + '<' + self.trees[0].to_html(indentation) + '/>'
       
        elif self.type == 'tagline5':
            # tagline : tag <DOT> text (DOT is not in the tree)
            string += indentation + '<' + self.trees[0].to_html(indentation) + '>' + self.trees[1].to_html(indentation+" ") + '</' + currentTag + '>' 

        elif self.type == 'tagline6': 
            # tagline : tag
            string += indentation + '<' + self.trees[0].to_html(indentation) + '>' + '</' + currentTag + '>' 
        
        elif self.type == 'tag1': 
            # tag : class_id_attributes LPAREN pug_attributes RPAREN 
            string += 'div' + self.trees[0].to_html(indentation) + self.trees[2].to_html(indentation)
            currentTag = "div"
        
        elif self.type == 'tag2': 
            # tag : TAG attributes
            string += self.trees[0].value + self.trees[1].to_html(indentation)
            currentTag = self.trees[0].value
        
        elif self.type == 'tag3': 
            # tag : class_id_attributes
            string += 'div' + self.trees[0].to_html(indentation)
            currentTag = "div"
        
        elif self.type == 'tag4': 
            # tag : TAG
            string += self.trees[0].value
            currentTag = self.trees[0].value
        
        elif self.type == 'attributes1':
            # attributes : class_id_attributes LPAREN pug_attributes RPAREN 
            string += self.trees[0].to_html(indentation) + self.trees[2].to_html(indentation)
        
        elif self.type == 'attributes2': 
            # attributes : LPAREN pug_attributes RPAREN
            string += self.trees[1].to_html(indentation)
        
        elif self.type == 'attributes3':
            # attributes : class_id_attributes
            string += self.trees[0].to_html(indentation)
        
        elif self.type == 'class_id_attributes1': 
            # class_id_attributes : class ID CLASS
            self.trees[0].to_html(indentation)
            classes += " " + self.trees[2].value
            string += f' class="{classes}" id="{self.trees[1].value}"'
        
        elif self.type == 'class_id_attributes2': 
            # class_id_attributes : class ID 
            self.trees[0].to_html(indentation) 
            string += f' class="{classes}" id="{self.trees[1].value}"'
        
        elif self.type == 'class_id_attributes3': 
            # class_id_attributes : ID class
            self.trees[1].to_html(indentation)
            string += f'class="{classes}" id="{self.trees[0].value}"'
        
        elif self.type == 'class_id_attributes4': 
            # class_id_attributes : ID
            string += f'id="{self.trees[0].value}"'
        
        elif self.type == 'class_id_attributes5': 
            # class_id_attributes : class
            self.trees[0].to_html(indentation)
            string += f'class="{classes}"'
        
        elif self.type == 'class': 
            # class : CLASS CLASS ...
            for subtree in self.trees:
                classes += " " + subtree.value
        
        elif self.type == 'pug_attributes': 
            # pug_attributes : pug_attribute pug_attribute ...
            for subtree in self.trees:
                string += " " + subtree.to_html(indentation)
        
        elif self.type == 'pug_attribute1': 
            # pug_attribute : ATTRIBUTENAME EQUALS attribute_value
            string += self.trees[0].value + self.trees[1].value + self.trees[2].to_html(indentation)
        
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
            string += self.trees[1].to_html(indentation)
        
        elif self.type == 'content2': 
            # content : text
            string += self.trees[0].to_html("")
        
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
                string += indentation + subtree.value
        
        elif self.type == 'switch':
            # switch : CASE CONDITION INDENT casesdefault DEDENT
            cond = self.trees[0].value
            string += self.trees[2].to_html(self.trees[1].value, cond)

        elif self.type == 'casesdefault1':
            default = self.trees[1]
            
            result = False

            for tree in self.trees[0].trees:
                result = context.eval(condition + ' == ' + tree.trees[0].value)
                if result:
                    string += tree.trees[1].to_html(indentation)
                    break
            
            if not result:
                string += default.to_html(indentation)

        elif self.type == 'casesdefault2':
            for tree in self.trees[0].trees:
                result = context.execute(condition + ' == ' + tree.trees[0].value)
                if result:
                    string += tree.trees[1].to_html(indentation)
                    break

        elif self.type == 'casesdefault3':
            string += self.trees[0].to_html(indentation)


    

        return string

    def addSubTree(self, tree):
        self.trees.append(tree)
        return self
