from dicttree.ordereddict import Node as _Node

from dicttree.qt import aspects

QtApp = aspects.qtapp(_Node)
Node = aspects.qt(_Node)

Label = aspects.label(_Node)
MainWindow = aspects.mainwindow(_Node)
MenuBar = aspects.menubar(_Node)

Table = aspects.table(_Node)
Tabbed = aspects.tabbed(_Node)
Widget = aspects.widget(_Node)
