student number: s3647048
student name: Carlos Eduardo Moreira Mendes
assignment status: completed.

Operational system used: Ubuntu 22.04.3 LTS (64-bit) 
Compiler version: GCC 11.4.0
Language used: Python 3.10.12

Notes: period/dot operator ('.') does not always work as intended, use parenthesis for proper results.


Obs: The files 'lexical_analysis.py' and 'syntactical_analysis.py' are excatly the same as they
were implemented in assignment_1. The only new changes to the code structure are the changes to main.py
and the new file 'interpreter.py'. 
(Still, for completeness, their individual explanations are also included in this document.)

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


    3. interpreter.py

        This file adds 3 more function that interact with the tree structure defined in systanctial_analysis.py:

            - 'free_variables()' which takes a tree strucure and returns all free variables of the expression.

            - 'substitute()' which takes a tree strucutre a target variable and a replacement strucure. It returns a copy
            of the passed strucure where every free occurance of the targe variable node is substituted by the replacement 
            tree strucure. It peforms alpha-conversions if needed (i.e. if a unintended variable capture would occur)

            - and lastly 'interpret()', the main function, which returns a reduced copy of the inputed tree structure.
            It recursivelly calls itself, reducing the tree in a top-down strategy.
        
        Additionally, I've defined one extra function: 'get_fresh_variable()', which takes a set of variable names and
        returns a new variable name not found in there. It is mainly used to perform alpha-conversions, renaming variables
        names before a substitution that would cause unwanted conflicts.
  

    4. main.py

        This file imports 'tokenize()', 'parse()' and 'interpret()' from the previous files and implements the commandline
        options to receive the file and ajust the beta-reduction step limit. The main.py script handles all errors, outputing
        them to the user with helpful messages.

        Only the first non-empty line from the input file will be read, as the program assumes that is the intended expression to
        be reduced. Furthermore, there is no way to change the system's strategy, the top down recursive approach is the only
        strategy the program is set to use.
