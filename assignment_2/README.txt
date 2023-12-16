student number: s3647048
assignment status: done (for now at least).

Notes: period/dot operator ('.') does not always work as intended, use parenthesis for proper results.


The code structure was devided into 4 files:
    
    1. lexical_analysis.py 

        This file implements the classes 'Token', 'TokenList' and the function 'tokenize()'.
        
        'Token' is an abstraction from the pair (type, name) that we desire each token to have.
        Since 'name' is only applicable for variables, other types will save the system's prefered 
        representation of the Token type there. e.g.: Token('lambda', 'λ') 

        'TokenList' abstracts from a list of Token's, allows us to implement and use the methods: 
            TokenList.peek() and 
            TokenList.consume(token_type)

        As suggested in the video lectures, '.peek()' returns the current Token that we are trying to parse,
        while '.consume(token_type)' will delete the current token, raising an error if there was nothing to
        consume or if the consumed Token type was different than the intended (passed as argument).

        The function 'tokenize()' will that as parameter a string (intended to be a line from standard input)
        and return a TokenList. 


    2. syntactical_analysis.py

        This file implements the function 'parse()' and a tree-like structure to represent the lambda expressions.
        
        The tree-like strucure is represented via the classes 'ApplicationNode', which points to an expression on 
        .left and another on right; 'LambdaNode' which takes a variable and point to the body on .right; and finally
        the 'VariableLeaf' which points to a variable name.
        These classes have a '__repr__' method that allows the response to the user as an expression.

        The function 'parse()' takes a TokenList and attemps to parse the Tokens using recursively, outputing the root 
        to the tree structure, however users can only see its visual representation as output. 

        The code in 'parse()' is a bit complex: Firstly this function defines 'consume()' and 'peek()' in terms of the
        inputed TokenList for better usability and readbility. Afterwards it defines one function for each production 
        rule in the LL(1) grammar: expr(), expr_(), lexpr(), lexpr_() and pexpr(). (Grammar can be found in comments)
        They work by calling each other making decisions based on the single next token peeked. 

        After each function is defined inside the scope of 'parse()' we call and return 'expr()' to parse the expression.

    3. interpret.py
  
    4. main.py



