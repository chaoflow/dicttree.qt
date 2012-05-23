from dicttree.ordereddict import Node as _Node

from dicttree.qt import aspects

QtApp = aspects.qtapp(_Node)
Node = aspects.qt(_Node)

MainWindow = aspects.mainwindow(_Node)
MenuBar = aspects.menubar(_Node)
