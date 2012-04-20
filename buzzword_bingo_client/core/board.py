""":mod:`buzzword_bingo_client.core.board` --- Internal representation of a Bingo board
"""

from __future__ import division
import math

FREE_SPACE_TEXT = 'FREE'

class Cell(object):
    """Single Bingo cell."""
    def __init__(self, word, covered=False):
        """Construct a cell with a word an optionally cover it.
        
        :param word: the buzzword
        :type word: :class:`str`
        """
        self.word = word
        self.covered = covered


class Board(object):
    """Matrix of cells."""
    def __init__(self, words):
        """Construct a board from a list of words. The board must always be
        square and the size is determined by the size of the list.
        
        :param rows: list of words
        :type rows: :class:`list` of :class:`str`

        .. todo::

            Error handling for the dimensions.
            
        """
        dimension = int(math.sqrt(len(words) + 1))
        middle = dimension // 2
        self.matrix = []
        for row in xrange(dimension):
            col_list = []
            for col in xrange(dimension):
                if row == middle and col == middle:
                    cell = Cell(FREE_SPACE_TEXT, True)
                else:
                    cell = Cell(words.pop())
                col_list.append(cell)
            self.matrix.append(col_list)

    def __len__(self):
        """Get the size of the board.

        :returns: the size
        :rtype: :class:`tuple` of 2 :class:`int`s
        """
        return len(self.matrix), len(self.matrix[0])

    def __getitem__(self, key):
        """Get a cell from the matrix.
        
        :param key: the 2D indices
        :type key: :class:`tuple` of 2 :class:`int`s
        :returns: the specified cell
        :rtype: :class:`Cell`
        
        .. todo::

            Error checking.
            
        """
        return self.matrix[key[0]][key[1]]

    def __iter__(self):
        """Return an iterator for the rows in this matrix.

        :returns: iterator for this matrix
        :rtype: :class:`listiterator`
        """
        return iter(self.matrix)

    def is_winning(self):
        """Determine whether the board is a winning board.
        
        :returns: win or loss
        :rtype: :class:`bool`
        """
        for row in self.matrix:
            for cell in row:
                if not cell.covered:
                    break
            else:
                return True
        for col in xrange(len(self.matrix[0])):
            for row in xrange(len(self.matrix)):
                if not self[row, col].covered:
                    break
            else:
                return True
        return False
