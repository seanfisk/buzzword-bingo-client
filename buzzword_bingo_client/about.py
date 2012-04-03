""":mod:`buzzword_bingo_client.about` --- Display the about dialog
"""

from PySide import QtCore, QtGui
import metadata

class AboutDialog(QtGui.QDialog):
    """Shows information about the program."""
    def __init__(self, parent=None):
        """Construct the dialog."""
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle('About ' + metadata.nice_title)
        self.layout = QtGui.QVBoxLayout(self)
        self.title_label = QtGui.QLabel(metadata.nice_title, self)
        self.layout.addWidget(self.title_label)
        self.version_label = QtGui.QLabel('Version ' + metadata.version, self)
        self.layout.addWidget(self.version_label)
        self.copyright_label = QtGui.QLabel('Copyright (C) ' +
                                            metadata.copyright, self)
        self.layout.addWidget(self.copyright_label)
        self.url_label = QtGui.QLabel(
            '<a href="{0}">{0}</a>'.format(metadata.url), self)
        self.url_label.setOpenExternalLinks(True)
        self.layout.addWidget(self.url_label)
        for i in xrange(self.layout.count()):
            self.layout.itemAt(i).setAlignment(QtCore.Qt.AlignHCenter)

