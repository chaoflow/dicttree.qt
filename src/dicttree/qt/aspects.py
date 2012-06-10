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
    _qtcls = aspect.cfg(None)

    # args and kw to be passed to qtcls
    _qtargs = None    # tuple
    _qtkw = None      # dict

    _layout = None
    _layoutcls = aspect.cfg(layout=None)

    _signals = aspect.cfg(dict())

    @property
    def layout(self):
        return self._layout

    @property
    def qt(self):
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
    def __init__(_next, self, **kw):
        log.debug('init %s start: %s' % (self, kw))
        _next(**kw)
        self._qt = self._qtcls(*self.qtargs, **self.qtkw)
        if self._layout is None and self._layoutcls is not None:
            self._layout = self._layoutcls()
            self._qt.setLayout(self._layout)
        for signal, slot in self._signals.items():
            if not callable(slot):
                slot = getattr(self, slot)
            # XXX: lambda is needed because of what seems to be a
            # PySide bug
            slot_lambda = lambda *_args, **_kw: slot(*_args, **_kw)
            getattr(self.qt, signal).connect(slot_lambda)

    @aspect.plumb
    def __setitem__(_next, self, key, val):
        _next(key, val)
        if self.layout:
            self.layout.addWidget(val.qt)


class qtapp(qt):
    """A qt application
    """
    _argv = aspect.cfg(sys.argv)
    _qtcls = QApplication

    @property
    def qtargs(self):
        return (self._argv,)

    def run(self):
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
    _silence = False
    _signals = dict(
        itemChanged="itemChanged",
        )

    @property
    def qtargs(self):
        args = [
            self.attrs.get('rows', 0),
            len(self._columns),
            ]
        return args

    @aspect.plumb
    def append(_next, self, row):
        # XXX: move to __setitem__ and support replacing
        row_idx = len(self.keys())
        _next(row)
        self.qt.setRowCount(row_idx+1)
        for col_idx, x in enumerate(row.attrs.values()):
            # bool's are shown as checkboxes for now and are editable
            # everything else is readonly
            if type(x) is bool:
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked if x else Qt.Unchecked)
            else:
                item = QTableWidgetItem(str(x))
                item.setFlags(Qt.ItemIsEnabled)
            self._silence = True
            self.qt.setItem(row_idx, col_idx, item)
            self._silence = False

    def itemChanged(self, item):
        if self._silence:
            return
        row = item.row()
        col = item.column()
        name = self._columns[col].name
        if Qt.ItemIsUserCheckable & item.flags():
            value = item.checkState()
        else:
            value = item.text()
        self[row].attrs[name] = value


class tabbed(qt):
    _qtcls = QTabWidget

    @aspect.plumb
    def __setitem__(_next, self, key, val):
        _next(key, val)
        # XXX: support replacing
        self.qt.addTab(val.qt, key)
