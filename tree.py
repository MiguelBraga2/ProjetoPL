import random
import js2py
import re
# Exceptions
from DuplicateAttribute import DuplicateAttribute
from SelfClosingElement import SelfClosingElement
from UnexpectedToken import UnexpectedToken

context = js2py.EvalJs({})

def block_text(string):
    count = 0
    for char in string:
        if char == ' ':
            count += 1
        else:
            break
    if count == 1:
        string = string[1:]
    elif count == 0:
        pass
    else:
        string = string.lstrip()
        string = ' ' + string

    return string

# Check if string is a javascript loop
def is_javascript_loop(string):
    pattern = r"^\s*(for|while)\s*\(.+\)\s*$"
    match = re.search(pattern, string)
    return bool(match)

class Tree:
    def __init__(self, type, value='', trees=[]):
        self.type = type
        self.value = value
        self.trees = trees
    
    # Print tree in a basic tree formatting
    def print_tree(self):
        print(self.type + '  ' + self.value + '(', end='')
        for tree in self.trees:
            tree.print_tree()
        print(')', end='')

    def to_html_attribute_list(self):
        classes = []
        attributes = {}

        for subtree in self.trees:
            # If we find a class, append it to the class list
            if subtree.type == 'CLASS':
                classes.append(subtree.value)
            else: # Remove spaces anywhere except between attributes
                at = re.sub(r'\s*(=|\:|\?|\+|-|\*|\/|,|\(|\)|\%|\<|\>|\&|\^|\||\!|\'|\{)', r'\1', subtree.value)
                style = re.findall(r'\w+=\{[^}]+}', at)
                if style:
                    at = re.sub(r'\w+=\{[^}]+}', '', at)

                # Create the attribute list by splitting by spaces
                at = re.split(r',?\s+', at)
                if at[0] == '':
                    at.pop(0)

                at += style

                for attribute in at:
                    attribute = re.split('=', attribute)

                    if len(attribute) == 1:
                        if attribute[0] == 'class':
                            classes.append(attribute[0])
                        elif attribute[0] not in attributes:
                            try:
                                attributes[attribute[0]] = attribute[0]
                            except:
                                attributes[attribute[0]] = ""
                        else: # Check for duplicated attributes
                            raise DuplicateAttribute(f'Duplicated attribute "{attribute[0]}" in not allowed')
                    else:
                        if attribute[0] == 'class':
                            classes.append(context.eval(attribute[1]))
                        elif attribute[0] not in attributes:
                            if attribute[0] == 'style':
                                if attribute[1][0] == '{' and attribute[-1][-1] == '}':
                                    res = attribute[1][1:-1]
                                    res = re.sub(r'\s*,\s*', ';', res)
                                    res = re.sub(r'\'', '', res)
                                    attributes[attribute[0]] = res + ';'
                                else:
                                    try:
                                        attributes[attribute[0]] = context.eval(attribute[1])
                                    except:
                                        attributes[attribute[0]] = ""
                            else:
                                try:
                                    attributes[attribute[0]] = context.eval(attribute[1])
                                except:
                                    attributes[attribute[0]] = ""
                        else:
                            raise DuplicateAttribute(f'Duplicated attribute "{attribute[0]}" in not allowed')

        return classes, attributes

    def to_html_attributes(self):
        match self.type:
            case 'attributes1':
                classes1, attributes1 = self.trees[0].to_html_attribute_list()
                id = self.trees[1].value
                classes2, attributes2 = self.trees[2].to_html_attribute_list()
                classes = classes1 + classes2 # Concatenate all classes from the attributes groups

                for chave, valor in attributes2.items():
                    if chave in attributes1:
                        raise DuplicateAttribute(f'Duplicate attribute "{chave}" is not allowed.')
                    else:
                        attributes1[chave] = valor

                return classes, id, attributes1

            case 'attributes2':
                id = self.trees[0].value
                classes, attributes = self.trees[1].to_html_attribute_list()

                return classes, id, attributes

            case 'attributes3':
                id = self.trees[1].value
                classes, attributes = self.trees[0].to_html_attribute_list()

                return classes, id, attributes
            case 'attributes4':
                id = self.trees[0].value

                return [], id, {}

            case 'attributes5':
                classes, attributes = self.trees[0].to_html_attribute_list()
                return classes, None, attributes

    def get_code(self):
        code = ''
        match self.type:
            case 'code_lines1':
                code += self.trees[0].value
            case 'code_lines2':
                code += self.trees[0].value
                for tree in self.trees[1].trees:
                    code += tree.value

        return code

    # Function to convert to HTML
    def to_html(self, indentation="\n", condition=""):
        global context # Context Javascript with the variables
        string = ""

        match self.type:
            case 'lines':
                for tree in self.trees:
                    string += tree.to_html(indentation)

            case 'line':
                string += self.trees[0].to_html(indentation)

            case 'DOCTYPE':
                res = re.sub('doctype', 'DOCTYPE', self.value.rstrip()) # To UPPER
                if res == 'DOCTYPE':
                    string += indentation + '<!DOCTYPE html>'
                else:
                    res = re.sub(r'\s+', ' ', res) 
                    res = re.split(r'DOCTYPE', res)
                    string += indentation + '<!DOCTYPE ' + res[-1].lstrip() + '>'

            case 'code1':
                code = self.trees[0].get_code()
                try:
                    context.execute(code)
                except Exception as e:
                    raise UnexpectedToken(f'Unexpected token: ' + str(e))

            case 'code2':
                code = self.trees[0].get_code()

                if is_javascript_loop(code):
                    # Generate a random_number to distinguish between contests
                    random_number = random.randint(1, 100000000000000)
                    setattr(context, 'to_html' + str(random_number), self.trees[2].to_html)
                    context.execute(f'''
                                    var result{random_number} = "";
                                    {code}{{
                                        result{random_number} += to_html{random_number}({indentation});
                                    }}
                                    ''')
                    result = context.eval(f'result{random_number}')

                    string += result

                else:
                    try:
                        # Save the JS context
                        context.execute(code)
                        string += self.trees[2].to_html(indentation)

                    except Exception as e:
                        raise UnexpectedToken(f'Unexpected token: ' + str(e))

            case 'conditional1':
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

            case 'conditional2':
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
                            try:
                                result = context.eval(tree.value)
                            except:
                                pass
                            if result:
                                if len(tree.trees) > 0:
                                    string += tree.trees[1].to_html(indentation)
                                break
                    else:
                        if len(self.trees[1].trees) > 0:
                            string += self.trees[1].trees[1].to_html(indentation)

            case 'conditional3':
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

            case 'iteration1':
                # iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
                try:
                    context.execute('iteration1 = ' + self.trees[1].value)
                    iterator = context.eval('iteration1')
                except Exception as e:
                    raise UnexpectedToken(f'Unexpected token: ' + str(e))
                for val in iterator:
                    if type(val) == str:
                        val = '"' + val + '"'

                    context.execute(self.trees[0].value + '=' + str(val))
                    string += self.trees[3].to_html(indentation)

            case 'iteration2':
                # iteration : EACH IDENTIFIER COMMA IDENTIFIER IN JSCODE INDENT lines DEDENT
                try:
                    context.execute('iteration2 = ' + self.trees[2].value)
                    iterator = context.eval('iteration2')
                    aux = context.eval('Array.isArray(iteration2)')
                except Exception as e:
                    raise UnexpectedToken(f'Unexpected token: ' + str(e))

                if aux:
                    i = 0
                    for val in iterator:
                        if type(val) == str:
                            val = '"' + val + '"'
                        context.execute(self.trees[0].value + ' = ' + val)
                        context.execute(self.trees[1].value + ' = ' + str(i))
                        i += 1
                        string += self.trees[4].to_html(indentation)
                else:
                    for key in iterator:
                        if type(key) == str:
                            key = '"' + key + '"'
                        context.execute(self.trees[1].value + ' = ' + key)
                        context.execute(self.trees[0].value + ' = ' + 'iteration2[' + str(key) + ']')
                        string += self.trees[4].to_html(indentation)

            case 'iteration3':
                # iteration : WHILE CONDITION INDENT lines DEDENT
                try:
                    cond = context.eval(self.trees[0].value)
                except Exception as e:
                    raise UnexpectedToken(f'Unexpected token: ' + str(e))
                while cond:
                    string += self.trees[2].to_html(indentation)
                    cond = context.eval(self.trees[0].value)

            case 'comment1':
                # comment : COMMENT comment_text
                fst_line = self.trees[0].value[2:]  # Retira o //
                lines = [tree.value.replace('\t', '    ') for tree in
                         self.trees[1].trees]  # Substitui \t por '    ' nas linhas seguintes
                min_spaces = min(len(line) - len(line.lstrip()) for line in lines) if lines else 0
                stripped_lines = [line[min_spaces:] for line in lines]
                indented_lines = [line + '\n' for line in stripped_lines[:-1]] + [stripped_lines[-1]]
                string += f"{indentation}<!--{fst_line}{''.join(indented_lines)}-->"

            case 'comment2':
                # comment : COMMENT
                string += f"{indentation}<!--{self.trees[0].value[2:]}-->"

            case 'tagline1':
                # tagline : tag content INDENT lines DEDENT 
                tag = self.trees[0].to_html(indentation)
                aux = tag.split(" ")
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                if tag_name == 'html':
                    string += indentation + tag + self.trees[1].to_html() + '\n' + \
                              self.trees[3].to_html(indentation=indentation)
                    string += '\n' + indentation + '</' + tag_name + '>'
                elif tag_name in ['input', 'br', 'img']:
                    raise SelfClosingElement(f'{tag_name} is a self closing element: <{tag_name}/> but contains nested content.')
                else:
                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    string += p + indentation + tag + self.trees[1].to_html() + \
                              self.trees[3].to_html(indentation=indentation + ' ' * 2)
                    string += indentation + '</' + tag_name + '>'

            case 'tagline2':
                # tagline : tag INDENT lines DEDENT 
                tag = self.trees[0].to_html(indentation)
                aux = tag.split()
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                if tag_name == 'html':
                    string += indentation + tag + '\n' + \
                              self.trees[2].to_html(indentation=indentation)
                    string += '\n' + indentation + '</' + tag_name + '>'
                elif tag_name in ['input', 'br','img']:
                    raise SelfClosingElement(f'{tag_name} is a self closing element: <{tag_name}/> but contains nested content.')
                else:
                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    string += p + indentation + tag + self.trees[2].to_html(indentation=indentation + ' ' * 2)
                    string += indentation + '</' + tag_name + '>'

            case 'tagline3':
                # tagline : tag content
                tag = self.trees[0].to_html(indentation)
                aux = tag.split()
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                if tag_name == 'html':
                    string += indentation + tag + self.trees[1].to_html(
                        indentation) + '\n' + indentation + '</' + tag_name + '>'
                elif tag_name in ['input', 'br','img']:
                    raise SelfClosingElement(f'{tag_name} is a self closing element: <{tag_name}/> but contains nested content.')
                else:
                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    string += p + indentation + tag + self.trees[1].to_html(indentation) + '</' + tag_name + '>'

            case 'tagline4':
                # tagline : tag BAR
                tag = self.trees[0].to_html(indentation)
                aux = tag.split()
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                if tag_name == 'html':
                    string += indentation + tag[:-1] + ' />' + '\n'
                else:

                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    string += p + indentation + tag[:-1] + ' />'

            case 'tagline5':
                # tagline : tag DOT NEWLINE block_text
                tag = self.trees[0].to_html(indentation)
                aux = tag.split()
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                lines = []
                line = ""
                for tree in self.trees[1].trees:
                    if tree.type == 'TEXT':
                        line += tree.value
                    elif tree.type[:-1] == 'tagline':
                        line += tree.to_html(indentation='')
                    elif tree.type == 'NEWLINE':
                        lines.append(line)
                        line = ''
                    else:
                        line += tree.to_html(indentation='')

                if line != '':
                    lines.append(line)

                if tag_name == 'script':
                    lines = [line.lstrip() for line in lines]
                    indented_lines = [line + indentation + ' ' * 2 for line in lines]

                    string += indentation + tag + indentation + ' ' * 2 + ''.join(indented_lines)[
                                                                          :-2] + '</' + tag_name + '>'
                elif tag_name in ['input', 'br','img']:
                    raise SelfClosingElement(f'{tag_name} is a self closing element: <{tag_name}/> but contains nested content.')
                else:
                    fst_line = lines.pop(0)
                    fst_line = block_text(fst_line)

                    if len(lines) > 0:
                        last_line = lines.pop(-1).lstrip()
                        if (last_line[-1] == ' ') or (last_line[-1] == '\t'):
                            last_line = last_line.rstrip()
                            last_line = last_line + ' '
                    else:
                        last_line = ''

                    if tag_name == 'html':
                        ht = '\n' + indentation
                    else:
                        ht = ''

                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    lines = [line.lstrip() for line in lines]
                    indented_lines = [line + indentation + ' ' * 2 for line in lines]
                    string += p + indentation + tag + fst_line + indentation + ' ' * 2 + ''.join(
                        indented_lines) + last_line + ht + '</' + tag_name + '>'

            case 'tagline6':
                # tagline : tag
                tag = self.trees[0].to_html(indentation)
                aux = tag.split()
                tag_name = aux[0][1:] if len(aux) > 1 else aux[0][1:-1]

                if tag_name == 'html':
                    string += indentation + tag + '\n' + indentation + '</' + tag_name + '>'
                elif tag_name in ['input', 'br','img']:
                    string += tag[:-1] + ' />'
                else:

                    if tag_name == 'body':
                        p = '\n'
                    else:
                        p = ''

                    string += p + indentation + tag + '</' + tag_name + '>'

            case 'tag1':
                # tag : TAG attributes
                if self.trees[0].value == 'div' and self.trees[1].trees[0].type == 'ATTRIBUTES':
                    raise UnexpectedToken('unexpected token "attributes"')

                classes, id, attributes = self.trees[1].to_html_attributes()
                atts = ' '.join([f'{chave}="{valor}"' for chave, valor in attributes.items()])

                if atts != '':
                    atts = ' ' + atts

                cls = " ".join(classes)

                if id is None and cls == '':
                    string += f'<{self.trees[0].value}{atts}>'
                elif id is None:
                    string += f'<{self.trees[0].value} class="{" ".join(classes)}"{atts}>'
                elif cls == '':
                    string += f'<{self.trees[0].value} id="{id}"{atts}>'
                else:
                    string += f'<{self.trees[0].value} class="{" ".join(classes)}" id="{id}"{atts}>'

            case 'tag2':
                # tag : TAG
                string += f'<{self.trees[0].value}>'

            case 'content1':
                # content : EQUALS JSCODE
                try:
                    string += str(context.eval(self.trees[0].value))
                except:
                    pass

            case 'content2':
                # content : text
                aux = self.trees[0].to_html("")
                if not self.trees[0].trees[0].type.startswith('interpolation') and not self.trees[0].trees[
                    0].type.startswith('tagline'):
                    aux = aux[1:]
                string += aux

            case 'interpolation1':
                # interpolation : JSCODE
                try:
                    string += str(context.eval(self.trees[0].value))
                except:
                    pass

            case 'text':
                for subtree in self.trees:
                    subtree_html = subtree.to_html(indentation)
                    string += indentation + subtree_html

            case 'TEXT':
                string += self.value

            case 'switch':
                # switch : CASE CONDITION INDENT casesdefault DEDENT
                cond = self.trees[0].value
                string += self.trees[2].to_html(indentation, cond)

            case 'casesdefault1':
                default = self.trees[1]

                result = False

                for i in range(len(self.trees[0].trees)):
                    try:
                        result = context.eval(condition + ' == ' + self.trees[0].trees[i].trees[0].value)
                    except Exception as e:
                        raise UnexpectedToken(f'Unexpected token: ' + str(e))

                    if result and len(self.trees[0].trees[i].trees) == 1:
                        i += 1
                        b_aux = False
                        while i < len(self.trees[0].trees):
                            if len(self.trees[0].trees[i].trees) != 1:
                                string += self.trees[0].trees[i].trees[1].to_html(indentation)
                                b_aux = True
                                break
                        if not b_aux:
                            result = False
                        break

                    if result:
                        string += self.trees[0].trees[i].trees[1].to_html(indentation)
                        break

                if not result:
                    string += default.to_html(indentation)

            case 'casesdefault2':
                for i in range(len(self.trees[0].trees)):
                    try:
                        result = context.eval(condition + ' == ' + self.trees[0].trees[i].trees[0].value)
                    except Exception as e:
                        raise UnexpectedToken(f'Unexpected token: ' + str(e))

                    if result and len(self.trees[0].trees[i].trees) == 1:
                        i += 1
                        while i < len(self.trees[0].trees):
                            if len(self.trees[0].trees[i].trees) != 1:
                                string += self.trees[0].trees[i].trees[1].to_html(indentation)
                                break
                        break

                    if result:
                        string += self.trees[0].trees[i].trees[1].to_html(indentation)
                        break

            case 'casesdefault3':
                string += self.trees[0].to_html(indentation)

        return string

    def addSubTree(self, tree):
        self.trees.append(tree)
        return self
