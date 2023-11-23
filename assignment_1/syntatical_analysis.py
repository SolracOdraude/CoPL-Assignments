'''
Notes on the grammar: 

<expr> ::= <var> | ( <expr> ) | λ <var> <expr> | λ <var> . <expr> | <expr> <expr>

In LL Grammar:
<expr>  ::= <lexpr><expr'>
<expr'> ::= <lexpr><expr'> | ε
<lexpr>  ::= <pexpr> | 'λ' <var> <lexpr'>
<lexpr'> ::= '.' <lexpr> | <lexpr>          
<pexpr> ::= <var> | '(' <expr> ')'
'''


