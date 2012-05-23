import sys

from PySide.QtCore import *
from PySide.QtGui import *

from metachao import aspect
from metachao.aspect import Aspect


class qtapp(Aspect):
    """A qt application
    """
    @aspect.plumb
    def __init__(_next, self, argv=None, **kw):
        _next(**kw)
        if argv is None:
            argv = sys.argv
        self._app = QApplication(argv)

    def run(self):
        for x in self.values():
            x.qtinit()
            x.qt.show()
        self._app.exec_()
        sys.exit()


class qt(Aspect):
    """A qt node
    """
    _qt = None
    _qtcls = None

    @property
    def qt(self):
        if self._qt is None:
            self._qt = self._qtcls()
        return self._qt

    @aspect.plumb
    def __init__(_next, self, qtcls=None, **kw):
        _next(**kw)
        if qtcls is not None:
            self._qtcls = qtcls

    def qtinit(self):
        """Make sure qt widgets are instantiated
        """
        self._qtinit()
        for x in self.values():
            if hasattr(x, 'qtinit'):
                x.qtinit()

    def _qtinit(self):
        pass


class menubar(qt):
    @aspect.plumb
    def append(_next, self, node):
        _next(node)
        self.parent.qt.menuBar().addMenu(node.name)


class mainwindow(qt):
    """qt mainwindow
    """
    _menu = None
    _qtcls = QMainWindow

    # XXX: how can we reach the aspect super class' unbound methods?
    # mainwindow.super.qtinit() ?
    def _qtinit(self):
        label = QLabel("Hello World")
        self.qt.setCentralWidget(label)
