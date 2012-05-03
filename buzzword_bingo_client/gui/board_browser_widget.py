""":mod:`buzzword_bingo_client.gui.board_browser_widget --- Browse boards
"""

from PySide import QtCore, QtGui

class BoardBrowserWidget(QtGui.QWidget):
    """Widget which allows browsing of all available boards."""
    def __init__(self, api, parent=None, flags=0):
        """Create the widget.

        :param api: api instance
        :type api: :class:`buzzword_bingo_client.core.api.API`
        """
        super(BoardBrowserWidget, self).__init__(parent, flags)
        
        # data
        self.api = api
        self.model = QtGui.QStringListModel()
        boards = self.api.all_boards()
        self.model.setStringList([board['name'] for board in boards])

        # graphics
        self.view = QtGui.QListView()
        self.view.setModel(self.model)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.view)
