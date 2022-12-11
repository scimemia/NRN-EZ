###################################################################
####
#### Version: 1.1.6
#### Date: 11/30/2022
#### Description: This file contains handler functions for all UI elements
#### Author: Evan Cobb
####
###################################################################
 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import globvar as gv
from errorLogger import *
from copy import deepcopy
from datetime import datetime
from shutil import copy2, rmtree
import os
from experimentClass import *
from timeClass import *
from weightClass import *
from locationClass import *
from loader import loadNRNEZ
import subprocess

##handles mouse clicks on the graph for segment selection.
##when 2 points are clicked, a line is calculated. This line is compared to the line
##drawn of every segment. If they intersect, the segment is highlighted.
def segSelect(evt):
    logDebug("gui_handler.py::segSelect() called.\n")
    ##already been a point selected, second click to determine seg
    if(gv.lastPoint is not None):
        sid = getIntersect(gv.lastPoint, gv.plotObj.vb.mapSceneToView(evt.scenePos()))
        sel = None
        inputs = None
        seg = None
        x = 1
        ##calculate the segment number
        if sid is not None:
            for part in gv.morphObj.morphParts:
                if sid == part.id:
                    sel = part
                    break
            if sel is not None:
                if sel.type == 1:
                    inputs = gv.morphObj.somaInputs[1:]
                elif sel.type == 2:
                    inputs = gv.morphObj.axonInputs
                elif sel.type == 3:
                    inputs = gv.morphObj.basalInputs
                else:
                    inputs = gv.morphObj.apicalInputs

                for i in inputs:
                    if sel.id == i.id:
                        seg = [x, sel.type]
                        break
                    x = x + 1
        ##highlight the segment
        if seg is not None:
            picker = gv.graphWin.parent().findChild(QComboBox, "Highlight Picker")
            picker.setCurrentIndex(seg[1]-1)
            le = gv.graphWin.parent().findChild(QLineEdit, "highlight")
            le.setText(str(seg[0]))
        gv.lastPoint = None
    ###set first click point
    else:
        gv.lastPoint = gv.plotObj.vb.mapSceneToView(evt.scenePos())

##determines if a segment intersects the two given points
def getIntersect(p1, p2):
    logDebug("gui_handler.py::getIntersect() called.\n")
    for l in gv.lines:
        a1 = p2.y() -p1.y()
        b1 = p1.x() - p2.x()
        c1 = (p1.x() * a1) + (p1.y() * b1)

        a2 = l[3] - l[1]
        b2 = l[0] - l[2]
        c2 = (l[0] * a2) + (l[1] * b2)

        det = (a1 * b2) - (a2 * b1)

        ##lines are parallel, then continue
        if(det == 0):
            continue
        else:
            x = round(((b2 * c1) - (b1 * c2))/det, 6)
            y = round(((a1 * c2) - (a2 * c1))/det, 6)

            x1 = round(p1.x(), 6)
            x2 = round(p2.x(), 6)
            y1 = round(p1.y() , 6)
            y2 = round(p2.y(), 6)

            #### check if the intersect point falls on the x of both lines
            if(((x1 <= x and x <= x2) or (x2 <= x and x <= x1)) and ((l[0] <= x and x <= l[2]) or (l[2] <= x and x <= l[0]))):
                ##check if the intersect point falls on the y of both lines
                if(((y1 <= y and y <= y2) or (y2 <= y and y <= y1)) and ((l[1] <= y and y <= l[3]) or (l[3] <= y and y <= l[1]))):
                    return l[4]
    return None
            
##handles the morphology file selection button
def fileSelect(q, tb, fileType):
    fname = QFileDialog.getOpenFileName(q, 'Open File', '~/', fileType)[0]
    if fname != "":
        tb.setText(fname)
    logDebug("gui_handler.py::fileSelect() called. --File Name: " + fname + "\n")

##handles the output directory selection button
def fileSelectOutput(q, tb):
    dirname = QFileDialog.getExistingDirectory(q, 'Select Directory', '~/',QFileDialog.ShowDirsOnly)
    if dirname != "":
        tb.setText(dirname)
    logDebug("gui_handler.py::fileSelectOutput() called. --Directory Name: " + dirname +"\n")

##handles range button selection/toggling
def rangeButton(btn, window):
    logDebug("gui_handler.py::rangeButton() called.\n")
    if btn.text() == 'All':
        if btn.isChecked() == True:
            window.hide()
    else:
        if btn.isChecked() == True:
            window.show()

##handles radio button selection/toggling
def radioButton(btn, w1, w2, w3, parent):
    logDebug("gui_handler.py::radioButton() called.\n")
    if btn.isChecked():
        if btn.text() == 'Single':
            w2.hide()
            w3.hide()
            w1.show()
        elif btn.text() == 'Multiple Uniform':
            w1.hide()
            w3.hide()
            w2.show()
        else:
            w1.hide()
            w2.hide()
            w3.show()
        btn.setFocusPolicy(QtCore.Qt.ClickFocus)
        setTabOrder(parent)

def radioButton2(btn, w1, w2, w3, w4, w5, w6, parent):
    logDebug("gui_handler.py::radioButton() called.\n")
    if btn.isChecked():
        if btn.text() == 'Single':
            w2.hide()
            w3.hide()
            w5.hide()
            w6.hide()
            w1.show()
            w4.show()
        elif btn.text() == 'Multiple Uniform':
            w1.hide()
            w3.hide()
            w4.hide()
            w6.hide()
            w2.show()
            w5.show()
        else:
            w1.hide()
            w2.hide()
            w4.hide()
            w5.hide()
            w3.show()
            w6.show()
            
            
        btn.setFocusPolicy(QtCore.Qt.ClickFocus)
        setTabOrder(parent)


        
##handles radio buttons for input selection
def inputRadioButton(button, hBox, sBox, w):
    logDebug("gui_handler.py::inputRadioButton() called.\n")
    if button.isChecked():
        hBox.hide()
        sBox.show()
    button.setFocusPolicy(QtCore.Qt.ClickFocus)
    setTabOrder(w)

##handles weight picker
def weightSelect(picker, boxes, w):
    logDebug("gui_handler.py::weightSelect() called.\n")
    for b in boxes:
        b.hide()
    boxes[picker.currentIndex()].show()
    setTabOrder(w)
    
##sets the tabbing order
def setTabOrder(w):
    logDebug("gui_handler.py::setTabOrder() called.\n")
    ######synaptic input tab order
    if(w.findChild(QComboBox, "Weight Picker").currentIndex() == 1):
        w.setTabOrder(w.findChild(QLineEdit, "highlight"), w.findChild(QLineEdit,"Weight Name"))
        if(w.findChild(QRadioButton, "ampSingle").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "Weight Name"), w.findChild(QLineEdit, "Single Weight"))
            w.setTabOrder(w.findChild(QLineEdit, "Single Weight"), w.findChild(QLineEdit,"E"))
        elif(w.findChild(QRadioButton, "ampMult").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "Weight Name"), w.findChild(QLineEdit, "amp Uni Mean"))
            w.setTabOrder(w.findChild(QLineEdit, "amp Uni Mean"), w.findChild(QLineEdit,"amp Uni SD"))
            w.setTabOrder(w.findChild(QLineEdit, "amp Uni SD"), w.findChild(QLineEdit,"E"))
        else:
            w.setTabOrder(w.findChild(QLineEdit, "Weight Name"), w.findChild(QLineEdit,"ampMean"))
            w.setTabOrder(w.findChild(QLineEdit, "ampMean"), w.findChild(QLineEdit,"ampSD"))
            w.setTabOrder(w.findChild(QLineEdit, "ampSD"), w.findChild(QLineEdit,"E"))
        w.setTabOrder(w.findChild(QLineEdit, "E"), w.findChild(QLineEdit,"Tau1"))
        w.setTabOrder(w.findChild(QLineEdit, "Tau1"), w.findChild(QLineEdit,"Tau2"))
        lastWeightTab = w.findChild(QLineEdit, "Tau2")
    #### i-step tab order
    elif(w.findChild(QComboBox, "Weight Picker").currentIndex() == 0):
        durPicker = w.findChild(QComboBox, "Duration Picker")
        if(durPicker.currentIndex() == 0):
            firstDur = w.findChild(QLineEdit, "Duration")
            lastWeightTab = w.findChild(QLineEdit, "Duration")
        elif(durPicker.currentIndex() == 1):
            firstDur = w.findChild(QLineEdit, 'Duration Uniform Mean')
            lastWeightTab = w.findChild(QLineEdit, 'Duration Uniform SD')
        else:
            firstDur = w.findChild(QLineEdit, 'Duration Poisson Mean')
            lastWeightTab = w.findChild(QLineEdit, 'Duration Poisson SD')
            
        w.setTabOrder(w.findChild(QLineEdit, "highlight"), w.findChild(QLineEdit,"Current Name"))
        if(w.findChild(QRadioButton, "curSingle").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "Current Name"), w.findChild(QLineEdit,"Single Current"))
            w.setTabOrder(w.findChild(QLineEdit, "Single Current"), firstDur)
        elif(w.findChild(QRadioButton, "curMult").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "Current Name"), w.findChild(QLineEdit,"cur Uni Mean"))
            w.setTabOrder(w.findChild(QLineEdit, "cur Uni Mean"), w.findChild(QLineEdit, "cur Uni SD"))
            w.setTabOrder(w.findChild(QLineEdit, "cur Uni SD"), firstDur)
        else:
            w.setTabOrder(w.findChild(QLineEdit, "Current Name"), w.findChild(QLineEdit,"curMean"))
            w.setTabOrder(w.findChild(QLineEdit, "curMean"), w.findChild(QLineEdit, "curSD"))
            w.setTabOrder(w.findChild(QLineEdit, "curSD"), firstDur)
        if(durPicker.currentIndex() != 0):
            w.setTabOrder(firstDur, lastWeightTab)
    ######################THIS IS FOR CUSTOM################    
    else:
        if(w.findChild(QRadioButton, "custSingle").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "ModFile"), w.findChild(QLineEdit, "Single Custom"))
            lastWeightTab = w.findChild(QLineEdit, "Single Custom")
        elif(w.findChild(QRadioButton, "custMult").isChecked()):
            w.setTabOrder(w.findChild(QLineEdit, "ModFile"), w.findChild(QLineEdit, "cust Uni Mean"))
            w.setTabOrder(w.findChild(QLineEdit, "cust Uni Mean"), w.findChild(QLineEdit, "cust Uni SD"))
            lastWeightTab = w.findChild(QLineEdit, "cust Uni SD")
        else:
            w.setTabOrder(w.findChild(QLineEdit, "ModFile"), w.findChild(QLineEdit, "custMean"))
            w.setTabOrder(w.findChild(QLineEdit, "custMean"), w.findChild(QLineEdit, "custSD"))
            lastWeightTab = w.findChild(QLineEdit, "custSD")
   
    ###location
    if(w.findChild(QRadioButton, "locSingle").isChecked()):
        w.setTabOrder(lastWeightTab, w.findChild(QLineEdit, "Section Number"))
        w.setTabOrder(w.findChild(QLineEdit, "Section Number"), w.findChild(QLineEdit, "Distance"))
        lastLocTab = w.findChild(QLineEdit, "Distance") 
    elif(w.findChild(QRadioButton, "locMult").isChecked()):
        w.setTabOrder(lastWeightTab, w.findChild(QLineEdit, "Uniform Section Number"))
        w.setTabOrder(w.findChild(QLineEdit, "Uniform Section Number"), w.findChild(QLineEdit, "Uniform Mean"))
        w.setTabOrder(w.findChild(QLineEdit, "Uniform Mean"), w.findChild(QLineEdit, "Uniform SD"))
        lastLocTab = w.findChild(QLineEdit, "Uniform SD")
    else:
        w.setTabOrder(lastWeightTab, w.findChild(QLineEdit, "PD Section Number"))
        w.setTabOrder(w.findChild(QLineEdit, "PD Section Number"), w.findChild(QLineEdit, "Location Mean"))
        w.setTabOrder(w.findChild(QLineEdit, "Location Mean"), w.findChild(QLineEdit, "Location SD"))
        lastLocTab = w.findChild(QLineEdit, "Location SD")
    ###Experiment box tab order
    w.setTabOrder(lastLocTab, w.findChild(QLineEdit, "Experiment Name"))
    w.setTabOrder(w.findChild(QLineEdit, "Experiment Name"), w.findChild(QLineEdit, "Inputs"))
    w.setTabOrder(w.findChild(QLineEdit, "Inputs"), w.findChild(QLineEdit, "Time of Onset"))
    ###time
    if(w.findChild(QRadioButton, "timeSingle").isChecked()):
        w.setTabOrder(w.findChild(QLineEdit, "Time of Onset"), w.findChild(QLineEdit, "Interval"))
        lastTimeTab = w.findChild(QLineEdit, "Interval")
    elif(w.findChild(QRadioButton, "timeMult").isChecked()):
        w.setTabOrder(w.findChild(QLineEdit, "Time of Onset"), w.findChild(QLineEdit, "Interval M Mean"))
        w.setTabOrder(w.findChild(QLineEdit, "Interval M Mean"), w.findChild(QLineEdit, "Interval M SD"))
        lastTimeTab = w.findChild(QLineEdit, "Interval M SD")
    else:
        w.setTabOrder(w.findChild(QLineEdit, "Time of Onset"), w.findChild(QLineEdit, "Interval Mean"))
        w.setTabOrder(w.findChild(QLineEdit, "Interval Mean"), w.findChild(QLineEdit, "Interval SD"))
        lastTimeTab = w.findChild(QLineEdit, "Interval SD")
    ### last tab steps
    w.setTabOrder(lastTimeTab, w.findChild(QLineEdit, "Output File"))
    w.setTabOrder(w.findChild(QLineEdit, "Output File"), w.findChild(QLineEdit, "Run Number"))
    
##########################################
####### Save/edit/delete weights
###########################################

###handles weight save button
def saveButtonClicked(parent):
    logDebug("gui_handler.py::saveButtonClicked() called.\n")
    inputVar = None
    
    if(parent.findChild(QComboBox, "Weight Picker").currentIndex() == 1):
        name = parent.findChild(QLineEdit, "Weight Name").text()
        e = parent.findChild(QLineEdit, "E").text()
        tau1 = parent.findChild(QLineEdit, "Tau1").text()
        tau2 = parent.findChild(QLineEdit, "Tau2").text()
        
        if(parent.findChild(QRadioButton, "ampSingle").isChecked()):
            inputVar = synInput(0, name, e, tau1, tau2, parent, parent.findChild(QLineEdit, "Single Weight").text())
        elif(parent.findChild(QRadioButton, "ampMult").isChecked()):
            inputVar = synInput(1, name, e, tau1, tau2, parent, mean=parent.findChild(QLineEdit, "amp Uni Mean").text(), sd=parent.findChild(QLineEdit, "amp Uni SD").text())
        else:
            inputVar = synInput(2, name, e, tau1, tau2, parent, mean=parent.findChild(QLineEdit, "ampMean").text(), sd=parent.findChild(QLineEdit, "ampSD").text())
    #### CURRENT INPUT ####
    elif(parent.findChild(QComboBox, "Weight Picker").currentIndex() == 0):
        name = parent.findChild(QLineEdit, "Current Name").text()
        if(parent.findChild(QComboBox, "Duration Picker").currentIndex() == 0):
            dur = parent.findChild(QLineEdit, "Duration").text()
            durMean = None
            durSD = None
            durType = 0
        elif(parent.findChild(QComboBox, "Duration Picker").currentIndex() == 1):
            dur = None
            durMean = parent.findChild(QLineEdit, "Duration Uniform Mean").text()
            durSD = parent.findChild(QLineEdit, "Duration Uniform SD").text()
            durType = 1
        else:
            dur = None
            durMean = parent.findChild(QLineEdit, "Duration Poisson Mean").text()
            durSD = parent.findChild(QLineEdit, "Duration Poisson SD").text()
            durType = 2
            
        if(parent.findChild(QRadioButton, "curSingle").isChecked()):
            inputVar = curInput(0, name, dur, parent, parent.findChild(QLineEdit, "Single Current").text(), durMean = durMean, durSD = durSD, durType = durType)
        elif(parent.findChild(QRadioButton, "curMult").isChecked()):
            inputVar = curInput(1, name, dur, parent, mean=parent.findChild(QLineEdit, "cur Uni Mean").text(), sd=parent.findChild(QLineEdit, "cur Uni SD").text(), durMean = durMean, durSD = durSD, durType = durType)
        else:
            inputVar = curInput(2, name, dur, parent, mean=parent.findChild(QLineEdit, "curMean").text(), sd=parent.findChild(QLineEdit, "curSD").text(), durMean = durMean, durSD = durSD, durType = durType)
    else: ###CUSTOM###
        modpath = parent.findChild(QLineEdit, "ModFile").text()
        if(parent.findChild(QRadioButton, "custSingle").isChecked()):
            inputVar = custInput(0, modpath, parent, parent.findChild(QLineEdit, "Single Custom").text())
        elif(parent.findChild(QRadioButton, "custMult").isChecked()):
            inputVar = custInput(1, modpath, parent, mean=parent.findChild(QLineEdit, "cust Uni Mean").text(), sd=parent.findChild(QLineEdit, "cust Uni SD").text())
        else:
            inputVar = custInput(2, modpath, parent, mean=parent.findChild(QLineEdit, "custMean").text(), sd=parent.findChild(QLineEdit, "custSD").text())

    ##ERROR CHECK###
    if(inputVar.err != ""):
        newMsgBox(inputVar.err)
        return
    
    if(gv.editMode is not None):
        gv.weightInputs[gv.editMode] = inputVar
        gv.model.removeRows(gv.editMode, 1)
        gv.model.insertRow(gv.editMode, [QStandardItem(inputVar.type), QStandardItem(inputVar.name), QStandardItem(inputVar.getFunc())])
        gv.editMode = None
    else:
        gv.weightInputs.append(inputVar)
        gv.model.appendRow([QStandardItem(inputVar.type), QStandardItem(inputVar.name), QStandardItem(inputVar.getFunc())])    

###handles weight and experiment delete buttons
def deleteButtonClicked(table, arr, model):
    logDebug("gui_handler.py::deleteButtonClicked() called.\n")
    indexes = table.selectedIndexes()
    if(len(indexes) < 1):
        return
    rows = []
    for i in indexes:
        rows.append(i.row())

    rows = removeDupes(rows)
    
    if(len(rows) > 1):
        newMsgBox("Please select only one row at a time to delete!")
        return

    del arr[rows[0]]
    model.removeRow(rows[0])

    if gv.editMode == rows[0]:
        gv.editMode = None
    
###handles weight table row click, used to edit weight data
def editButtonClicked(parent, table):
    logDebug("gui_handler.py::editButtonClicked() called.\n")
    indexes = table.selectedIndexes()
    if(len(indexes) < 1):
        return
    rows = []
    for i in indexes:
        rows.append(i.row())
        
    rows = removeDupes(rows)
    
    if(len(rows) > 1):
        newMsgBox("Please select only one row at a time to edit!")
        return
    
    gv.editMode = rows[0]
    curRec = gv.weightInputs[rows[0]]
    curRec.setElements(parent)
    curRec.editGUI()
    
###################################
#### Experiment save/edit/delete handlers
##################################

###experiment save button handler
def allSaveButtonClicked(aWin):
    logDebug("gui_handler.py::allSaveButtonClicked() called.\n")
    
    #####LOCATION checks
    if(aWin.findChild(QRadioButton, "locSingle").isChecked()):
        locObj = locObject(0, aWin.findChild(QComboBox, "Single Picker").currentIndex(), aWin.findChild(QLineEdit, "Section Number").text(), aWin.findChild(QLineEdit, "Distance").text())
    
    elif(aWin.findChild(QRadioButton, "locMult").isChecked()):
        locObj = locObject(1, aWin.findChild(QComboBox, "Uniform Picker").currentIndex(), aWin.findChild(QLineEdit, "Uniform Section Number").text(), mean = aWin.findChild(QLineEdit, "Uniform Mean").text(), sd = aWin.findChild(QLineEdit, "Uniform SD").text())
        
    else:
        locObj = locObject(2, aWin.findChild(QComboBox, "PD Picker").currentIndex(), aWin.findChild(QLineEdit, "PD Section Number").text(), mean = aWin.findChild(QLineEdit, "Location Mean").text(), sd = aWin.findChild(QLineEdit, "Location SD").text())
    ##location error check
    if(locObj.err != ""):
        newMsgBox(locObj.err)
        return
        
    #####TIME Setup
    onsetTime = aWin.findChild(QLineEdit, "Time of Onset").text()
    if(aWin.findChild(QRadioButton, "timeSingle").isChecked()):
        timeObj = timeObject(0, onsetTime, aWin.findChild(QLineEdit, "Interval").text())
        
    elif(aWin.findChild(QRadioButton, "timeMult").isChecked()):
        timeObj = timeObject(1, onsetTime, mean=aWin.findChild(QLineEdit, "Interval M Mean").text(), sd=aWin.findChild(QLineEdit, "Interval M SD").text())
        
    else:
        timeObj = timeObject(2, onsetTime, mean=aWin.findChild(QLineEdit, "Interval Mean").text(), sd=aWin.findChild(QLineEdit, "Interval SD").text())
        
    ##time error check
    if(timeObj.err != ""):
        newMsgBox(timeObj.err)
        return
    #####Need to clear the UI elements I set in the class because deepcopy doesn't like them
    for w in gv.weightInputs:
        w.clearElements()
        
    allVar = experimentObject(aWin.findChild(QLineEdit, "Experiment Name").text(), locObj, timeObj, deepcopy(gv.weightInputs), aWin.findChild(QLineEdit, "Inputs").text(), getColor(), aWin.findChild(QCheckBox, "somaCB").isChecked(), aWin.findChild(QCheckBox, "apicalCB").isChecked(),aWin.findChild(QCheckBox, "basalCB").isChecked(), aWin.findChild(QCheckBox, "axonCB").isChecked())
    
    if(allVar.err):
        newMsgBox(allVar.errString)
        return
    
    citem = QStandardItem()
    br = QBrush(QColor(allVar.color))
    br.setStyle(QtCore.Qt.SolidPattern)
    citem.setBackground(br)
    
    if(gv.allEditMode is not None):
        gv.experiments[gv.allEditMode] = allVar
        gv.allModel.removeRows(gv.allEditMode, 1)
        gv.allModel.insertRow(gv.allEditMode, [QStandardItem(allVar.name), QStandardItem(allVar.inputs), citem])
        gv.allEditMode = None
    else:
        gv.experiments.append(allVar)
        gv.allModel.appendRow([QStandardItem(allVar.name), QStandardItem(allVar.inputs), citem])
    resetClicked(aWin)

###handles an experiment data row being selected, to edit the data
def editInputButtonClicked(parent, table):
    logDebug("gui_handler.py::editInputButtonClicked() called.\n")
    indexes = table.selectedIndexes()
    if(len(indexes) < 1):
        return
    rows = []
    for i in indexes:
        rows.append(i.row())
        
    rows = removeDupes(rows)
    
    if(len(rows) > 1):
        newMsgBox("Please select only one row at a time to edit!")
        return
    
    gv.allEditMode = rows[0]
    curRec = gv.experiments[rows[0]]
    curRec.editGUI(parent)

###clears all data entered into the data table (weight and experiment)
def clearButtonClicked(alist, model, headers, editmode, table):
    logDebug("gui_handler.py::clearButtonClicked() called.\n")
    del alist[:]
    model.clear()
    model.setHorizontalHeaderLabels(headers)
    table.setColumnWidth(0, 105)
    table.setColumnWidth(1, 105)
    table.setColumnWidth(2, 106)
    if(editmode == 1):
        gv.editMode = None
    else:
        gv.allEditMode = None

###handles the reset button clicked, clears all data from the UI, and returns each section to the 'default' state. Doesn't clear the loaded morphology data
def resetClicked(p):
    logDebug("gui_handler.py::resetClicked() called.\n")
    lineEdits = p.findChildren(QLineEdit)
    checkBoxes = p.findChildren(QCheckBox)
    comboBoxes = p.findChildren(QComboBox)

    for c in lineEdits:
        if(c.objectName() != "soma" and c.objectName() != "apical" and c.objectName() != "basal" and c.objectName() != "axon" and c.objectName() != "fileName" and c.objectName() != "Output File"):
            c.setText("")
            
    for c in checkBoxes:
        c.setChecked(True)
        
    for c in comboBoxes:
        c.setCurrentIndex(0)

    p.findChild(QLineEdit, "Distance").setText('0')
    p.findChild(QLineEdit, "Run Number").setText('1')
    p.findChild(QRadioButton, "locSingle").setChecked(True)
    p.findChild(QRadioButton, "timeSingle").setChecked(True)
    p.findChild(QRadioButton, "ampSingle").setChecked(True)
    p.findChild(QRadioButton, "curSingle").setChecked(True)

##removes duplicate row selection data
def removeDupes(l):
    logDebug("gui_handler.py::removeDupes() called.\n")
    return list(dict.fromkeys(l))

##returns the currently selected color
def getColor():
    logDebug("gui_handler.py::getColor() called.\n")
    return gv.color.name()

###handles Load .nrnez button click
def nrnezButtonClicked(w):
    logDebug("gui_handler.py::nrnezButtonClicked() called.\n")
    try:
        fname = QFileDialog.getOpenFileName(w, 'Open File', '~/', "NRNEZ (*.nrnez)")[0]
        if(fname is None or fname == ''):
            return
        loadNRNEZ(w, fname)
    except Exception as ex:
        newMsgBox("Error loading .nrnez file", str(ex))
        logErr(str(ex), 'gui_handler::nrnezButtonClicked()')


##handles reload button clicked, used to reload previously generated sessions
def reloadButtonClicked(q):
    logDebug("gui_handler.py::reloadButtonClicked() called.\n")
    try:
        fname = QFileDialog.getOpenFileName(q, 'Open File', '~/', "PKL (*.pkl)")[0]
        if(fname is None or fname == ''):
            return
        fpath = fname.split("/data.pkl")[0]
        q.findChild(QLineEdit, "Output File").setText(fpath)

        clearButtonClicked(gv.weightInputs, gv.model, ['Module', 'Name', 'Weight'], gv.editMode, gv.wTable)
        clearButtonClicked(gv.experiments, gv.allModel, ['Tag', 'Num. Inputs', 'Color'], gv.allEditMode, gv.inputTable)

        loadPickle(fname)
        ##there should always be at least one run, and all the swc files are the same
        swcPath = fpath + '/run_1/' + gv.morphObj.swcfname + '.swc'
        lineEdits = [q.findChild(QLineEdit, 'soma'), q.findChild(QLineEdit, 'apical'), q.findChild(QLineEdit, 'basal'), q.findChild(QLineEdit, 'axon')]
        q.findChild(QLineEdit, "fileName").setText(swcPath)
    
        gv.morphObj.loadFile(swcPath, lineEdits)
    
        for exp in gv.experiments:
            citem = QStandardItem()
            br = QBrush(QColor(exp.color))
            br.setStyle(QtCore.Qt.SolidPattern)
            citem.setBackground(br)
        
            gv.allModel.appendRow([QStandardItem(exp.name), QStandardItem(exp.inputs), citem])
            gv.morphObj.plotInputs(fpath + "/run_1/" + exp.name + "/syn_loc.dat", exp.color)

    except Exception as ex:
        newMsgBox("Error reloading previous session", str(ex))
        logErr(str(ex), 'gui_handler::reloadButtonClicked()')

###creates directory
def createDir(path):
    logDebug("gui_handler.py::createDir() called. Path:: " + path + "\n")
    try:
        os.mkdir(path)
        return 1
    except Exception as ex:
        newMsgBox("Unable to create directory: " + path, str(ex))
        logErr(str(ex), 'gui_handler::createDir()')
        return 0

##handles run button being clicked, generates all output data
def generateButton(parent):                                       
    logDebug("gui_handler.py::generateButton() called.\n")
    ##general error checking for required data
    if(gv.morphObj.fLoadFlag != True):
        newMsgBox("No morphology loaded!")
        return
    if(parent.findChild(QLineEdit, "Output File").text() == ""):
        newMsgBox("Please enter an output file path!")
        return
    if(parent.findChild(QLineEdit, "Run Number").text() == ""):
        newMsgBox("Please enter the desired number of runs!")
        return
    if(len(gv.experiments) < 1):
        newMsgBox("Please add at least one Tag")
        return
    
    swcPath = gv.morphObj.swcPath
    swcFile = swcPath.split("/")[-1]
    curTime = datetime.now()
    numRuns = int(parent.findChild(QLineEdit, "Run Number").text())
    outPath = parent.findChild(QLineEdit, "Output File").text()
    allPath = outPath + "/nrnez_" + curTime.strftime("%Y_%m_%d_%H_%M_%S")
    cwd = os.getcwd()
    tmp = os.path.dirname(os.path.realpath(__file__)) + '/incl/tmp'
    if not createDir(allPath):
        return
    
    ###something went wrong previously so cleanup the tmp dir and recreate
    if os.path.isdir(tmp):
        rmtree(tmp)
        
    if not createDir(tmp):
        return

    gv.morphObj.clearInputs()

    ###used for custom code creation
    exclude = []
    if(len(gv.morphObj.somaInputs) == 0):
        exclude.append('//~~~SOMA~~~//')
    if(len(gv.morphObj.apicalInputs) == 0):
        exclude.append('//~~~APICAL~~~//')
    if(len(gv.morphObj.basalInputs) == 0):
        exclude.append('//~~~BASAL~~~//')
    if(len(gv.morphObj.axonInputs) == 0):
        exclude.append('//~~~AXON~~~//')

    ####i don't like adding the cursor restore before every return, consider try/finally or maybe put the restore in the msgbox function?
    QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
    for run in range(numRuns):
        path = allPath + "/run_" + str(run + 1)

        if not createDir(path):
            QApplication.restoreOverrideCursor()
            return
        
        uid = 1
    
        for exp in gv.experiments:
            exp.path = path + "/" + exp.name
            if not createDir(exp.path):
                exp.path = None
                QApplication.restoreOverrideCursor()
                return

            exp.generate(parent)
        
            #### error checking                                                         
            if(exp.err):
                QApplication.restoreOverrideCursor()
                newMsgBox(exp.err)
                return                                             

            try:
                exp.genHocFile(exclude, uid)
                uid = uid + 1
            except Exception as err:
                QApplication.restoreOverrideCursor()
                newMsgBox("Error generating Hoc files", str(err))
                logErr(str(err), 'gui_handler::generate::genHocFile')
                return


            #####this should be the same for each run, consider restructure to pull this out
        #####maybe create once then copy to each folder? Seems it should be in each run folder to plug and play in Neuron
        try:
            gv.morphObj.genNrn(path)
            gv.morphObj.genOverall(gv.experiments, path)
        except Exception as err:
            QApplication.restoreOverrideCursor()
            newMsgBox("Error generating overall hoc files", str(err))
            logErr(str(err), 'gui_handler::generate::genNrn/Overall')
            return
        try:
            copy2(swcPath, path + "/" + swcFile)
        except Exception as ex:
            QApplication.restoreOverrideCursor()
            newMsgBox("Error copying swc file", str(ex))
            logErr(str(ex), 'gui_handler::generate::copy2')
            return

        try:
            os.chdir(path)
            subprocess.run("nrnivmodl", shell=True)
            os.chdir(cwd)
        except Exception as ex:
            QApplication.restoreOverrideCursor()
            newMsgBox("Error running nrnivmodl", str(ex))
            logErr(str(ex), "gui_handler::generate::subprocess")
        
    ##################plot just the last set of points ###########
    for exp in gv.experiments:
        try:
            gv.morphObj.plotInputs(exp.path + "/syn_loc.dat", exp.color)
        except Exception as err:
            QApplication.restoreOverrideCursor()
            newMsgBox("Error plotting inputs", str(err))
            logErr(str(ex), 'gui_handler::generate::plotInputs')
            return

    ##clean up
    rmtree(tmp)
    ######Need to clear UI elements set in the objects before we pickle, only need one pickle    
    for exp in gv.experiments:
        exp.clearElements()
    gv.morphObj.clearPlot()
    ###pickle
    savePickle(allPath + "/data.pkl")
    ###restore plot object
    gv.morphObj.restorePlot()

    QApplication.restoreOverrideCursor()
    
    newMsgBox("Neuron files generated!", None, "Success")

