import os


class Board:
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

        for i, j in sample([(i, j) for i in range(len(self.board)) for j in range(len(self.board[i]))], num_mines):
            self.board[i][j] = True

    def __str__(self):
        return 'baord!'

    def __len__(self):
        return len(self.board)

    def choose_square(self, i, j):
        pass


class Game:
    def __init__(self, board=None):
        self.board = board
        self.in_progress = True

    def start(self):
        self.set_difficulty()
        self.play()

    def set_difficulty(self):
        diff = input('Choose difficulty ([e]asy, [m]edium, or [h]ard): ')

        while diff not in {'e', 'm', 'h'}:
            diff = input(
                "Sorry, I don't recognize difficulty \"{}\". Enter 'e' for easy, 'm' for medium, or 'h' for hard: ".format(
                    diff))

        self.board = Board(diff)

    def play(self):
        while self.in_progress:
            self.print_board()

            choice = input("Choose your square: ").split()
            while len(choice) != 2 or not all([val.isnumeric() and 0 <= int(val) < len(self.board) for val in choice]):
                choice = input("Please enter 2 valid coordinates separated by a space (e.g.: 1 2): ").split()

            self.board.choose_square(int(choice[0], int(choice[1])))

    @staticmethod
    def print_header():
        os.system('clear')
        print('\t******* MINESWEEPER *******')
        print('\t***************************')

    def print_board(self):
        self.print_header()
        print(self.board)


if __name__ == '__main__':
    Game().start()
