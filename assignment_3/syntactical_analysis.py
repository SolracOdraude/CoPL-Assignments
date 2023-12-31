from lexical_analysis import Token, TokenList

class VariableLeaf:     # for <lvar>
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class TypeLeaf:         # for <uvar>
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class JudgementNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left}) : ({self.right})'

class LambdaNode:
    def __init__(self, var, var_type, right):
        self.var = var
        self.var_type = var_type
        self.right = right

    def __repr__(self):
        return f'(λ{self.var}^{self.var_type} {self.right})'

class ApplicationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.right})'

class TypeArrowNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} -> {self.right})'


# The classes above will save the structure parsed.

'''
Notes on the grammar: 

Grammar:
<judgement> ::= <expr> : <expr>
     <expr> ::= <lvar> | (<expr>) | λ <lvar> ^ <type> <expr> | <expr> <expr>
     <type> ::= <uvar> | (<type>) | <type> -> <type>

In LL(1) Grammar: 
<judg>  ::= <expr> : <type>
<expr>  ::= <lexpr> <expr'>
<expr'> ::= <lexpr> <expr'> | ε
<lexpr> ::= <pexpr> | λ <lvar> ^ <type> <expr>
<pexpr> ::= <lvar> | (<expr>)
<type>  ::= <uvar> <type'> | (<type>) <type'>
<type'> ::= -> <type> <type'> | ε 
'''

def parse(TokenList):

    consume = TokenList.consume 
    # Consume stays the same as before, we only pass the extra prefix reference.

    def peek():
        found = TokenList.peek()
        return found if found else Token('None', None)
                # Here we abstract the end of TokenList as a new Token of type 'None'. 

    FIRST = {
        'lexpr': ['lvar', 'lparen', 'lambda'],        
        # Obs: we don't need to fill the rest, but for larger grammars this could be useful.  
        } 

    def judg():
        left = expr()
        consume('colon')
        right = taipe()
        return JudgementNode(left, right)

    def expr():
        left = lexpr()
        right = expr_()
        if right is None:
            return left
        return ApplicationNode(left, right)

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
            var = consume('lvar')
            consume('hat')
            var_type = taipe()
            if peek().type == 'period': 
                consume('period')     
            right = expr()
            return LambdaNode(var.name, var_type, right)
        return pexpr()

    def pexpr():
        if peek().type == 'lparen':
            consume('lparen')
            expression = expr()
            consume('rparen')
            return expression
        lvar = consume('lvar')
        return VariableLeaf(lvar.name)

    # Obs: 'type' had to be renamed due to naming conflicts with python.
    def taipe():
        if peek().type == 'lparen':
            consume('lparen')
            left = taipe()
            consume('rparen')
            right = type_()
        else:
            uvar = consume('uvar')
            left = TypeLeaf(uvar.name)
            right = type_()
        if right is None:
            return left
        return TypeArrowNode(left, right)

    def type_():
        if peek().type == 'arrow':
            consume('arrow')
            left = taipe()
            right = type_()
            if right is None:
                return left
            return TypeArrowNode(left, right)
    
    # Scope variables are set, now we parse:
    return judg()


if __name__ == '__main__':

    import sys
    from lexical_analysis import tokenize

    for line in sys.stdin.readlines():
        tokens = tokenize(line)
        lambda_tree = parse(tokens)
        print(lambda_tree)
