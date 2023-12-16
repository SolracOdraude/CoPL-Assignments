from string import ascii_lowercase
from copy import deepcopy
from syntactical_analysis import VariableLeaf, LambdaNode, ApplicationNode

# Bellow we will define a few functions that can work with the tree structure imported above:

def free_variables(tree):
    ''' Returns a set containing all free variables in the expression tree. '''
    match (tree):

        case VariableLeaf():
            return set(tree.name)

        case LambdaNode():
            return free_variables(tree.right) - set(tree.variable)

        case ApplicationNode():
            return free_variales(tree.left) | free_variables(tree.right)

        case _:
            raise TypeError("Improper tree format! Found an unknown node type in the tree.")


def get_fresh_variable(variable_set):
    ''' Return a new variable not present in the inputed set of variables. '''
    if len(variable_set) < 26:
        # Means we can get a single letter variable.
        return (set(ascii_lowercase) - variable_set).pop() 

    # else:
    num = 2
    while True:
        for letter in ascii_lowercase:
            if f'{letter}{num}' not in variable_set:
                return f'{letter}{num}'
        num += 1


def substitute(tree, variable, replacement):
    ''' Returns a copy of the tree structure after the substitution. 
        Obs:    'variable' should be a string while 
                'replacement' should be a Tree structure. '''

    match (tree):

        case VariableLeaf():
            # Tree is a single variable.
            if tree.name == variable:
                return replacement
            return deepcopy(tree)


        case ApplicationNode():
            return ApplicationNode( substitute(self.left,  variable, replacement),
                                    substitute(self.right, variable, replacement)  )

        case LambdaNode():
            if tree.variable == variable:
                return deepcopy(tree)

            replacement_free_variables = free_variables(replacement) 
            if tree.variable in replacement_free_variables:
                # Alpha-conversion:
                fresh_variable = get_fresh_variable(replacement_free_variables | free_variables(tree.right))
                new_right = substitute(tree.right, tree.variable, VariableLeaf(fresh_variable)) 
                return LambdaNode(fresh_variable, substitute(new_right, variable, replacement))

            # else: (Meaning replacement variables are fresh in our node)
            return LambdaNode(tree.variable, substitute(tree.right, variable, replacement))


        case _:
            raise TypeError("Improper tree format! Found an unknown node type in the tree.")


# This is a recursive function that calls itself to interpret the tree 
# structure built during the syntactical_analysis of the input.

def interpret(tree):
    ''' Returns a simplified (interpreted) copy of the tree structure inputed. '''

    # Variable "tree" actually refers to the root of the tree, meaning it is a node with pointers
    # the remaning of the tree is accessed via tree.right and tree.left when applicable.

    match (tree):

        case VariableLeaf():
            return deepcopy(tree)
            # Nothing to simplify here.

        case LambdaNode():
            return LambdaNode(tree.variable, interpret(tree.right))
            # Nothing much to do with a function node alone.
            # We can only simplify its RHS.


        case ApplicationNode():
        
            match (tree.left):
            
                case VariableLeaf():
                    # We can only simplify the RHS:
                    simple_right = interpret(tree.right)
                    return ApplicationNode(deepcopy(tree.left), simple_right)

                case LambdaNode():
                    function_application = substitute(tree.left.right, tree.left.variable, tree.right)    
                    return interpret(function_application)

                case ApplicationNode():
                    simple_left = interpret(tree.left)
                    if simple_left == tree.left:
                        # Infinite loop. -> (\x.(x x)) \x.(x x)
                        return deepcopy(tree)
                    return interpret(ApplicationNode(simple_left, deepcopy(tree.right)))                         

        case _:
            raise TypeError("Improper tree format! Found an unknown node type in the tree.")


if __name__ == '__main__':
    pass 
