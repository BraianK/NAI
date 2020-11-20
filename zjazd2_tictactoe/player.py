class Player:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol

    def make_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, player_symbol):
        super().__init__(player_symbol)

    def make_move(self, game):
        valid_filed = False
        val = None
        while not valid_filed:
            filed = input(self.player_symbol + '\'s turn. Input move (0-8): ')
            try:
                val = int(filed)
                if val not in game.possible_moves():
                    raise ValueError
                valid_filed = True
            except ValueError:
                print('Invalid filed. Try again.')
        return val


class AiPlayer(Player):
    def __init__(self, player_symbol):
        super().__init__(player_symbol)

    def make_move(self, game):
        if game.empty_fields_count() == 9:
            return 0
        return self.minimax(game, self.player_symbol)['move']

    def minimax(self, game_simulation, player):
        max_player = self.player_symbol
        other_player = 'O' if player == 'X' else 'X'

        if game_simulation.winner == other_player:
            return {'move': None, 'rate': 1 * (game_simulation.empty_fields_count() + 1) if other_player == max_player else -1 * (
                        game_simulation.empty_fields_count() + 1)}
        elif not game_simulation.empty_fields_count():
            return {'move': None, 'rate': 0}

        if player == max_player:
            best = {'move': None, 'rate': -9999 }
        else:
            best = {'move': None, 'rate': 9999}
        for possible_move in game_simulation.possible_moves():
            game_simulation.make_move(possible_move, player)
            simulation_result = self.minimax(game_simulation, other_player)
            game_simulation.fields_board[possible_move] = ' '
            game_simulation.winner = None
            simulation_result['move'] = possible_move

            if player == max_player:
                if simulation_result['rate'] > best['rate']:
                    best = simulation_result
            else:
                if simulation_result['rate'] < best['rate']:
                    best = simulation_result
        return best
