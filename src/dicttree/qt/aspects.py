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

    _layout = None

    @property
    def layout(self):
        return self._layout

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
    def __init__(_next, self, qtcls=None, layout=None, **kw):
        _next(**kw)
        if qtcls is not None:
            self._qtcls = qtcls
        if layout is not None:
            self._layout = layout()

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
        log.debug('_qtinit: start: %s' % self.name)
        if self._qt is None and self._qtcls:
            args = self.qtargs
            kw = self.qtkw
            if self.parent and not self.parent.layout and \
                    isinstance(self.parent.qt, QWidget):
                kw['parent'] = self.parent.qt
            log.debug('_qtcls for %s with %r %r' % (self.name, args, kw))
            self._qt = self._qtcls(*args, **kw)
            if self.parent and self.parent.layout:
                log.debug('adding to parent layout')
                self.parent.layout.addWidget(self._qt)
            if self._layout:
                log.debug('setting layout')
                self._qt.setLayout(self._layout)
        log.debug('_qtinit: end: %s' % self.name)


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


class widget(qt):
    _qtcls = QWidget


class mainwindow(qt):
    """qt mainwindow
    """
    _menu = None
    _qtcls = QMainWindow

    @aspect.plumb
    def __setitem__(_next, self, key, node):
        _next(key, node)
        if key == "central":
            self.qt.setCentralWidget(node.qt)


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


class table(qt):
    _qtcls = QTableWidget

    @property
    def qtargs(self):
        args = [
            self.attrs.get('rows', 0),
            self.attrs.get('cols', 0),
            ]
        return args

    @aspect.plumb
    def append(_next, self, row):
        row_idx = len(self.keys())
        _next(row)
        self.qt.setRowCount(row_idx+1)
        for col_idx, x in enumerate(row.attrs.values()):
            item = QTableWidgetItem(str(x))
            self.qt.setItem(row_idx, col_idx, item)

