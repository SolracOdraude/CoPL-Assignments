student number: s3647048
student name: Carlos Eduardo Moreira Mendes
assignment status: completed.

Operational system used: Ubuntu 22.04.3 LTS (64-bit) 
Compiler version: GCC 11.4.0
Language used: Python 3.10.12


Notes: period/dot operator ('.') does not always work as intended, use parenthesis for proper results.


The code structure was devided into 3 files:
    
    1. lexical_analysis.py 

        This file implements the classes 'Token', 'TokenList' and the function 'tokenize()'.
        
        'Token' is an abstraction from the pair (type, name) that we desire each token to have.
        Since 'name' is only applicable for variables, other types will save the system's prefered 
        representation of the Token type there. e.g.: Token('lambda', 'λ') 

        'TokenList' abstracts from a list of Token's, allowing us to implement and use the methods: 
            TokenList.peek() and 
            TokenList.consume(token_type)

        As suggested in the video lectures, '.peek()' returns the current Token that we are trying to parse,
        while '.consume(token_type)' will delete the current token, raising an error if there was nothing to
        consume or if the consumed Token type was different than the intended (passed as argument).

        The function 'tokenize()' will take as parameter one string (intended to be a line from standard input)
        and return the TokenList related to the expression read. 


    2. syntactical_analysis.py

        This file implements the function 'parse()' and a tree-like structure to represent the lambda expressions.
        
        The tree-like strucure is represented via the classes: 
            'ApplicationNode', which points to an expression on .left and another on .right; 
            'LambdaNode' which points to a variable name and to the body on .right;
            'VariableLeaf' which points to a variable name.

        These classes have a '__repr__' method that allows for a inline respresentation expression tree.

        The function 'parse()' takes a TokenList and attemps to parse the Tokens using recursion, outputing the root 
        to the tree structure. 

        The code in 'parse()' is as follows: Firstly this function defines 'consume()' and 'peek()' in terms of the
        inputed TokenList for better usability and readbility. Afterwards it defines one function for each production 
        rule in the LL(1) grammar: expr(), expr_(), lexpr(), lexpr_() and pexpr(). (Grammar can be found in comments)
        They work by calling each other making decisions based on the single next token peeked. 

        After each function is defined inside the scope of 'parse()' we call and return 'expr()' to parse the expression.    


    3. main.py

        'main.py' simply imports 'tokenize()' and 'parse()' from the previous files and unites them together with the
        standard input to respond to user interation. The program reads each line of the input as its own isolated expression,
        it also ignores lines with only spaces in the input.

        Output follows the same order of input, with error messages for illegal inputs or when parsing fails. There are 4 
        possible errors detected, 2 from lexical analysis: 'Illegal variable name', 'Character not recognized'. And 2 from 
        syntactical analysis: 'Expected {some_token} found {other_token}' (input not in grammar) or 'No token to consume', 
        meaning the program expected more input at the end (like a closing parenthesis for instance).

        The files 'lexical_analysis.py' and 'syntactical_analysis.py' can be run as scripts as well, however error
        messages and output format are not as polished in those files. In 'lexical_analysis' the output is the TokenList
        for each line of the input, while in 'syntactical_analysis' the output are the expressions understood by the parser.
