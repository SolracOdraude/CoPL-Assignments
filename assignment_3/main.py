if __name__ == '__main__':
    
    # Obs: this file is only meant to be used as an script

    import sys 
    from argparse import ArgumentParser

    from lexical_analysis import tokenize
    from syntactical_analysis import parse
    from type_checker import assert_judgement


    # Setting up command line arguments:

    cmd_line = ArgumentParser(description='')
    
    cmd_line.add_argument('filepath',   # Positional argument
                            default=None,
                            help='Relative filepath to target file containing one or more judgements (one judgement per line!).')

    # Retriving values from command line:

    args = cmd_line.parse_args()

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

    lines = []

    for line in file_contents:
        line = line.strip()
        if not line:    # Empty line
            continue
        lines.append(line)

    if not lines:
        print('Error: Empty file, could not find any judgments.')
        sys.exit(1)

    
    # Attempting to parse the lines:
    exit_code = 0

    for line in lines:
        # Trying to parse the line
        try:
            tree = parse(tokenize(line))
        except Exception as error:
            print(f"Error: Could not parse or tokenize judgment '{line}'. ({error})")
            exit_code = 1
            continue

        # Trying to assert judgment
        try:
            if assert_judgement(tree):
                print(tree)
            else:
                exit_code = 1
        except Exception as error:
            print(f'Error: Exception raise during judgement check: {error}')

    sys.exit(exit_code)
