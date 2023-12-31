student number: s3647048
student name: Carlos Eduardo Moreira Mendes
assignment status: completed.

Operational system used: Ubuntu 22.04.3 LTS (64-bit) 
Compiler version: GCC 11.4.0
Language used: Python 3.10.12

Notes: period/dot operator ('.') does not always work as intended, use parenthesis for proper results.


The code structure was devided into 4 files:
    
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

        The function 'tokenize()' will take as parameter one string and return the TokenList related to the expression read. 


    2. syntactical_analysis.py

        This file implements the function 'parse()' and a tree-like structure to represent the lambda expressions.
        
        The tree-like strucure is represented via the classes:
            'JudgementNode', which points to a lambda expression and a type expression.
            'ApplicationNode', which points to an expression on .left and another on .right; 
            'LambdaNode' which points to a variable name and to the body on .right;
            'TypeArrowNode', which points to two type expressions (.left and .right);
            'VariableLeaf', which points to a variable name.
            'TypeLeaf', which points to a Type name.

        These classes have a '__repr__' method that allows for a inline respresentation of the expression tree.

        The function 'parse()' takes a TokenList and attemps to parse the Tokens using recursion, outputing the root 
        to the tree structure. 

        The code in 'parse()' is as follows: Firstly this function defines 'consume()' and 'peek()' in terms of the
        inputed TokenList for better usability and readbility. Afterwards it defines one function for each production 
        rule in the LL(1) grammar: judg(), expr(), expr_(), lexpr(), pexpr(), type(), type_(). 
        (Grammar used can be found in comments)

        These functions work by recusivelly calling each other, making decisions based on the single next token peeked. 

        After each function is defined inside the scope of 'parse()' we call and return 'judg()' to parse the judgement.


    3. type_checker.py

        This file implements two function to help asserting the judgement:
            
            - 'interpret()' which will interpret the type of an expression by using the 3 rules discussed in the video lecture.
            It uses two arguments: tree and context. The variable 'tree' points to the root of the tree we are looking at,
            while 'context' will keep track of the known variable types throughtout the recursive process.

            - 'assert_judgement' which takes a JudgementNode (root of the tree) and splits it into expression and type.
            Then, it calls interpret on the lambda expression to check if it yields the same type as the one in the judgement.

    4. main.py

        This file imports 'tokenize()', 'parse()' and 'assert_judgement' from the previous files and implements the commandline
        options to receive the file containing one or more judgments. The main.py script handles all errors, outputing
        them to the user with helpful messages.
