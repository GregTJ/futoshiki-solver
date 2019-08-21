from puzzle import Puzzle

if __name__ == '__main__':
    # Wait for valid user input (a puzzle file.)
    while True:
        fn = input('Puzzle file: ')
        try:
            p = Puzzle.read_puzzle(fn)
            break

        except FileNotFoundError:
            print(f'File "{fn}" not found.')

    print('Unsolved:')
    print(p)

    if p.solve():
        print('Solved:')
        print(p)

    else:
        print('Puzzle is unsolvable.')

    input()
