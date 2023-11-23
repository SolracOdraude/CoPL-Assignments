import sys

'''
Notes on the grammar: (not entirely relevant in lexical analysis)

Grammar: 
<expr> ::= <var> | '(' <expr> ')' | '\ ' <var> <expr> | <expr> <expr>

obs: also accepting | 'λ' <var> '.' <expr> | would be optimal.

In LL Grammar (from lectures)
<expr>  ::= <lexpr><expr'>
<expr'> ::= <lexpr><expr'> | ε
<lexpr> ::= <pexpr> | 'λ' <var> <lexpr>
<pexpr> ::= <var> | '(' <expr> ')'

Here in the lexical analysis we only need to know which characters we need to tokenize.
Their types are:
    variables (arbitrary name)
    lambda (\ or λ)
    dot '.'
    left parenthesis '('
    right parenthesis ')'
'''


def lexer():    # Also known as tokenizer. 
    """ Returns a list of list of tokens, one for each line inputed. 
    Takes no inputs because it reads direcly from sys.stdin """
    
    output = []

    for line in sys.stdin.readlines():
        line = line.rstrip()    # This removes any trailling whitespaces, including '\n' and similar.
        tokens = []    
        ''' I will represent tokens as tuples (type, name).
        The slot 'name' is only really applicable for variables, as such I will just include 
        my prefered representation of the other types in the place of 'name'.
        '''       
 
        temp_var_name = ''  # This will collect the variable char by char.
        for char in line:
            # Handling variables names:
            if char.isalpha():
                temp_var_name += char
                continue

            elif char.isnumeric():
                if not temp_var_name:
                    raise SyntaxError("Variables may not start with numeric values")
                temp_var_name += char
                continue

            elif temp_var_name:
                tokens.append( ('variable', temp_var_name) )
                temp_var_name = ''

            # Handling other cases:
            if char in ['λ', '\\']: tokens.append( ('lambda', 'λ') )

            elif char == '.': tokens.append( ('dot', '.') )

            elif char == '(': tokens.append( ('left_parenthesis', '(') )

            elif char == ')': tokens.append( ('right_parenthesis', ')'))

            elif char.isspace(): continue 

            else: raise SyntaxError("Inputed character not recognized: " + char)

        # Handling case where last char is part of a variable name:
        if temp_var_name:
            tokens.append( ('variable', temp_var_name) )

        output.append(tokens)

    return output 
        


if __name__ == '__main__':
    for token_list in lexer():
        print(token_list)
    
