import unittest
from puzzle import Puzzle


class TestPuzzle(unittest.TestCase):
    def test_4x4(self):
        puzzle = Puzzle.read_puzzle('4x4.txt')
        puzzle.solve()
        correct = Puzzle.read_puzzle('4x4 solution.txt')
        self.assertEqual(puzzle.puzzle, correct.puzzle)

    def test_5x5(self):
        puzzle = Puzzle.read_puzzle('5x5.txt')
        puzzle.solve()
        correct = Puzzle.read_puzzle('5x5 solution.txt')
        self.assertEqual(puzzle.puzzle, correct.puzzle)

    def test_6x6(self):
        puzzle = Puzzle.read_puzzle('6x6.txt')
        puzzle.solve()
        correct = Puzzle.read_puzzle('6x6 solution.txt')
        self.assertEqual(puzzle.puzzle, correct.puzzle)


if __name__ == '__main__':
    unittest.main()
