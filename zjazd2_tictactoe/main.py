# https://pl.wikipedia.org/wiki/K%C3%B3%C5%82ko_i_krzy%C5%BCyk
# Paweł Szyszkowski s18184, Braian Kreft s16723
# Środowisko nie wymaga przygotowania


from player import HumanPlayer, AiPlayer
from tictactoe import TicTacToe


def start_game(game, player_x, player_o):
    """Metoda startująca rozgrywkę

    Parametry wejściowe:
        game (TicTacToe): instancja gry
        player_x (Player): instancja obiektu gracza posiadającego znak X
        player_o (Player): instancja obiektu gracza posiadającego znak O
    """
    game.print_fields_board_scheme()

    player_symbol = 'X'
    while game.empty_fields_count():
        if player_symbol == 'O':
            field = player_o.get_move(game)
        else:
            field = player_x.get_move(game)

        if game.make_move(field, player_symbol):

            print(player_symbol + ' moved to field ' + str(field))
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
