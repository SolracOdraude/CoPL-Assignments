from syntactical_analysis import VariableLeaf, TypeLeaf, JudgementNode, \
                                 LambdaNode, ApplicationNode, TypeArrowNode

def interpret(tree, context=None):
    ''' Recursive function to reduce the left tree into a final type. '''
    if context is None:
        context = dict()

    match tree:
        
        case TypeLeaf():
            return tree

        case TypeArrowNode():
            return tree

        case VariableLeaf():
            if tree.name in context:
                return context[tree.name]
            raise TypeError(f"Unknown type for variable '{tree.name}'.")

        case LambdaNode():
            context[tree.var] = tree.var_type
            codomain = interpret(tree.right, context.copy())
            return TypeArrowNode(tree.var_type, codomain)

        case ApplicationNode():
            type_left = interpret(tree.left, context.copy())
            type_right = interpret(tree.right, context.copy())

            if type(type_left) == TypeArrowNode:
                if str(type_right) == str(type_left.left):
                    return type_left.right
                else:
                    raise TypeError(f"During application '{tree}', expected input of type '{type_left.left}' instead got '{type_right}'.")

            else:
                # I don't think it should even reach here.
                return ApplicationNode(type_left, type_right)


def assert_judgement(tree):
    if type(tree) != JudgementNode:
        raise TypeError('Expression is not a judgment. Can only type-check a judgment.')

    expression = interpret(tree.left)
    target_type = tree.right

    return str(expression) == str(target_type)


if __name__ == '__main__':
   
    import sys
    from lexical_analysis import tokenize
    from syntactical_analysis import parse

    for line in sys.stdin.readlines():
        tokens = tokenize(line)
        lambda_tree = parse(tokens)
        if assert_judgement(lambda_tree):
            print(lambda_tree)
        else:
            print(False)
