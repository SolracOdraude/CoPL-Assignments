student number: s3647048
assignment status: nearly done. (read 2.)

The code structure was devised as follows:
    We have only two function that will do all the work, they are:
        1. lexer()              found in lexical_analysis.py
        2. parse(TokenList)     found in syntactical_analysis.py

    These function manipulate information encoded in the abstractions (python classes):
        3. Token                found in lexical_analysis.py
        4. TokenList            found in lexical_analysis.py


    3.  The class 'Token' is an abstraction from the pair (type, name) that we desire each token to have.
        Since 'name' is only applicable for variables, other types will save the system's prefered 
        representation of the Token type. 
   
    4.  'TokenList' is an abstraction of a list of Token's that allows us to use the methods: 
            TokenList.peek() and 
            TokenList.consume(token_type)

        As suggested in the video lectures, .peek() returns the current Token that we are trying to parse,
        while .consume(token_type) will delete the current token, raising an error if there was nothing to
        consume or if the consumed Token type was different than the intended (passed as argument).


    1.  The function 'lexer()' is meant to be used only once with no extra arguments.
        It reads directly from standard input (using the sys module) and returns a list of TokenList(s),
        one for each line on the input. 

    2.  The function 'parse()' takes a single TokenList and attemps to parse the Tokens using recursive
        descent. Currently it does not output the sturcture back to the user, but it parsers correctly,
        returning an error if it does not fit the grammar.

        Its structure is a bit complex: Firstly this function defines consume() and peek() in terms of the
        inputed TokenList for better readbility.
        Afterwards it defines one function for each production rule in the LL(1) grammar: expr(), expr_()
        lexpr(), lexpr_(), pexpr(). 
        They work by calling each other making decisions based on the single next token peeked. 

        After each function is defined inside the scope of 'parse()' we call 'expr()' to parse an expression.  
