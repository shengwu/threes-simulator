import copy
import itertools
import math
import random

class Board(object):
    # Variables for making moves 
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.board = [[None for _ in xrange(4)] for _ in xrange(4)]
        self.next_card = random.choice([1, 2, 3])

    def display(self):
        for row in self.board:
            print "{}\t{}\t{}\t{}".format(*row)

    def start(self):
        self.__init__()
        positions = list(itertools.product(range(4), repeat=2))
        random.shuffle(positions)

        # Add two or three cards of each value 1, 2, and 3
        for card in range(1, 4):
            for i in range(random.randint(2, 3)):
                pos = positions.pop()
                self.board[pos[0]][pos[1]] = card

    def score(self):
        score = 0
        for row in self.board:
            for card in row:
                if card < 3:
                    continue
                score += 3**(math.log(card/3, 2) + 1)
        return int(score)

    @staticmethod
    def can_merge(a, b):
        """Check if values a and b can merge. If so,
        return their sum."""
        if (a == 1 and b == 2) or (a == 2 and b == 1) or\
           (a > 2 and b > 2 and a == b):
            return a + b
        return False

    def get_adjacent(self, x, y):
        """Return a list of the neighbors of a board location"""
        adjacent = []
        if x > 0:
            adjacent.append(self.board[x-1][y])
        if x < 3:
            adjacent.append(self.board[x+1][y])
        if y > 0:
            adjacent.append(self.board[x][y-1])
        if y < 3:
            adjacent.append(self.board[x][y+1])
        return adjacent

    def can_move(self):
        """Check if it's possible to make a valid
        move on the current board"""
        for i in range(4):
            for j in range(4):
                card = self.board[i][j]
                if card is None:
                    continue
                neighbors = self.get_adjacent(i, j)
                if (None in neighbors) or \
                   (card == 1 and 2 in neighbors) or \
                   (card == 2 and 1 in neighbors) or \
                   (card > 2 and card in neighbors):
                    return True
        return False

    def set_next_card(self):
        """Generates a new card at random, depending on what's
        currently on the board. This card will be the next one
        introduced to the board."""
        candidates = [1, 2, 1, 2, 1, 2] # 1, 2 should be more likely
        max_card = max(map(max, self.board))
        candidates.extend([3*2**i\
                           for i in range(int(math.log(max_card/3, 2))+1)])
        next_card = random.choice(candidates)
        return next_card

    def preview_move(self, direction):
        """
        Given a direction, returns the resulting board
        after swiping in that direction.
        """
        if not self.can_move():
            return False

        # Keep track of where we can put the new card
        locations = []

        # Don't modify our board
        board = copy.deepcopy(self.board)

        if direction == Board.UP:
            for col in range(4):
                for row in range(3):
                    if board[row][col] is None:
                        # Shift remaining values up one
                        for i in range(row, 3):
                            board[i][col] = board[i+1][col]

                        # Add this to possible locations for new card
                        board[3][col] = None
                        locations.append((3, col))
                        break

                    # If there's a card here, see if it can be merged
                    val = Board.can_merge(board[row][col],
                                          board[row+1][col])
                    if val:
                        # If the values could be merged,
                        # set current position to their sum
                        board[row][col] = val

                        # Shift remaining values up one
                        for i in range(row+1, 3):
                            board[i][col] = board[i+1][col]

                        # Add this to possible locations for new card
                        board[3][col] = None
                        locations.append((3, col))
                        break

        elif direction == Board.DOWN:
            for col in range(4):
                for row in range(3, 0, -1):
                    if not board[row][col]:
                        for i in range(row, 0, -1):
                            board[i][col] = board[i-1][col]

                        board[0][col] = None
                        locations.append((0, col))
                        break

                    val = Board.can_merge(board[row][col],
                                          board[row-1][col])
                    if val:
                        board[row][col] = val

                        for i in range(row-1, 0, -1):
                            board[i][col] = board[i-1][col]

                        locations.append((0, col))
                        board[0][col] = None
                        break

        elif direction == Board.RIGHT:
            for row in range(4):
                for col in range(3, 0, -1):
                    if not board[row][col]:
                        for i in range(col, 0, -1):
                            board[row][i] = board[row][i-1]

                        board[row][0] = None
                        locations.append((row, 0))
                        break

                    val = Board.can_merge(board[row][col],
                                          board[row][col-1])
                    if val:
                        board[row][col] = val

                        for i in range(col-1, 0, -1):
                            board[row][i] = board[row][i-1]

                        board[row][0] = None
                        locations.append((row, 0))
                        break

        elif direction == Board.LEFT:
            for row in range(4):
                for col in range(3):
                    if not board[row][col]:
                        for i in range(col, 3):
                            board[row][i] = board[row][i+1]

                        board[row][3] = None
                        locations.append((row, 3))
                        break

                    val = Board.can_merge(board[row][col],
                                          board[row][col+1])
                    if val:
                        board[row][col] = val

                        for i in range(col+1, 3):
                            board[row][i] = board[row][i+1]

                        board[row][3] = None
                        locations.append((row, 3))
                        break

        # TODO handle locations, next_card

        return board

    def move(self, direction):
        board = self.preview_move(direction)
        if board:
            self.board = board
        return board
