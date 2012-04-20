""":mod:`buzzword_bingo_client.core.board` --- Internal representation of a Bingo board
"""

from __future__ import division
import math
from textwrap import dedent

FREE_SPACE_TEXT = 'FREE'

class DimensionsError(Exception):
    """Error that is raised when a list of words of an invalid length is
    given. Valid lengths are one less than the squares of odd numbers greater
    than or equal to 9 (3x3 board). They must be odd to accomodate the free
    space."""
    def __init__(self, length):
        """Create the error.
        
        :param length: length of the word list
        :type length: :class:`int`
        """
        self.length = length

    def __str__(self):
        """Stringify the error.

        :return: the string representation
        :rtype: :class:`str`
        """
        return dedent('''
        Word list length must be one less than the square of an odd number and 
        be greater than or equal to 9 (3x3 board). Odd edge size is to 
        accomodate the free space. The length given was: ''' +
        str(self.length)).replace('\n', '')
        

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

    MINIMUM_BOARD_DIMENSION = 3
    """Minimum dimension of the square board."""
    
    def __init__(self, words):
        """Construct a board from a list of words. The board must always be
        square and the size is determined by the size of the list.
        
        :param rows: list of words
        :type rows: :class:`list` of :class:`str`
        :raises: :class:`DimensionsError`
        """
        # check dimensions
        length = len(words)
        if length < self.MINIMUM_BOARD_DIMENSION ** 2 - 1:
            raise DimensionsError(length)
        dimension_float = math.sqrt(length + 1)
        dimension = int(dimension_float)
        if dimension_float != dimension or dimension % 2 != 1:
            raise DimensionsError(length)
        
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
