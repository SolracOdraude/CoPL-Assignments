if __name__ == '__main__':
    
    # Obs: this file is only meant to be used as an script

    import sys 
    from lexical_analysis import tokenize
    from syntactical_analysis import parse

    exit_code = 0

    for number, line in enumerate(sys.stdin.readlines(), start=1):
        if number == 1:
            print('-'*32)
        line = line.strip()
        if not line:
            # skip over empty lines    
            continue
        
        try:     
            tokens = tokenize(line)
            expression_tree = parse(tokens)
            print(expression_tree)

        except Exception as error:
            print(f'Error on line {number}: {error}')
            exit_code = 1

    sys.exit(exit_code)
