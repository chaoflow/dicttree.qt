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
            x._widget.show()
        self._app.exec_()
        sys.exit()

class qt(Aspect):
    """A qt widget
    """
    # XXX: consider renaming to qt and qtcls
    _widget = None
    _widgetcls = None

    @property
    def widget(self):
        if self._widget is None:
            self._widget = self._widgetcls()
        return self._widget

    @aspect.plumb
    def __init__(_next, self, widgetcls=None, **kw):
        _next(**kw)
        if widgetcls is not None:
            self._widgetcls = widgetcls

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
        self.parent.widget.menuBar().addMenu(node.name)


class mainwindow(qt):
    """qt mainwindow
    """
    _menu = None
    _widgetcls = QMainWindow

    # XXX: how can we reach the aspect super class' unbound methods?
    # mainwindow.super.qtinit() ?
    def _qtinit(self):
        label = QLabel("Hello World")
        self.widget.setCentralWidget(label)
