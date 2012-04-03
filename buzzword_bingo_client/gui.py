""":mod:`buzzword_bingo_client.gui` --- Client graphics

Displays the bingo board.
"""

from PySide import QtCore, QtGui
from about import AboutDialog

class MainWindow(QtGui.QMainWindow):
    """Main application window."""
    def __init__(self, parent=None):
        """Construct the window."""
        super(MainWindow, self).__init__(parent)
        
        self.menu_bar = QtGui.QMenuBar()
        self.game_menu = self.menu_bar.addMenu('&Game')
        self.quit_action = self.game_menu.addAction('&Quit')
        self.quit_action.triggered.connect(self.close)
        self.help_menu = self.menu_bar.addMenu('&Help')
        self.about_action = self.help_menu.addAction('&About')
        self.about_action.triggered.connect(self.about)
        self.setMenuBar(self.menu_bar)

    @QtCore.Slot()
    def about(self):
        """Create and show the about dialog."""
        AboutDialog(self).exec_()

