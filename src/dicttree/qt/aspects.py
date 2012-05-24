import sys

from PySide.QtCore import *
from PySide.QtGui import *

from metachao import aspect
from metachao.aspect import Aspect

from dicttree.qt.log import getLogger
log = getLogger('aspects')


class qt(Aspect):
    """A qt node
    """
    # qt instance object
    _qt = None

    # qt class to create instance object
    _qtcls = None

    # args and kw to be passed to qtcls
    _qtargs = None    # tuple
    _qtkw = None      # dict

    @property
    def qt(self):
        if self._qt is None:
            # make sure parent is created first
            if self.parent:
                self.parent.qt
            self._qtinit()
        return self._qt

    @property
    def qtargs(self):
        if self._qtargs is None:
            return ()
        return self._qtargs

    @property
    def qtkw(self):
        if self._qtkw is None:
            return {}
        return self._qtkw

    @aspect.plumb
    def __init__(_next, self, qtcls=None, **kw):
        _next(**kw)
        if qtcls is not None:
            self._qtcls = qtcls

    def qtinit(self):
        """Make sure qt widgets are instantiated
        """
        log.debug('qtinit begin: %s' % self.name)
        self._qtinit()
        for x in self.values():
            if hasattr(x, 'qtinit'):
                x.qtinit()
        log.debug('qtinit end: %s ' % self.name)

    def _qtinit(self):
        if self._qt is None and self._qtcls:
            args = self.qtargs
            kw = self.qtkw
            log.debug('_qtinit: %s with %r %r' % (self.name, args, kw))
            self._qt = self._qtcls(*args, **kw)


class qtapp(qt):
    """A qt application
    """
    _qtcls = QApplication

    @aspect.plumb
    def __init__(_next, self, argv=None, **kw):
        _next(**kw)
        if argv is not None:
            self._qtargs = (argv,)
        if self._qtargs is None:
            self._qtargs = (sys.argv,)

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
        if self._qt is None:
            self._qt = self._qtcls()
            label = QLabel("Hello World")
            self._qt.setCentralWidget(label)


class label(qt):
    _qtcls = QLabel

    @property
    def qtargs(self):
        return (getattr(self.attrs, 'title', ''),)


class menubar(qt):
    @property
    def qt(self):
        return self.parent.qt.menuBar()

    @aspect.plumb
    def append(_next, self, node):
        _next(node)
        self.qt.addMenu(node.name)
