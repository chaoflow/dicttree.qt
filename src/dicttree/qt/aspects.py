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
# XXX: does not work yet
#    _schema = aspect.cfg(aspect.default(None))
    _schema2 = aspect.cfg(None)
    _silence = False
    _signals = dict(
        itemChanged="itemChanged",
        )
    _transpose = aspect.cfg(False)

    @property
    def schema(self):
        # XXX: not needed once aspect.cfg handles default/overwrite/...
        try:
            return self._schema
        except AttributeError:
            return self._schema2

    @property
    def qtargs(self):
        if self._transpose:
            args = [len(self.schema), 0]
        else:
            args = [0, len(self.schema)]
        return args

    @aspect.plumb
    def __init__(_next, self, **kw):
        # call __init__ of parent aspect - is this good?
        qt.__init__.payload(_next, self, **kw)
        if self._transpose:
            setHeaders = self.qt.setVerticalHeaderLabels
        else:
            setHeaders = self.qt.setHorizontalHeaderLabels
        setHeaders([x.name for x in self.schema])

    @aspect.plumb
    def append(_next, self, node):
        # XXX: move to __setitem__ and support replacing
        idx = len(self.keys())
        _next(node)
        if self._transpose:
            self.qt.setColumnCount(idx+1)
        else:
            self.qt.setRowCount(idx+1)
        for attr_idx, val in enumerate(node.attrs.values()):
            flags = Qt.ItemIsEnabled
            readonly = self.schema[attr_idx].readonly
            if type(val) is bool:
                # bool's are shown as checkboxes for now - could be
                # configured via schema
                item = QTableWidgetItem()
                if not readonly:
                    flags |= Qt.ItemIsUserCheckable
                item.setCheckState(Qt.Checked if val else Qt.Unchecked)
            else:
                if not readonly:
                    flags |= Qt.ItemIsEditable
                item = QTableWidgetItem(str(val))
            item.setFlags(flags)
            self._silence = True
            if self._transpose:
                self.qt.setItem(attr_idx, idx, item)
            else:
                self.qt.setItem(idx, attr_idx, item)
            self._silence = False

    def itemChanged(self, item):
        if self._silence:
            return
        if self._transpose:
            attr_idx = item.row()
            idx = item.column()
        else:
            idx = item.row()
            attr_idx = item.column()
        field = self.schema[attr_idx]
        if Qt.ItemIsUserCheckable & item.flags():
            value = item.checkState()
        else:
            value = item.text()
        self[idx].attrs[field.name] = field.type(value)


class tabbed(qt):
    _qtcls = QTabWidget

    @aspect.plumb
    def __setitem__(_next, self, key, val):
        _next(key, val)
        # XXX: support replacing
        self.qt.addTab(val.qt, key)


class pushbutton(qt):
    _qtcls = QPushButton

    @property
    def qtargs(self):
        return (self.name,)
