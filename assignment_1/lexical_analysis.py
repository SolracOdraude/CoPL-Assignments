'''
Some notes on the grammar:

Grammar: 
<expr> ::= <var> | '(' <expr> ')' | '\ ' <var> <expr> | <expr> <expr>

(obs: we will also recognize '.' from input) 

Here in the lexical analysis we only need to know which characters we need to tokenize.
Their types are:
    variable (arbitrary name)
    lambda (\ or λ)
    period '.'
    left parenthesis '('
    right parenthesis ')'
    (white spaces will not be needed)
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
        # Obs: _tokens is saved in reverse to that .consume() uses a faster operation.

    def __repr__(self):
        return str(self._tokens[::-1])
 
    def peek(self):
        ''' Return the current token we are looking at. '''
        return self._tokens[-1] if self._tokens else None

    def consume(self, token_type):
        ''' Deletes the current token we are peeking at. '''
        if not self._tokens:
            raise SyntaxError(f"Expected more tokens.")

        consumed = self._tokens.pop() 
        if consumed.type != token_type:
            raise SyntaxError(f"Expected '{token_type}' found '{consumed.type}'.")

        return consumed
        
'''
These two classes above are just abstractions to help write easily readable code.

'Token' could be easily represented by a python tuple (type, name), but this would require
accesing their type via token[0], instead of the more elegant token.type use.

Similarly for TokenList, it couldve been implemented as a python list containing tokens,
however using this abstraction allows for the construction of .peek() and .consume(). 
'''
        

def tokenize(line): 
    ''' Returns all the tokens in the inputed line '''   
 
    tokens = []    

    temp_var_name = ''  # This will collect the variable name as we accumulate characters.
    for char in line:
        # Handling variables names:
        if char.isalpha() and char != 'λ':
            temp_var_name += char
            continue

        elif char.isnumeric():
            if not temp_var_name:
                raise SyntaxError("Variables may not start with numeric values.")
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

        else: raise SyntaxError(f"Inputed character {char} is not recognized.")

    # Handling case where last char is part of a variable name:
    if temp_var_name:
        tokens.append(Token('variable', temp_var_name))

    return TokenList(tokens)


if __name__ == '__main__':
    
    import sys 
    
    for line in sys.stdin.readlines():
        tokens = tokenize(line)
        print(tokens)

