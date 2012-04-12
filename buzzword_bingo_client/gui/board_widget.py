""":mod:`buzzword_bingo_client.gui.board` --- Graphical board widget
"""

from PySide import QtCore, QtGui
#from buzzword_bingo_client.core.board import Board

SIZE = 5
COLOR_UNCOVERED = QtGui.QColor(244, 244, 244)
COLOR_COVERED = QtCore.Qt.lightGray

# set the background and frame color for the labels
LABEL_PALETTE = QtGui.QPalette()
LABEL_PALETTE.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
LABEL_PALETTE.setColor(QtGui.QPalette.Light, QtCore.Qt.black)
LABEL_PALETTE.setColor(QtGui.QPalette.Dark, QtCore.Qt.black)

class BoardLabel(QtGui.QLabel):
    """A square for the bingo board."""
    
    clicked = QtCore.Signal(int, int)
    
    def __init__(self, row, col, text, covered=False, parent=None, f=0):
        """Construct a board label.

        :param row: cell's row
        :type row: :class:`int`
        :param col: cell's column
        :type col: :class:`int`
        :param text: string to show
        :type text: :class:`str`
        :param covered: whether this cell is covered
        :type covered: :class:`bool`
        :param parent: parent in the Qt hierarchy
        :type parent: :class:`QtGui.QWidget`
        :param f: window flags
        :type f: :class:`QtCore.Qt.WindowFlags`
        """
        super(BoardLabel, self).__init__(text, parent, f)
        # the following line is nesscary to paint the background of the
        # widget
        self.setAutoFillBackground(True)
        self.setPalette(LABEL_PALETTE)
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Raised)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.row = row
        self.col = col
        self.set_covered(covered)

    def set_covered(self, covered):
        """Cover or uncover the cell.
        
        :param covered: whether the cell is covered
        :type covered: :class:`bool`
        """
        palette = self.palette()
        color = COLOR_COVERED if covered else COLOR_UNCOVERED
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)

    def mousePressEvent(self, event):
        """Handle mouse press events.

        :param event: the mouse press event
        :type event: :class:`QtGui.QMouseEvent`
        """
        self.set_covered(True)
        self.clicked.emit(self.row, self.col)


class BoardWidget(QtGui.QWidget):
    """Widget which shows the board."""
    def __init__(self, parent=None):
        """Construct a visual representation of the board.
        
        :param parent: parent in Qt hierarchy
        :type parent: :class:`QtGui.QWidget`
        """
        super(BoardWidget, self).__init__(parent)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QtCore.QMargins())

    def set_board(self, board):
        """Display a board on the screen.
        
        :param board: board to show
        :type board: :class:`Board`
        """
        self.board = board
        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                label = BoardLabel(r, c, cell.word, cell.covered, self)
                label.clicked.connect(self.label_clicked)
                self.layout.addWidget(label, r, c)

    @QtCore.Slot(int, int)
    def label_clicked(self, row, col):
        self.board[row, col].covered = True
        if self.board.is_winning():
            print 'You won!'

                
