# https://pl.wikipedia.org/wiki/K%C3%B3%C5%82ko_i_krzy%C5%BCyk
# Paweł Szyszkowski s18184, Braian Kreft s16723
# Środowisko nie wymaga przygotowania


from player import HumanPlayer, AiPlayer


class TicTacToe:

    def __init__(self):
        self.fields_board = [' ' for _ in range(9)]
        self.winner = None

    def print_fields_board(self):
        for row in [self.fields_board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_fields_board_scheme():
        """Returned argument a is squared."""
        number_fields_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_fields_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, player_symbol):
        if self.fields_board[square] == ' ':
            self.fields_board[square] = player_symbol
            if self.check_is_winner(player_symbol):
                self.winner = player_symbol
            return True
        return False

    def check_is_winner(self, player_symbol):
        for row in [self.fields_board[i * 3:(i + 1) * 3] for i in range(3)]:
            if all([symbol == player_symbol for symbol in row]):
                return True
        for i in range(3):
            if all([symbol == player_symbol for symbol in [self.fields_board[i + j * 3] for j in range(3)]]):
                return True
        if all([s == player_symbol for s in [self.fields_board[i] for i in [0, 4, 8]]]):
            return True
        if all([s == player_symbol for s in [self.fields_board[i] for i in [2, 4, 6]]]):
            return True

        return False

    def empty_fields_count(self):
        return self.fields_board.count(' ')

    def possible_moves(self):
        return [i for i, x in enumerate(self.fields_board) if x == ' ']


def start_game(game, player_x, player_o):
    game.print_fields_board_scheme()

    player_symbol = 'X'
    while game.empty_fields_count():
        if player_symbol == 'O':
            square = player_o.make_move(game)
        else:
            square = player_x.make_move(game)

        if game.make_move(square, player_symbol):

            print(player_symbol + ' moved to field ' + str(square))
            game.print_fields_board()
            print('')

            if game.winner:
                print(player_symbol + ' is winner!!!')
                return player_symbol
            player_symbol = 'O' if player_symbol == 'X' else 'X'

    print('It\'s a draw!')


print('Select game mode. \n[1] Human vs Human\n[2] AI vs Human \n[3] Human vs AI \n[4] AI vs AI')
game_mode = None
player_x = None
player_o = None
while not game_mode:
    game_mode = input('Game mode: ')
    if game_mode == '1':
        player_x = HumanPlayer('X')
        player_o = HumanPlayer('O')
    elif game_mode == '2':
        player_x = AiPlayer('X')
        player_o = HumanPlayer('O')
    elif game_mode == '3':
        player_x = HumanPlayer('X')
        player_o = AiPlayer('O')
    elif game_mode == '4':
        player_x = AiPlayer('X')
        player_o = AiPlayer('O')
    else:
        print("Out of range")
        game_mode = None
game_instance = TicTacToe()
start_game(game_instance, player_x, player_o)
