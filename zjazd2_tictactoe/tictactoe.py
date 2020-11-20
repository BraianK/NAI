class TicTacToe:
    """Klasa definiująca grę w kółko i krzyżyk

    Atrybuty:
        winner (str): Przechowuje symbol zwycięzcy
        fields_board (array[str]): Lista pól
    """
    def __init__(self):
        self.fields_board = [' ' for _ in range(9)]
        self.winner = None
    """Metoda wypisująca plansze do gry"""
    def print_fields_board(self):
        for row in [self.fields_board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_fields_board_scheme():
        """Metoda zwracająca schemat pól na planszy"""
        number_fields_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_fields_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, field, player_symbol):
        """Metoda zapisująca ruch na planszy i wywołująca metodę czy mamy zwycięzcę

        Parametry wejściowe:
            field (int): numer pola na planszy
            player_symbol (str): oznaczenie gracza

        Parametry wyjściowe:
            boolean: potwierdzenie zapisania ruchu
        """
        if self.fields_board[field] == ' ':
            self.fields_board[field] = player_symbol
            if self.check_is_winner(player_symbol):
                self.winner = player_symbol
            return True
        return False

    def check_is_winner(self, player_symbol):
        """Metoda sprawdzają czy mamy zwycięzce

        Parametry wejściowe:
            player_symbol (str): oznaczenie gracza

        Parametry wyjściowe:
            boolean: zmienna określająca czy jest zwycięzca
        """
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
        """Metoda sprawdzająca ilość pustych pól

        Parametry wyjściowe:
            int: ilość pustych pól
        """
        return self.fields_board.count(' ')

    def possible_moves(self):
        """Metoda sprawdzająca możliwe ruchy

        Parametry wyjściowe:
            array[int]: indeksy możliwych ruchów
        """
        return [i for i, x in enumerate(self.fields_board) if x == ' ']

