import sys

from PySide.QtCore import *
from PySide.QtGui import *

from metachao import aspect
from metachao.aspect import Aspect


class qt(Aspect):
    """A qt node
    """
    _qt = None
    _qtcls = None

    @property
    def qt(self):
        if self._qt is None:
            # make sure parent is created first
            if self.parent:
                self.parent.qt
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


class qtapp(qt):
    """A qt application
    """
    _argv = None
    _qtcls = QApplication

    @property
    def qt(self):
        if self._qt is None:
            self._qt = self._qtcls(self._argv)
        return self._qt

    @aspect.plumb
    def __init__(_next, self, argv=None, **kw):
        _next(**kw)
        if argv is not None:
            self._argv = argv
        if self._argv is None:
            self._argv = sys.argv

    def run(self):
        self.qtinit()
        for x in self.values():
            x.qt.show()
        self.qt.exec_()
        sys.exit()


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


class menubar(qt):
    @property
    def qt(self):
        return self.parent.qt.menuBar()

    @aspect.plumb
    def append(_next, self, node):
        _next(node)
        self.qt.addMenu(node.name)
