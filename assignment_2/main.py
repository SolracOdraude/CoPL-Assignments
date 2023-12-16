if __name__ == '__main__':
    
    # Obs: this file is only meant to be used as an script

    import sys 
    from argparse import ArgumentParser

    from lexical_analysis import tokenize
    from syntactical_analysis import parse
    from interpreter import interpret


    # Setting up command line arguments:

    cmd_line = ArgumentParser(description='')
    
    cmd_line.add_argument('filepath',   # Positional argument
                            default=None,
                            help='Relative filepath to target file containing an lambda expression.')

    cmd_line.add_argument('-l', '--limit',
                            default=1000,
                            help='Maximum number beta-reduction that can be executed. (Must be a non-negative integer)')

    # Retriving values from command line:

    args = cmd_line.parse_args()

    if type(args.limit) != int or args.limit < 0:
        print("Error: Invalid command line argument: 'limit'. (Must be a non-negative integer)") 
        sys.exit(1)

    if args.filepath is None:
        print('Error: You must give a filepath to allow program execution.')
        sys.exit(1)

    try:
        with open(args.filepath, 'r') as file:
            file_contents = file.readlines()

    except FileNotFoundError:
        print(f'Error: Filepath {args.filepath} not found.')
        sys.exit(1)

    except OSError:
        print(f'Error: OSError exception while trying to open filepath {args.filepath}')
        sys.exit(1)

    except Exception as error:
        print(f'Error: Unexpected exception while opening {args.filepath}. ({error})')
        sys.exit(1)


    # Reading the first 'valid' line in file:

    for line in file_contents:
        line = line.strip()
        if not line:    # Empty line
            continue
        break
    else:
        # Meaning only empty lines
        print('Error: Empty file, could not find an expression to parse.')
        sys.exit(1)

    
    # Attempting to parse the line:

    try:
        tree = parse(tokenize(line))
    except Exception as error:
        print(f'Error: Exception raise while trying to parse expression. ({error})')
        sys.exit(1)


    # Setting limit to 'interpret' function:
    sys.setrecursionlimit(args.limit)

    # Interpreting expression tree:
    try:
        simple_tree = interpret(tree)

    except RecursionError as error:
        print(f'Error: Could not reduce tree in only {args.limit} beta-reductions. ({error})')
        sys.exit(2)

    except Exception as error:
        print(f'Error: Unexpected exception while trying to interpret expression tree. ({error})')
        sys.exit(1) 


    # Success!
    print(simple_tree)
    sys.exit(0)           
