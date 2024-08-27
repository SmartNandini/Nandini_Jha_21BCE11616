class Game:
    def __init__(self):
        self.grid = [['' for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'
        self.players = {'A': [], 'B': []}
        self.positions = {'A': {}, 'B': {}}  # Track character positions

    def initialize_game(self, player_a: list, player_b: list):
        self.players['A'] = player_a
        self.players['B'] = player_b

        # Ensure the order is P1, P2, H1, H2, P3
        self.grid[0] = ['A-' + ch for ch in player_a] if len(player_a) == 5 else self.grid[0]
        self.grid[4] = ['B-' + ch for ch in player_b] if len(player_b) == 5 else self.grid[4]

        # Store initial positions
        self.positions['A'] = {ch: (0, i) for i, ch in enumerate(player_a)}
        self.positions['B'] = {ch: (4, i) for i, ch in enumerate(player_b)}

    def reset_game(self):
        self.grid = [['' for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'
        self.players = {'A': [], 'B': []}
        self.positions = {'A': {}, 'B': {}}  # Track character positions


    def validate_move(self, player: str, character: str, direction: str):
        if character not in self.positions[player]:
            return False
        
        x, y = self.positions[player][character]
        
        if character.startswith('P'):
            if direction == 'L':
                new_x, new_y = x, y - 1
            elif direction == 'R':
                new_x, new_y = x, y + 1
            elif direction == 'F':
                new_x, new_y = (x - 1, y) if player == 'A' else (x + 1, y)
            elif direction == 'B':
                new_x, new_y = (x + 1, y) if player == 'A' else (x - 1, y)
            else:
                return False
        elif character.startswith('H1'):
            if direction == 'L':
                new_x, new_y = x, y - 2
            elif direction == 'R':
                new_x, new_y = x, y + 2
            elif direction == 'F':
                new_x, new_y = (x - 2, y) if player == 'A' else (x + 2, y)
            elif direction == 'B':
                new_x, new_y = (x + 2, y) if player == 'A' else (x - 2, y)
            else:
                return False
        elif character.startswith('H2'):
            if direction == 'FL':
                new_x, new_y = (x - 2, y - 2) if player == 'A' else (x + 2, y + 2)
            elif direction == 'FR':
                new_x, new_y = (x - 2, y + 2) if player == 'A' else (x + 2, y - 2)
            elif direction == 'BL':
                new_x, new_y = (x + 2, y - 2) if player == 'A' else (x - 2, y + 2)
            elif direction == 'BR':
                new_x, new_y = (x + 2, y + 2) if player == 'A' else (x - 2, y - 2)
            else:
                return False
        else:
            return False

        # Check bounds
        if not (0 <= new_x < 5 and 0 <= new_y < 5):
            return False

        # Check for friendly fire
        if self.grid[new_x][new_y] and self.grid[new_x][new_y].startswith(player):
            return False

        return True

    def make_move(self, player: str, character: str, direction: str):
        if not self.validate_move(player, character, direction):
            return False
        
        x, y = self.positions[player][character]
        
        # Determine the new position based on the direction
        if character.startswith('P'):
            if direction == 'L':
                new_x, new_y = x, y - 1
            elif direction == 'R':
                new_x, new_y = x, y + 1
            elif direction == 'F':
                new_x, new_y = (x - 1, y) if player == 'A' else (x + 1, y)
            elif direction == 'B':
                new_x, new_y = (x + 1, y) if player == 'A' else (x - 1, y)
        elif character.startswith('H1'):
            if direction == 'L':
                new_x, new_y = x, y - 2
            elif direction == 'R':
                new_x, new_y = x, y + 2
            elif direction == 'F':
                new_x, new_y = (x - 2, y) if player == 'A' else (x + 2, y)
            elif direction == 'B':
                new_x, new_y = (x + 2, y) if player == 'A' else (x - 2, y)
        elif character.startswith('H2'):
            if direction == 'FL':
                new_x, new_y = (x - 2, y - 2) if player == 'A' else (x + 2, y + 2)
            elif direction == 'FR':
                new_x, new_y = (x - 2, y + 2) if player == 'A' else (x + 2, y - 2)
            elif direction == 'BL':
                new_x, new_y = (x + 2, y - 2) if player == 'A' else (x - 2, y + 2)
            elif direction == 'BR':
                new_x, new_y = (x + 2, y + 2) if player == 'A' else (x - 2, y - 2)

        # Update the grid
        self.grid[x][y] = ''
        self.grid[new_x][new_y] = f'{player}-{character}'

        # Update the character's position
        self.positions[player][character] = (new_x, new_y)

        # Switch turns
        self.current_turn = 'B' if self.current_turn == 'A' else 'A'

        return True

    def check_game_over(self):
        # Check if one player has no characters left
        a_characters_remaining = any(self.grid[0][j].startswith('A') for j in range(5))
        b_characters_remaining = any(self.grid[4][j].startswith('B') for j in range(5))

        if not a_characters_remaining:
            return "Player B wins!"
        elif not b_characters_remaining:
            return "Player A wins!"

        return None

    def get_game_state(self):
        return {
            'grid': self.grid,
            'turn': self.current_turn
        }
