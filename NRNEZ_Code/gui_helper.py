###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This contains all the functions used to create GUI elements.
#### Author: Evan Cobb
####
###################################################################
 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import globvar as gv
from errorLogger import *

####returns a button gui element
def newButton(layout, text, row = None, col = None, rowSpan = None, colSpan = None):
    logDebug("gui_helper.py::newButton() called. --Text: " + text + "\n")
    b = QPushButton()
    b.setText(text)
    if(rowSpan is not None):
        layout.addWidget(b, row, col, rowSpan, colSpan)
    elif(row is not None):
        layout.addWidget(b, row, col)
    else:
        layout.addWidget(b)
    return b

####returns a label gui element
def newLabel(layout, text, row = None, col = None, rowSpan = None, colSpan = None):
    logDebug("gui_helper.py::newLabel() called. --Text: " + text + "\n")
    l = QLabel(text)
    #l.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    if(rowSpan is not None):
        layout.addWidget(l, row, col, rowSpan, colSpan)
    elif(row is not None):
        layout.addWidget(l, row, col)
    else:
        layout.addWidget(l)
    return l

####returns a line edit gui element
def newLineEdit(layout, name, validator=None, row = None, col = None, rowSpan = None, colSpan = None):
    logDebug("gui_helper.py::newLineEdit() called. --Name: " + name + "\n")
    e = QLineEdit()
    ##e.setFixedWidth(width)
    e.setObjectName(name)
    e.setValidator(validator)
    e.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    if(rowSpan is not None):
        layout.addWidget(e, row, col, rowSpan, colSpan)
    elif(row is not None):
        layout.addWidget(e, row, col)
    else:
        layout.addWidget(e)
    return e

####returns a checkbox gui element
def newCheckBox(layout, text, checked, name):
    logDebug("gui_helper.py::newCheckBox() called. --Name: " + name + "\n")
    b = QCheckBox(text)
    b.setChecked(checked)
    b.setObjectName(name)
    layout.addWidget(b)
    return b

####returns a radio button gui element
def newRadioButton(layout, text, checked, name, row = None, col = None, rowSpan = None, colSpan = None):
    logDebug("gui_helper.py::newRadioButton() called. --Name: " + name + "\n")
    b = QRadioButton(text)
    b.setChecked(checked)
    b.setObjectName(name)
    if(rowSpan is not None):
        layout.addWidget(b, row, col, rowSpan, colSpan)
    elif(row is not None):
        layout.addWidget(b, row, col)
    else:
        layout.addWidget(b)
    return b

####returns a radio button group gui element 
def newButtonGroup(parent, buttons, name):
    logDebug("gui_helper.py::newButtonGroup() called. --Name: " + name + "\n")
    group = QButtonGroup(parent)
    group.setObjectName(name)
    for b in buttons:
        group.addButton(b)
    return group

####returns a table view gui element
def newTableView(layout, name):
    logDebug("gui_helper.py::newTableView() called. --Name: " + name + "\n")
    table = QTableView()
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    table.setObjectName(name)
    layout.addWidget(table)
    return table

####returns a validator with double precision for line edit gui elements
def newDVal(decimal, minx=None, maxx=None):
    logDebug("gui_helper.py::newDVal() called. --Number Validator: " + str(decimal) + "\n")
    validator = QDoubleValidator()
    if minx != None:
        validator.setBottom(minx)
    validator.setDecimals(decimal)
    if maxx != None:
        validator.setTop(maxx)
    return validator

####returns a combo box gui element
def newComboBox(layout, items, name, row = None, col = None, rowSpan = None, colSpan = None):
    logDebug("gui_helper.py::newComboBox() called. --Name: " + name + "\n")
    cb = QComboBox()
    cb.addItems(items)
    cb.setObjectName(name)
    if(rowSpan is not None):
        layout.addWidget(cb, row, col, rowSpan, colSpan)
    elif(row is not None):
        layout.addWidget(cb, row, col)
    else:
        layout.addWidget(cb)
    return cb

####sets color from the color picker
def colorPicker():
    logDebug("gui_helper.py::colorPicker() called.\n")
    gv.color = QColorDialog.getColor()
    

