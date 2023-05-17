import js2py
import re
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


    def to_html_attribute_list(self):
        classes = []
        attributes = {}

        for subtree in self.trees:
            if subtree.type == 'CLASS':
                classes.append(subtree.value)
            else:
                attributes_names = re.findall(r'\w+\s*=(?!=)', subtree.value)
                attributes_values = re.split(r'\w+\s*=(?!=)', subtree.value)[1:]
                
                for i in range(len(attributes_names)):
                    attributes_names[i] = attributes_names[i].strip()
                    attributes_names[i] = attributes_names[i][:-1]
                    context.execute('atr=' + attributes_values[i])
                    attributes_values[i] = context.eval('atr')

                    if attributes_names[i] == 'class':
                        classes.append(attributes_values[i])
                    elif attributes_names[i] not in attributes:
                        attributes[attributes_names[i]] = attributes_values[i] 
                    else:
                        raise ValueError(f'Duplicated attribute "{attributes_names[i]}" in not allowed')

        return classes, attributes


    def to_html_attributes(self):
        
        
        if self.type == 'attributes1':
            classes1, attributes1 = self.trees[0].to_html_attribute_list()
            id = self.trees[1].value
            classes2, attributes2 = self.trees[2].to_html_attribute_list()
            classes = classes + classes1 + classes2
            attributes = attributes1.copy()
            attributes1.update(attributes2)

            for chave, valor in attributes1.items():
                if valor != attributes1.get(chave):
                    # erro
                    pass
                
            return classes, id, attributes1
        elif self.type == 'attributes2':
            id = self.trees[0].value
            classes, attributes = self.trees[1].to_html_attribute_list()
            
            return classes, id, attributes
        elif self.type == 'attributes3':
            id = self.trees[1].value
            classes, attributes = self.trees[0].to_html_attribute_list()
            
            return classes, id, attributes
        elif self.type == 'attributes4':
            id = self.trees[0].value
            return [], id, {}
        elif self.type == 'attributes5':
            classes, attributes = self.trees[0].to_html_attribute_list()
            return classes, None, attributes 


    def to_html(self, indentation="\n", condition=""):
        string = ""

        if self.type == 'lines': 
            # lines : line line line ...
            for line in self.trees:
                string += line.to_html(indentation)
        
        elif self.type == 'line1': 
            string += self.trees[0].to_html(indentation) 

        elif self.type == 'line2':
            context.execute(self.trees[0].value)
        
        elif self.type == 'conditional1':
            # conditional : conditional_begin conditional_middle conditional_final
            begin = self.trees[0]
            try:
                result = context.eval(begin.trees[0].value)
            except:
                result = False
            if begin.type == 'conditional_begin1' and result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin2' and result:
                pass
            elif begin.type == 'conditional_begin3' and not result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin4' and not result:
                pass
            else: 
                middle = self.trees[1]

                for tree in middle.trees:
                    try:
                        result = context.eval(tree.value)
                    except: 
                        pass
                    if result:
                        if len(tree.trees) > 0:
                            string += tree.trees[1].to_html(indentation)
                        break

                if not result:
                    if len(self.trees[2].trees) > 0:
                        string += self.trees[2].trees[1].to_html(indentation)

        elif self.type == 'conditional2':
            # conditional : conditional_begin conditional_final
            #             | conditional_begin conditional_middle 
            begin = self.trees[0]
            try:
                result = context.eval(begin.trees[0].value)
            except:
                result = False
            if begin.type == 'conditional_begin1' and result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin2' and result:
                pass
            elif begin.type == 'conditional_begin3' and not result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin4' and not result:
                pass
            else: 
                if self.trees[1].type == 'conditional_middle':
                    middle = self.trees[1]

                    for tree in middle.trees:
                        result = context.eval(tree.value)
                        if result:
                            if len(tree.trees) > 0:
                                string += tree.trees[1].to_html(indentation)
                            break
                else:
                    if len(self.trees[1].trees) > 0:
                        string += self.trees[1].trees[1].to_html(indentation)
            
        elif self.type == 'conditional3':
            # begin
            begin = self.trees[0]
            try:
                result = context.eval(begin.trees[0].value)
            except:
                result = False
            if begin.type == 'conditional_begin1' and result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin2' and result:
                pass
            elif begin.type == 'conditional_begin3' and not result:
                string += begin.trees[2].to_html(indentation)
            elif begin.type == 'conditional_begin4' and not result:
                pass
            
        elif self.type == 'iteration1':
            # iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
            context.execute('iteration1 = ' + self.trees[1].value)
            iterator = context.eval('iteration1')
            for val in iterator:
                if type(val) == str:
                    val = '"' + val + '"'
                context.execute(self.trees[0].value + '=' + str(val)) 
                string += self.trees[3].to_html(indentation)

        elif self.type == 'iteration2':
            # iteration : EACH IDENTIFIER COMMA IDENTIFIER IN JSCODE INDENT lines DEDENT
            context.execute('iteration2 = ' + self.trees[2].value)
            iterator = context.eval('iteration2')
            for val in iterator:
                if type(val) == str:
                    val = '"' + val + '"'
                context.execute(self.trees[0].value + ' = ' + val)
                context.execute(self.trees[1].value + ' = ' + 'iteration2[' + str(val) + ']')
                string += self.trees[4].to_html(indentation)

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
            tag = self.trees[0].to_html(indentation)
            aux = tag.split(" ")
            tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1] 
            string += indentation + tag + self.trees[1].to_html() + \
                            self.trees[3].to_html(indentation = self.trees[2].value)
            string += indentation + '</' + tag_name + '>'
        
        elif self.type == 'tagline2':
            # tagline : tag INDENT lines DEDENT 
            tag = self.trees[0].to_html(indentation)
            aux = tag.split()
            tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1] 
            string += indentation + tag + \
                            self.trees[2].to_html(indentation = self.trees[1].value)
            string += indentation + '</' + tag_name + '>'                  
        
        elif self.type == 'tagline3':
            # tagline : tag content
            tag = self.trees[0].to_html(indentation)
            aux = tag.split()
            tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1] 
            string += indentation + tag + self.trees[1].to_html(indentation) + '</' + tag_name + '>' 
        
        elif self.type == 'tagline4': 
            # tagline : tag BAR
            string += indentation + self.trees[0].to_html(indentation)[:-1] + '/>'
       
        elif self.type == 'tagline5':
            # tagline : tag DOT text
            tag = self.trees[0].to_html(indentation)
            aux = tag.split()
            tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1] 
            string += indentation + tag + self.trees[1].to_html(indentation+" ") + indentation + '</' + tag_name + '>' 

        elif self.type == 'tagline6': 
            # tagline : tag
            tag = self.trees[0].to_html(indentation)
            aux = tag.split()
            tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1] 
            string += indentation + tag + '</' + tag_name + '>' 
        
        elif self.type == 'tag1': 
            # tag : TAG attributes
            classes, id, attributes = self.trees[1].to_html_attributes()
            atts = ' '.join([f'{chave}="{valor}"' for chave, valor in attributes.items()])
    
            if atts != '':
                atts = ' ' + atts
            
            cls = " ".join(classes)

            if id == None and cls == '': 
                string += f'<{self.trees[0].value}{atts}>'
            elif id == None:
                string += f'<{self.trees[0].value} class="{" ".join(classes)}"{atts}>'
            elif cls == '':
                string += f'<{self.trees[0].value}{atts} id="{id}">'
            else:
                string += f'<{self.trees[0].value} class="{" ".join(classes)}"{atts} id="{id}">'
            
        elif self.type == 'tag2': 
            # tag : TAG
            string += f'<{self.trees[0].value}>'
            
        elif self.type == 'tag3': 
            # tag : CLASS attributes
            classes, id, attributes = self.trees[1].to_html_attributes()
            classes.append(self.trees[0].value)
            atts = ' '.join([f'{chave}="{valor}"' for chave, valor in attributes.items()])
            if atts != '':
                atts = ' ' + atts
            
            if id == None: 
                string += f'<div class="{" ".join(classes)}"{atts}>'
            else:
                string += f'<div class="{" ".join(classes)}"{atts} id="{id}">'
            
            
        elif self.type == 'tag4': 
            # tag : CLASS
            string += f'<div class="{self.trees[0].value}">'

        elif self.type == 'tag5': 
            # tag : ID attribute_list
            classes, attributes = self.trees[1].to_html_attribute_list()
            id = self.trees[0].value
            atts = ' '.join([f'{chave}="{valor}"' for chave, valor in attributes.items()])
            if atts != '':
                atts = ' ' + atts + ' '
            string += f'<div class="{" ".join(classes)}"{atts}id="{id}">'

        elif self.type == 'tag6': 
            # tag : ID 
             string += f'<div id="{self.trees[0].value}">'
        
        elif self.type == 'content1': 
            # content : EQUALS interpolation
            string += self.trees[1].to_html(indentation)
        
        elif self.type == 'content2': 
            # content : text
            aux = self.trees[0].to_html("")
            if not self.trees[0].trees[0].type.startswith('interpolation'):
                aux = aux[1:]
            string += aux
        
        elif self.type == 'interpolation1':
            # interpolation : STRING
            string += self.trees[0].value
        
        elif self.type == 'interpolation2':
            # interpolation : IDENTIFIER
            try:
                result = str(context.eval(self.trees[0].value))
            except:
                result = ''
            string += result
        
        elif self.type == 'interpolation3':
            # # interpolation : NUMBER
            string += str(self.trees[0].value)
        
        elif self.type == 'text':
            for subtree in self.trees:
                string += indentation + subtree.to_html(indentation)
        
        elif self.type == 'TEXT':
            string += self.value

        elif self.type == 'switch':
            # switch : CASE CONDITION INDENT casesdefault DEDENT
            cond = self.trees[0].value
            string += self.trees[2].to_html(indentation, cond)

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
