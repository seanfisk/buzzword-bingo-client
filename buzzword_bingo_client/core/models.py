""":mod:`buzzword_bingo_client.core.board` --- Internal representation of a Bingo board
"""

from __future__ import division
import math

FREE_SPACE_TEXT = 'FREE'

# class BoardItem(object):
#     """Representation of a board in the list of available boards."""
#     def __init__(self, name, url, word_urls, win_condition_urls):
#         """Construct the board item.
        
#         :param name: name of the board
#         :type name: :class:`str`
#         :param url: uniform resource locator for the board instance
#         :type url: :class:`str`
#         :param word_urls: list of URLs to words
#         :type word_urls: :class:`list` of :class:`str`
#         :param win_condition_urls: list of URLs to win conditions
#         :type win_condition_urls: :class:`list` of :class:`str`
#         """
#         self.name = name
#         self.url = url
#         self.words = None
#         self.word_urls = word_urls
#         self.win_condition_urls = None
#         self.win_condition_urls = win_condition_urls

#     def load(self):
#         """Load the board words and win conditions with the supplied URLs."""
#         self.words = []
#         for url in self.word_urls:
#             self.words.append(self.api.load_word(url))

#         self.win_conditions = []
#         for url in self.win_condition_urls:
#             self.win_conditions.append(self.api.load_win_condition(url))

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
        return ('Word list length must be one less than the square of an odd '
        'number and be greater than or equal to 9 (3x3 board). Odd edge size is '
        'to accomodate the free space. The length given was: ')
    

class ActiveCell(object):
    """Single Bingo cell in the active board."""
    def __init__(self, word, covered=False):
        """Construct a cell with a word an optionally cover it.
        
        :param word: the buzzword
        :type word: :class:`str`
        """
        self.word = word
        self.covered = covered


class ActiveBoard(object):
    """Matrix of cells in the active board."""

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
                    cell = ActiveCell(FREE_SPACE_TEXT, True)
                else:
                    cell = ActiveCell(words.pop())
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
