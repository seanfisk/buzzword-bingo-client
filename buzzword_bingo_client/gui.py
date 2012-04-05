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
import metadata

SIZE = 5

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

        self.setCentralWidget(QtGui.QWidget(self))

        # set the background and frame color for the labels
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.yellow)
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Light, QtCore.Qt.blue)
        palette.setColor(QtGui.QPalette.Dark, QtCore.Qt.blue)

        self.layout = QtGui.QGridLayout(self.centralWidget())
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QtCore.QMargins())

        middle = SIZE // 2
        for row in xrange(SIZE):
            for col in xrange(SIZE):
                if row == middle and col == middle:
                    text = 'FREE SPACE'
                else:
                    text = 'Cloud Computing'
                label = QtGui.QLabel(text, self.centralWidget())
                # the following line is nesscary to paint the background of the
                # widget
                label.setAutoFillBackground(True)
                label.setPalette(palette)
                label.setFrameShape(QtGui.QFrame.Box)
                label.setFrameShadow(QtGui.QFrame.Raised)
                label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

                self.layout.addWidget(label, row, col)
        

    @QtCore.Slot()
    def about(self):
        """Create and show the about dialog."""
        AboutDialog(self).exec_()

