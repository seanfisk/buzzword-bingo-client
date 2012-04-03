""":mod:`buzzword_bingo_client.gui` --- Client graphics

Displays the bingo board.
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

        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QtGui.QGridLayout(self.central_widget)

        middle = SIZE // 2
        for row in xrange(SIZE):
            for col in xrange(SIZE):
                if row == middle and col == middle:
                    text = 'FREE SPACE'
                else:
                    text = 'Cloud Computing'
                self.layout.addWidget(QtGui.QLabel(text, self.central_widget), row, col, QtCore.Qt.AlignHCenter)
        

    @QtCore.Slot()
    def about(self):
        """Create and show the about dialog."""
        AboutDialog(self).exec_()

