'''
Some notes on the grammar:

Grammar: 
<judgement> ::= <expr> : <expr>
     <expr> ::= <lvar> | (<expr>) | λ <lvar> ^ <type> <expr> | <expr> <expr>
     <type> ::= <uvar> | (<type>) | <type> -> <type>

Obs: <lvar> stands for variable name.

Here in the lexical analysis we only need to know which characters we need to tokenize.
Their types are:
    lvar (lowecase variable name)
    uvar (uppercase variable name)
    lambda (\ or λ)
    period '.'
    lparen '('
    rparen ')'
    colon ':'
    hat '^'
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
    shaft = False       # This will be used to detect '->', shaft True means we read '-'.

    for char in line:

        if shaft and char != '>':
            raise SyntaxError(f"Expected '>' to form '->'. Instead found '{char}'.")

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
            if temp_var_name[0].islower(): 
                tokens.append(Token('lvar', temp_var_name))
            else: 
                tokens.append(Token('uvar', temp_var_name))
            temp_var_name = ''

        # Handling other cases:
        match char:
            
            case char if char in ['λ', '\\']: tokens.append(Token('lambda', 'λ'))

            case '.': tokens.append(Token('period', '.'))

            case '(': tokens.append(Token('lparen', '('))

            case ')': tokens.append(Token('rparen', ')'))

            case ':': tokens.append(Token('colon', ':'))

            case '^': tokens.append(Token('hat', '^'))

            case '-': shaft = True; continue
    
            case '>': 
                if shaft: tokens.append(Token('arrow', '->'))
                else: raise SyntaxError(f"Expected '-' before '>'. Instead found '{char}'.") 

            case _: 
                if char.isspace():
                    pass
                else:
                    raise SyntaxError(f"Inputed character {char} is not recognized.")

        shaft = False


    # Handling case where last char is part of a variable name:
    if temp_var_name:
        if temp_var_name[0].islower():
            tokens.append(Token('lvar', temp_var_name))
        else: 
            tokens.append(Token('uvar', temp_var_name))

    return TokenList(tokens)


if __name__ == '__main__':
    
    import sys 
    
    for line in sys.stdin.readlines():
        tokens = tokenize(line)
        print(tokens)

