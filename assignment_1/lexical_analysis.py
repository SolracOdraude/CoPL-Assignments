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
    variable (arbitrary name)
    lambda (\ or λ)
    period '.'
    left parenthesis '('
    right parenthesis ')'
'''


class Token:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return str((self.type, self.name))


class TokenList:
    def __init__(self, token_list):
        self._tokens = token_list[::-1]
        # Obs: _tokens is saved in reverse to that .consume() uses a fast operation.

    def __repr__(self):
        return str(self._tokens[::-1])
 
    def peek(self):
        ''' Return the current token we are looking at. '''
        return self._tokens[-1] if self._tokens else None

    def consume(self, token_type):
        ''' Deletes the current token we are peeking at. '''
        if not self._tokens:
            raise SyntaxError("No token to consume.")

        consumed = self._tokens.pop() 
        if consumed.type != token_type:
            raise SyntaxError("Consumed token does not match expected type.")

        return consumed
        
'''
These two classes above are just abstractions to help write easily readable code.

'Token' could be easily represented by a python tuple (type, name), but this would require
accesing their type via token[0], instead of the more elegant token.type.

Similarly for TokenList, it couldve been implemented as a python list containing tokens,
however using this abstraction allows for the construction of .peek() and .consume(). 
'''
        

def lexer(): 
    ''' Returns a list of TokenList(s), one for each line in the standard input. ''' 
    
    output = []

    for line in sys.stdin.readlines():
        tokens = []    
 
        temp_var_name = ''  # This will collect the variable name as we accumulate characters.
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
                tokens.append(Token('variable', temp_var_name))
                temp_var_name = ''

            # Handling other cases:
            if char in ['λ', '\\']: tokens.append(Token('lambda', 'λ'))

            elif char == '.': tokens.append(Token('period', '.'))

            elif char == '(': tokens.append(Token('left_parenthesis', '('))

            elif char == ')': tokens.append(Token('right_parenthesis', ')'))

            elif char.isspace(): continue 

            else: raise SyntaxError("Inputed character not recognized: " + char)

        # Handling case where last char is part of a variable name:
        if temp_var_name:
            tokens.append(Token('variable', temp_var_name))

        output.append(TokenList(tokens))

    return output
        

if __name__ == '__main__':
   for tokenized_line in lexer():
        print(tokenized_line) 
