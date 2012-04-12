""":mod:`buzzword_bingo_client.gui` --- Client graphics

Displays the bingo board.

.. todo::

   Add borders to the labels.

.. todo::

   Make the labels clickable and have an X appear when clicked.
   
.. todo::

   Connect the labels' click events to API calls.
   
.. todo::

   Use the actual API, which has yet to be completed.
   
.. todo::

   Add message boxes to win the game.
   
.. todo::
   
   Allow users to compose words and boards and submit them.

"""

from PySide import QtCore, QtGui
from about import AboutDialog
from board_widget import BoardWidget
from buzzword_bingo_client import metadata
from buzzword_bingo_client.core.board import Board
from buzzword_bingo_client.core.api import API

SIZE = 5
COLOR_UNCOVERED = QtGui.QColor(244, 244, 244)
COLOR_COVERED = QtCore.Qt.lightGray

# set the background and frame color for the labels
LABEL_PALETTE = QtGui.QPalette()
LABEL_PALETTE.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
LABEL_PALETTE.setColor(QtGui.QPalette.Window,
                 COLOR_UNCOVERED)
LABEL_PALETTE.setColor(QtGui.QPalette.Light, QtCore.Qt.black)
LABEL_PALETTE.setColor(QtGui.QPalette.Dark, QtCore.Qt.black)

class BoardLabel(QtGui.QLabel):
    """A square for the bingo board."""
    
    clicked = QtCore.Signal(int, int)
    
    def __init__(self, row, col, text, parent=None, f=0):
        """Construct a board label.
        
        :param text: string to show
        :type text: :class:`str`
        :param coords: coordinates of this label
        :type coords: :class:`tuple` of :class:`int`
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

    def mousePressEvent(self, event):
        """Handle mouse press events.

        clicked.emt
        
        :param event: the mouse press event
        :type event: :class:`QtGui.QMouseEvent`
        """
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, COLOR_COVERED)
        self.setPalette(palette)
        self.clicked.emit(self.row, self.col)


class MainWindow(QtGui.QMainWindow):
    """Main application window."""
    def __init__(self, parent=None):
        """Construct the window."""
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(metadata.nice_title)
        
        self.menu_bar = QtGui.QMenuBar()
        self.game_menu = self.menu_bar.addMenu('&Game')
        self.quit_action = self.game_menu.addAction('&Quit')
        self.quit_action.triggered.connect(self.close)
        self.help_menu = self.menu_bar.addMenu('&Help')
        self.about_action = self.help_menu.addAction('&About')
        self.about_action.triggered.connect(self.about)
        self.setMenuBar(self.menu_bar)

        self.api = API('http://localhost:8000/')

        words = [word['word'] for word in self.api.all_boards()[0]['words']]
        print words
        
        self.board_widget = BoardWidget(self)
        self.setCentralWidget(self.board_widget)
        self.board = Board(words)
        self.board_widget.set_board(self.board)

        # self.setCentralWidget(QtGui.QWidget(self))

        # self.layout = QtGui.QGridLayout(self.centralWidget())
        # self.layout.setSpacing(0)
        # self.layout.setContentsMargins(QtCore.QMargins())

        # middle = SIZE // 2
        # for row in xrange(SIZE):
        #     for col in xrange(SIZE):
        #         if row == middle and col == middle:
        #             text = 'FREE SPACE'
        #         else:
        #             text = 'Cloud Computing'
        #         label = BoardLabel(row, col, text, self.centralWidget())
        #         label.clicked.connect(self.label_clicked)
        #         self.layout.addWidget(label, row, col)
        
    @QtCore.Slot()
    def about(self):
        """Create and show the about dialog."""
        AboutDialog(self).exec_()
