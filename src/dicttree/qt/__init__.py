from dicttree.ordereddict import Node

from dicttree.qt import aspects

QtApp = aspects.qtapp(Node)
Node = aspects.qt(Node)

MainWindow = aspects.mainwindow(Node)
MenuBar = aspects.menubar(Node)
