class Puzzle:
    __slots__ = {'puzzle', 'constraints', 'size'}

    def __init__(self, puzzle, constraints, size):
        self.puzzle = puzzle
        self.constraints = constraints
        self.size = size

    def __str__(self):
        """Magic method for converting puzzle object to text representation."""
        output = ['|', '|']

        for i, j in enumerate(zip(self.puzzle, self.constraints)):
            # Determine if current square is at the end or interior of a row.
            interior = bool((i + 1) % self.size)

            # Pad for interior squares.
            pad = ' ' * interior

            # Determine the constraint symbols for current square if they exist.
            constraints = (('<' * bool(j[1] & 1)) or ('>' * bool(j[1] & 2)),
                           ('^' * bool(j[1] & 4)) or ('v' * bool(j[1] & 8)))

            # Write square constraints and values to last 2 output lines with proper padding.
            output[-2] += f"{j[0] or '-'}{constraints[0] or pad}"
            output[-1] += f"{constraints[1] or ' '}{pad}"

            # Create new lines when current lines reach the edge of the puzzle
            # unless loop has reached the bottom of the puzzle.
            if not interior and i != self.size ** 2 - 1:
                output += ['|', '|']

        # Return concatenated output with size prepended.
        # Also trim final line which will always be blank for properly formatted puzzles.
        output = '|\n'.join(output[:-1])
        return f"{self.size}\n{output}|\n"

    @classmethod
    def read_puzzle(cls, filename):
        """Class method for converting text representation of puzzle into puzzle object."""
        with open(filename, 'r') as file:
            # Read puzzle size.
            size = int(file.read(1))

            # Remove superfluous characters, change constraint symbols to powers of two,
            # and change hyphens and spaces to zeros.
            # Lastly split string into list elements delimited by newlines.
            translator = str.maketrans(' -<>^v', '001248', '|')
            data = file.read().strip().translate(translator).split('\n')

            # Deinterleave and flatten data into constraint and puzzle lists.
            puzzle = [int(j) for i in data[::2] for j in i[::2]]
            constraints = [int(j) for i in data[1::2] for j in i[::2]]

            # Pad constraints.
            constraints += [0] * size

            # Increment constraint values based on remaining interleaved constraints.
            for i, x in enumerate(data[::2]):
                for j, y in enumerate(x[1::2]):
                    constraints[i * size + j] += int(y)

            return cls(puzzle, constraints, size)

    def solve(self):
        """A recursive backtracking method to solve futoshiki puzzles."""
        def index(i, j):
            # 2D Index -> Flat Index (Row Major)
            return i * self.size + j

        def inverse_index(i):
            # Flat Index -> 2D Index (Row Major)
            return i // self.size, i % self.size

        def is_legal(square, new_value):
            def comparator(a, b):
                def view(i):
                    # View square at index i, substitutes value of current square with new_value
                    # to avoid directly modifying the puzzle or creating a copy.
                    return new_value if i == square else self.puzzle[i], self.constraints[i]

                # Flatten 2d indices.
                flat = index(*a), index(*b)

                # Verify second square is within puzzle.
                if flat[1] >= self.size ** 2:
                    return True

                # Read squares from puzzle into tuple for comparison,
                # swap squares if square b is before a in the flattened list.
                swap = (flat[1] > flat[0]) * 2 - 1
                views = tuple(view(f) for f in flat[::swap])

                # Every edge between adjacent squares
                # may have one of two possible constraints, check for both.
                for power in range(2):
                    # If squares a and b are in the same column,
                    # check for vertical constraints instead of horizontal ones.
                    if a[1] == b[1]:
                        power += 2

                    if all((2 ** power & views[0][1],  # Check if the first square has constraints.
                            views[1][0] != 0,  # Skip inequality if second square is empty.
                            not views[power % 2][0] < views[not power % 2][0])):  # Check actual inequality.
                        return False

                return True

            # Get 2D index from flat index.
            row, col = inverse_index(square)

            # Check for duplicate values in row and column of the modified square.
            row_slice = self.puzzle[index(row, 0):index(row, self.size)]
            col_slice = self.puzzle[index(0, col):index(self.size, col):self.size]
            if new_value in row_slice or new_value in col_slice:
                return False

            # Check constraints between squares adjacent to the modified square.
            stencil = ((0, 1), (1, 0), (0, -1), (-1, 0))
            for x in stencil:
                if not comparator((row, col), (row + x[0], col + x[1])):
                    return False

            return True

        try:
            # Find first empty square.
            empty = self.puzzle.index(0)

        # If there are no empty squares the puzzle has been solved.
        except ValueError:
            return True

        # Iterate over potential values.
        for n in range(self.size):

            # Check legality of setting the empty square to n.
            if is_legal(empty, n + 1):
                self.puzzle[empty] = n + 1

                # Recursively solve.
                if self.solve():
                    return True

                # Backtrack from dead end partial solutions.
                else:
                    self.puzzle[empty] = 0

        # Return false if puzzle is unsolvable.
        return False

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
