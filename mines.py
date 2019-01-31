from os import system
from sys import exit


class Board:
    from collections import namedtuple
    CHOICE_RESULT = namedtuple('choice_result', ['valid', 'invalid', 'mine'])

    def __init__(self, difficulty):
        self.board = self._make_board(difficulty)
        self._set_mines(difficulty)
        self.cleared = set([])

    @staticmethod
    def _make_board(difficulty):
        size = 5 if difficulty == 'e' else (10 if difficulty == 'm' else 20)
        return [[None] * size for _ in range(size)]

    def _set_mines(self, difficulty):
        from random import sample

        num_mines = 7 if difficulty == 'e' else (30 if difficulty == 'm' else 80)

        for i, j in sample([(i, j) for i in range(len(self)) for j in range(len(self))], num_mines):
            self[i][j] = True

    def __getitem__(self, item):
        return self.board[item]

    def __str__(self):
        return '\n'.join([
            '\t' + ' '.join([
                '?' if (i, j) not in self.cleared else '_' for j in range(len(self))
            ]) for i in range(len(self))
        ])

    def __len__(self):
        return len(self.board)

    def choose_square(self, i, j):
        mine, invalid = self[i][j] is not None, (i, j) in self.cleared
        valid = not mine and not invalid
        result = self.CHOICE_RESULT(
            mine=mine,
            invalid=invalid,
            valid=valid
        )

        if valid:
            stack = [(i, j)]
            while stack:
                x, y = stack.pop()
                self.cleared.add((x, y))

                for nbr in self.neighbors(x, y):
                    self.cleared.add(nbr)
                    stack.append(nbr)

        return result

    def neighbors(self, i, j):
        nbrs = []

        for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            in_grid = min(x, y) >= 0 and max(x, y) < len(self)
            not_yet_cleared = (x, y) not in self.cleared
            not_mine = in_grid and self[x][y] is None

            if in_grid and not_yet_cleared and not_mine:
                nbrs.append((x, y))

        return nbrs


class Game:
    def __init__(self, board=None):
        self.board = board

    def start(self):
        self.set_difficulty()
        print('(mines at {})'.format([(i, j) for i in range(len(self.board)) for j in range(len(self.board)) if self.board[i][j]]))
        self.play()

    def set_difficulty(self):
        self.print_header()
        diff = input('Choose difficulty ([e]asy, [m]edium, or [h]ard): ').lower()

        while diff not in {'e', 'm', 'h'}:
            diff = input(
                "Sorry, I don't recognize difficulty \"{}\". Enter 'e' for easy, 'm' for medium, or 'h' for hard: "
                .format(diff)
                .lower()
            )

        self.board = Board(diff)

    def play(self):
        self.print_board()

        while True:
            choice = input("Choose your square: ").split()
            while len(choice) != 2 or not all([val.isnumeric() and 1 <= int(val) <= len(self.board) for val in choice]):
                choice = input("Please enter 2 valid coordinates separated by a space (e.g.: 1 2): ").split()

            # Input indices are 1-based, not 0-based, so we subtract 1
            result = self.board.choose_square(int(choice[0]) - 1, int(choice[1]) - 1)

            if result.mine:
                play_again = input("Ouch! that's a mine ;(\nPlay again?: (Y/n): ").lower()
                if play_again == 'y':
                    self.start()
                    break
                else:
                    print('Thanks for playing!')
                    exit()
            elif result.invalid:
                print('That square has already been checked. Please choose another\n')
            else:
                self.print_board()

    @staticmethod
    def print_header():
        system('clear')
        print('\t***************************')
        print('\t******* MINESWEEPER *******')
        print('\t***************************\n')

    def print_board(self):
        self.print_header()
        print(self.board)


if __name__ == '__main__':
    Game().start()
