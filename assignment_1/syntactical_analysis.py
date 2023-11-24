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

def parse(TokenList):

    consume = TokenList.consume 
    # Consume stays the same as before, we only pass the extra prefix reference.

    def peek():
        found = TokenList.peek()
        return found if found else Token('None', None)
                # Here we abstract the end of TokenList as a new Token of type 'None'. 

    FIRST = {
        'lexpr': ['variable', 'left_parenthesis', 'lambda'],        
        # Obs: we don't need to fill the rest, but for larger grammar this could be useful.  
        } 

    def expr(): 
        lexpr()
        expr_()

    def expr_():
        if peek().type not in FIRST['lexpr']:
            return
        lexpr()
        expr_()

    def lexpr():
        if peek().type == 'lambda':
            consume('lambda')
            consume('variable')
            lexpr_()
            return
        pexpr()

    def lexpr_():
        if peek().type == 'period':
            consume('period')
        lexpr()    
    
    def pexpr():
        if peek().type == 'variable':
            consume('variable')
            return
        consume('left_parenthesis')
        expr()
        consume('right_parenthesis')


    # Scope variables are set, now we parse:
    expr()


if __name__ == '__main__':
    from lexical_analysis import lexer

    for tokenized_line in lexer():
        parse(tokenized_line)

