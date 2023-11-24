from lexical_analysis import Token

'''
Notes on the grammar: 

Grammar:
<expr> ::= <var> | ( <expr> ) | λ <var> <expr> | λ <var> . <expr> | <expr> <expr>

In LL Grammar: (accepting optional parenthesis and periods)
<expr> ::= <lexpr> <expr'>
<expr'> ::= <lexpr> <expr'> | ε
<lexpr> ::= <pexpr> | 'λ' <var> <lexpr'>
<lexpr'> ::= '.' <lexpr> | <lexpr>          
<pexpr> ::= <var> | '(' <expr> ')'

FIRST(<expr>) = FIRST(<lexpr>) = FIRST(<pexpr>) ∪ {'λ'} = {<var>, '(', 'λ'}
FIRST(<expr'>) = FIRST(<lexpr>) ∪ {ε} = {<var>, '(', 'λ', ε}
FIRST(<lexpr>) = FIRST(<pexpr>) ∪ {'λ'} = {<var>, '(', 'λ'}
FIRST(<lexpr'>) = {'.'} ∪ FIRST(<lexpr>) = {'.', <var>, '(', 'λ'}
FIRST(<pexpr>) = {<var>, '('} 
'''

class VariableLeaf:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'{self.name}'

class LambdaNode:
    def __init__(self, variable, right):
        self.variable = variable
        self.right = right

    def __repr__(self):
        return f'λ{self.variable}.({self.right})'

class ApplicationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.right})'


# The classes above will save the structure parsed.
# Variables can ever only appear in leafs
# Lamda Nodes connect the lambda variable 'λx.' to an expression (right).
# Applications connect two expressions (left and right).


def parse(TokenList):

    consume = TokenList.consume 
    # Consume stays the same as before, we only pass the extra prefix reference.

    def peek():
        found = TokenList.peek()
        return found if found else Token('None', None)
                # Here we abstract the end of TokenList as a new Token of type 'None'. 

    FIRST = {
        'lexpr': ['variable', 'left_parenthesis', 'lambda'],        
        # Obs: we don't need to fill the rest, but for larger grammars this could be useful.  
        } 

    def expr(): 
        left = lexpr()
        right = expr_()
        if right is not None:
            return ApplicationNode(left, right)
        return left

    def expr_():
        if peek().type not in FIRST['lexpr']:
            return None
        left = lexpr()
        right = expr_()
        if right is not None:
            return ApplicationNode(left, right)
        return left

    def lexpr():
        if peek().type == 'lambda':
            consume('lambda')
            var = consume('variable') 
            right = lexpr_()
            return LambdaNode(var.name, right)
        return pexpr()

    def lexpr_():
        if peek().type == 'period':
            consume('period')
        return lexpr()
    
    def pexpr():
        if peek().type == 'variable':
            var = consume('variable')
            return VariableLeaf(var.name) 
        consume('left_parenthesis')
        expression = expr()
        consume('right_parenthesis')
        return expression

    # Scope variables are set, now we parse:
    return expr()


if __name__ == '__main__':

    import sys
    from lexical_analysis import tokenize

    for line in sys.stdin.readlines():
        tokens = tokenize(line)
        lambda_tree = parse(tokens)
        print(lambda_tree)
