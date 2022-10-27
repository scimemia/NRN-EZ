###################################################################
####
#### Version: 1.1.5
#### Date: 10/26/2022
#### Description: This file creates the GUI for NRN-EZ.
#### Author: Evan Cobb
####
###################################################################
 
import sys
import globvar as gv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui_helper import *
from gui_handler import *
from errorLogger import *
from loader import loadNRNEZ
import morphologyClass as mc
import pyqtgraph as pg

####creates the GUI window and all elements in it
def window():
    logDebug("gui.py::window() called\n")
    logRun("Started NRN-EZ")
    
    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(100,100,1078,525)
    w.setMinimumSize(1200, 525)
    w.setWindowTitle("NRN-EZ")
    w.setWindowIcon(QIcon(gv.incPath + 'nrnez.png'))
    
    windowLayout = QHBoxLayout(w)
    windowLayout.setContentsMargins(0,0,0,0)
    
    leftPanel = QFrame()
    leftPanel.setFrameStyle(QFrame.Panel)
    leftPanel.setLineWidth(1)
    leftPanel.setStyleSheet(""".QFrame{border:1px solid lightgray;}""")
    leftPanel.setSizePolicy(QSizePolicy.Expanding, leftPanel.sizePolicy().verticalPolicy())
    middlePanel = QFrame()
    middlePanel.setFrameStyle(QFrame.Panel)
    middlePanel.setLineWidth(1)
    middlePanel.setStyleSheet(""".QFrame{border:1px solid lightgray;}""")
    middlePanel.setSizePolicy(QSizePolicy.Expanding, middlePanel.sizePolicy().verticalPolicy())
    rightPanel = QFrame()
    rightPanel.setSizePolicy(QSizePolicy.Expanding, rightPanel.sizePolicy().verticalPolicy())
    rightPanel.setFrameStyle(QFrame.Panel)
    rightPanel.setLineWidth(1)
    rightPanel.setStyleSheet(""".QFrame{border:1px solid lightgray;}""")
    windowLayout.addWidget(leftPanel)
    windowLayout.addWidget(middlePanel)
    windowLayout.addWidget(rightPanel)
    
    leftLO = QVBoxLayout(leftPanel)
    midLO = QVBoxLayout(middlePanel)
    rightLO = QVBoxLayout(rightPanel)
    leftLO.setContentsMargins(5,5,5,5)
    midLO.setContentsMargins(0,0,0,0)
    rightLO.setContentsMargins(0,0,0,0)
    
      
    h1 = QHBoxLayout()
    h1.setContentsMargins(0,0,0,0)
    browseButton = newButton(h1, "Browse")
    browseButton.clicked.connect(lambda: fileSelect(browseButton, fileName_le, "SWC (*.swc)"))
    fileName_le = newLineEdit(h1, 'fileName') 
    
    leftLO.addLayout(h1)

    h2 = QHBoxLayout()
    h2.setContentsMargins(0,0,0,0)
    loadButton = newButton(h2, "Load")                                                          
    loadButton.clicked.connect(lambda: gv.morphObj.loadFile(fileName_le.text(), [somaLineEdit, apicalLineEdit, basalLineEdit, axonLineEdit]))
    h2.addStretch(1)
    loadNRNEZButton = newButton(h2, "Load .nrnez")                                           
    loadNRNEZButton.clicked.connect(lambda: nrnezButtonClicked(w))
    reloadButton = newButton(h2, "Reload Session")
    reloadButton.clicked.connect(lambda: reloadButtonClicked(w))

    leftLO.addLayout(h2)

    h3 = QHBoxLayout()
    h3.setContentsMargins(0,0,0,0)
    segmentLabel = newLabel(h3, "Segments in each section:")           
    h3.setAlignment(segmentLabel, Qt.AlignLeft)
    leftLO.addLayout(h3)

    
    h4 = QHBoxLayout()
    h4.setContentsMargins(0,0,0,0)
    somaLabel = newLabel(h4, 'Soma:')           
    somaLineEdit = newLineEdit(h4, 'soma')
    somaLineEdit.setMaximumWidth(80)
    somaLineEdit.setReadOnly(True)
    h4.addStretch(1)
    apicalLabel = newLabel(h4, 'Apical Dendrite:')
    apicalLineEdit = newLineEdit(h4, 'apical')
    apicalLineEdit.setMaximumWidth(80)
    apicalLineEdit.setReadOnly(True)
    h4.setAlignment(somaLabel, Qt.AlignLeft)
    h4.setAlignment(somaLineEdit, Qt.AlignLeft)
    h4.setAlignment(apicalLineEdit, Qt.AlignRight)
    h4.setAlignment(apicalLabel, Qt.AlignRight)

    leftLO.addLayout(h4)

    h5 = QHBoxLayout()
    h5.setContentsMargins(0,0,0,0)
    axonLabel = newLabel(h5, 'Axon: ')
    axonLineEdit = newLineEdit(h5, 'axon')
    axonLineEdit.setMaximumWidth(80)
    axonLineEdit.setReadOnly(True)
    h5.addStretch(1)
    basalLabel = newLabel(h5, ' Basal Dendrite:')
    basalLineEdit = newLineEdit(h5, 'basal')
    basalLineEdit.setMaximumWidth(80)
    basalLineEdit.setReadOnly(True) 
    h5.setAlignment(axonLabel, Qt.AlignLeft)
    h5.setAlignment(axonLineEdit, Qt.AlignLeft)
    h5.setAlignment(basalLineEdit, Qt.AlignRight)
    h5.setAlignment(basalLabel, Qt.AlignRight)

    leftLO.addLayout(h5)
    
    h6 = QHBoxLayout()
    h6.setContentsMargins(0,0,0,0)
    selectedLabel = newLabel( h6, 'Highlighted Segment: ')  
    highlightLE = newLineEdit(h6, 'highlight', QIntValidator())                          
    highlightLE.validator().setBottom(1)                                                              
    highlightLE.setMaximumWidth(80)
    highlightPicker = newComboBox(h6, ["Soma", "Axon", "Basal", "Apical"], "Highlight Picker") 
    highlightLE.textChanged.connect(lambda: gv.morphObj.textChanged(highlightLE, highlightPicker))    
    highlightPicker.currentIndexChanged.connect(lambda: gv.morphObj.textChanged(highlightLE, highlightPicker))
    h6.addStretch(1)

    leftLO.addLayout(h6)

    gLO = QHBoxLayout()
    gLO.setContentsMargins(0,0,0,0)

    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    gv.graphWin = pg.GraphicsWindow()
    gv.graphWin.setMaximumWidth(382)
    gLO.addWidget(gv.graphWin)
    leftLO.addLayout(gLO)

    gv.graphWin.setFocusPolicy(Qt.ClickFocus)
    
    gv.morphObj = mc.morphologyClass()

    h7 = QHBoxLayout()
    h7.setContentsMargins(0,5,0,0)

    outputBrowseButton = newButton(h7, "Set Path")
    outputFile_le = newLineEdit(h7, 'Output File')  
    outputBrowseButton.clicked.connect(lambda: fileSelectOutput(outputBrowseButton, outputFile_le)) 

    leftLO.addLayout(h7)
    
    h8 = QHBoxLayout()
    h8.setContentsMargins(0,0,0,0)
    genNumberLE = newLineEdit(h8, "Run Number", QIntValidator())
    genNumberLE.validator().setBottom(0)
    genNumberLE.setText('1')
    genNumberLE.setAlignment(QtCore.Qt.AlignRight)
    genNumberLE.setMaximumWidth(80)
    genButton = newButton(h8, "Run")
    h8.addStretch(3)
    resetButton = newButton(h8, "Reset Fields")
    genButton.clicked.connect(lambda: generateButton(w))
    resetButton.clicked.connect(lambda: resetClicked(w))

    leftLO.addLayout(h8)
    
    
    app.lastWindowClosed.connect(lambda: closingApp())
    
    ####tabbing setup
    outputBrowseButton.setFocusPolicy(Qt.ClickFocus)
    resetButton.setFocusPolicy(Qt.ClickFocus)
    genButton.setFocusPolicy(Qt.ClickFocus)
    reloadButton.setFocusPolicy(Qt.ClickFocus)
    loadButton.setFocusPolicy(Qt.ClickFocus)
    loadNRNEZButton.setFocusPolicy(Qt.ClickFocus)
    browseButton.setFocusPolicy(Qt.ClickFocus)
    highlightPicker.setFocusPolicy(Qt.ClickFocus)
    somaLineEdit.setFocusPolicy(Qt.ClickFocus)
    axonLineEdit.setFocusPolicy(Qt.ClickFocus)
    basalLineEdit.setFocusPolicy(Qt.ClickFocus)
    apicalLineEdit.setFocusPolicy(Qt.ClickFocus)
    w.setTabOrder(fileName_le, highlightLE)

    ##setup each section of the application
    setupWeight(w, midLO)
    setupLoc(w, midLO)
    setupInputControl(w, rightLO)
    setupTime(w, rightLO)
    
    setTabOrder(w)

    w.show()
    
    ###if there is a .nrnez file in the config, load it
    if(gv.nrnezPath != ''):
        try:
            loadNRNEZ(w, gv.nrnezPath)
        except Exception as ex: ##we'll log the error, but no need to interupt the app
            logErr(str(ex), 'gui.py::loadNRNEZ() call')

    sys.exit(app.exec_())

####creates the Location GUI portion of the application    
def setupLoc(rWindow, midLO):
    logDebug("gui.py::setupLoc() called\n")

    locBox = QVBoxLayout()
    locBox.setContentsMargins(5,5,5,5)
    midLO.addLayout(locBox)

    h1 = QHBoxLayout()
    h1.setContentsMargins(0,0,0,0)
    locBox.addLayout(h1)
    h2 = QHBoxLayout()
    h2.setContentsMargins(0,0,0,0)
    locBox.addLayout(h2)
    h3 = QHBoxLayout()
    h3.setContentsMargins(0,0,0,0)
    locBox.addLayout(h3)
    h4 = QHBoxLayout()
    h4.setContentsMargins(0,0,0,0)
    locBox.addLayout(h4)
    
    locLabel = newLabel(h1, "Location: ")
    locSRB = newRadioButton(h2, "Single", True,"locSingle")
    locURB = newRadioButton(h3, "Multiple Uniform", False, "locMult")
    locPRB = newRadioButton(h4, "Multiple Poisson", False, "locPos")
    locDisBG = newButtonGroup(rWindow, [locSRB, locURB, locPRB], "locDisBG")

    sbw1 = QWidget()
    sbw1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    ubw1 = QWidget()
    ubw1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    pbw1 = QWidget()
    pbw1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    ubw1.hide()
    pbw1.hide()

    h2.addStretch(1)
    h2.addWidget(sbw1)
    h2.addWidget(ubw1)
    h2.addWidget(pbw1)
    h2.setAlignment(sbw1, Qt.AlignRight)
    h2.setAlignment(ubw1, Qt.AlignRight)
    h2.setAlignment(pbw1, Qt.AlignRight)
    
    h1.addStretch(1)
    locSingleLabel = newLabel(h1, "Segment Number: ")
    h1.setAlignment(locSingleLabel, Qt.AlignRight)

    sbwLO = QHBoxLayout(sbw1)
    sbwLO.setContentsMargins(0,0,0,0)
    locSingleLE = newLineEdit(sbwLO, 'Section Number', QIntValidator())
    locSingleLE.validator().setBottom(0)
    locSingleLE.setMaximumWidth(50)
    sbwLO.setAlignment(locSingleLE, Qt.AlignRight)
    locSinglePicker = newComboBox(sbwLO, ["Soma", "Axon", "Basal", "Apical"], "Single Picker")

    sbw2 = QWidget()
    sbw2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    ubw2 = QWidget()
    ubw2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    pbw2 = QWidget()
    pbw2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    ubw2.hide()
    pbw2.hide()
    
    h3.addWidget(sbw2)
    h3.addWidget(ubw2)
    h3.addWidget(pbw2)
    h3.setAlignment(sbw2, Qt.AlignRight)
    h3.setAlignment(ubw2, Qt.AlignRight)
    h3.setAlignment(pbw2, Qt.AlignRight)

    
    sbwLO2 = QHBoxLayout(sbw2)
    sbwLO2.setContentsMargins(0,0,0,0)
    locSingleDist = newLabel(sbwLO2, "Distance (" + "\u03BC" + "m): ")
    locSingleDistLE = newLineEdit(sbwLO2, "Distance", newDVal(2,0))
    locSingleDistLE.setText('0')
    locSingleDistLE.setMaximumWidth(50)
    sbwLO2.setAlignment(locSingleDist, Qt.AlignRight)
    sbwLO2.setAlignment(locSingleDistLE, Qt.AlignRight)
    
    ubwLO = QHBoxLayout(ubw1)
    ubwLO.setContentsMargins(0,0,0,0)
    locUniformLE = newLineEdit(ubwLO, 'Uniform Section Number', QIntValidator())
    ubwLO.setAlignment(locUniformLE, Qt.AlignRight)
    locUniformLE.validator().setBottom(0)        
    locUniformPicker = newComboBox(ubwLO, ["Soma", "Axon", "Basal", "Apical"], "Uniform Picker")
    ubwLO.setAlignment(locUniformLE, Qt.AlignRight)
    locUniformLE.setMaximumWidth(50)
    
    ubwLO2 = QHBoxLayout(ubw2)
    ubwLO2.setContentsMargins(0,0,0,0)
    locUniMeanLabel = newLabel(ubwLO2, "Mean(" + "\u03BC" + "m): ")
    locUniMeanLineEdit = newLineEdit(ubwLO2, 'Uniform Mean', newDVal(2,0))
    locUniMeanLineEdit.setMaximumWidth(50)
    locUniSDLabel = newLabel(ubwLO2, "S.D.: ")
    locUniSDLineEdit = newLineEdit(ubwLO2, 'Uniform SD', newDVal(2,0))
    locUniSDLineEdit.validator().setBottom(0)
    locUniSDLineEdit.setMaximumWidth(50)
    ubwLO2.setAlignment(locUniMeanLabel, Qt.AlignRight)
    ubwLO2.setAlignment(locUniMeanLineEdit, Qt.AlignRight)
    ubwLO2.setAlignment(locUniSDLabel, Qt.AlignRight)
    ubwLO2.setAlignment(locUniSDLineEdit, Qt.AlignRight)


    pbwLO = QHBoxLayout(pbw1)
    pbwLO.setContentsMargins(0,0,0,0)
    locPDLE = newLineEdit(pbwLO,  'PD Section Number', QIntValidator())
    locPDLE.validator().setBottom(0)
    pbwLO.setAlignment(locPDLE, Qt.AlignRight)
    locPDLE.setMaximumWidth(50)

    
    pbwLO2 = QHBoxLayout(pbw2)
    pbwLO2.setContentsMargins(0,0,0,0)
    locPMeanLabel = newLabel(pbwLO2, "Mean(" + "\u03BC" + "m): ")
    locPMeanLineEdit = newLineEdit(pbwLO2, 'Location Mean', newDVal(2,0))
    locPSDLabel = newLabel(pbwLO2, "S.D.: ")
    locPSDLineEdit = newLineEdit(pbwLO2, 'Location SD', newDVal(2,0))
    locPSDLineEdit.validator().setBottom(0)
    locPSDLineEdit.setMaximumWidth(50)
    locPMeanLineEdit.setMaximumWidth(50)
    pbwLO2.setAlignment(locPMeanLabel, Qt.AlignRight)
    pbwLO2.setAlignment(locPMeanLineEdit, Qt.AlignRight)
    pbwLO2.setAlignment(locPSDLabel, Qt.AlignRight)
    pbwLO2.setAlignment(locPSDLineEdit, Qt.AlignRight)

    locMeanPicker = newComboBox(pbwLO, ["Soma", "Axon", "Basal", "Apical"], "PD Picker")
    pbwLO.setAlignment(locMeanPicker, Qt.AlignRight)
    locPMeanLineEdit.validator().setBottom(0)
    
    locSRB.toggled.connect(lambda: radioButton2(locSRB, sbw1, ubw1, pbw1, sbw2, ubw2, pbw2,rWindow))
    locURB.toggled.connect(lambda: radioButton2(locURB, sbw1, ubw1, pbw1, sbw2, ubw2, pbw2, rWindow))
    locPRB.toggled.connect(lambda: radioButton2(locPRB, sbw1, ubw1, pbw1, sbw2, ubw2, pbw2, rWindow))

    ###tabbing setup
    locSRB.setFocusPolicy(Qt.ClickFocus)
    locURB.setFocusPolicy(Qt.ClickFocus)
    locPRB.setFocusPolicy(Qt.ClickFocus)
    locSinglePicker.setFocusPolicy(Qt.ClickFocus)
    locUniformPicker.setFocusPolicy(Qt.ClickFocus)
    locMeanPicker.setFocusPolicy(Qt.ClickFocus)

####creates the Time GUI portion of the application
def setupTime(rWindow, rightLO):
    logDebug("gui.py::setupTime() called\n")
                
    timeBox = QVBoxLayout()
    timeBox.setContentsMargins(5,5,5,5)
    rightLO.addLayout(timeBox)

    h1 = QHBoxLayout()
    h1.setContentsMargins(0,0,0,0)
    timeBox.addLayout(h1)
    h2 = QHBoxLayout()
    h2.setContentsMargins(0,0,0,0)
    timeBox.addLayout(h2)
    h3 = QHBoxLayout()
    h3.setContentsMargins(0,0,0,0)
    timeBox.addLayout(h3)
    h4 = QHBoxLayout()
    h4.setContentsMargins(0,0,0,0)
    timeBox.addLayout(h4)


    timeLabel = newLabel(h1, "Timing: ")
    h1.addStretch(1)
    onsetLabel = newLabel(h1, "Onset(ms): ")
    onsetLineEdit = newLineEdit(h1, 'Time of Onset', newDVal(10,0))
    h1.setAlignment(onsetLabel, Qt.AlignRight)
    h1.setAlignment(onsetLineEdit, Qt.AlignRight)
    onsetLineEdit.setMaximumWidth(50)
    
    timeSRB = newRadioButton(h2, "Single", True, "timeSingle")
    timeURB = newRadioButton(h3, "Multiple Uniform", False, "timeMult")
    timePRB = newRadioButton(h4, "Multiple Poisson", False, "timePos")
    timeDisBG = newButtonGroup(timeBox, [timeSRB, timeURB, timePRB], "timeDisBG")

    tsw = QWidget()
    tuw = QWidget()
    tpw = QWidget()
    tuw.hide()
    tpw.hide()
    tsw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    tuw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    tpw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    h2.addWidget(tsw)
    h2.addWidget(tuw)
    h2.addWidget(tpw)
    h2.setAlignment(tsw, Qt.AlignRight)
    h2.setAlignment(tuw, Qt.AlignRight)
    h2.setAlignment(tpw, Qt.AlignRight)

    sLO = QHBoxLayout(tsw)
    uLO = QHBoxLayout(tuw)
    pLO = QHBoxLayout(tpw)
    sLO.setContentsMargins(0,0,0,0)
    uLO.setContentsMargins(0,0,0,0)
    pLO.setContentsMargins(0,0,0,0)

    
    timeSingleLabel = newLabel(sLO, "Interval(ms): ")
    timeSingleLE = newLineEdit(sLO, 'Interval', newDVal(10,0))
    timeSingleLE.setMaximumWidth(50)
    sLO.setAlignment(timeSingleLabel, Qt.AlignRight)
    sLO.setAlignment(timeSingleLE, Qt.AlignRight)
    
    timeUMinLabel = newLabel(uLO, "Mean(ms): ")
    timeUMinLineEdit = newLineEdit(uLO, 'Interval M Mean', newDVal(10,0))
    timeUMaxLabel = newLabel(uLO, "S.D.: ")
    timeUMaxLineEdit = newLineEdit(uLO, 'Interval M SD', newDVal(10,0))
    timeUMinLineEdit.setMaximumWidth(50)
    timeUMaxLineEdit.setMaximumWidth(50)
    uLO.setAlignment(timeUMinLabel, Qt.AlignRight)
    uLO.setAlignment(timeUMinLineEdit, Qt.AlignRight)
    uLO.setAlignment(timeUMaxLabel, Qt.AlignRight)
    uLO.setAlignment(timeUMaxLineEdit, Qt.AlignRight)

    timePMeanLabel = newLabel(pLO, "Mean(ms): ")
    timePMeanLineEdit = newLineEdit(pLO, 'Interval Mean', newDVal(10,0))
    timePSDLabel = newLabel(pLO, "S.D.: ")
    timePSDLineEdit = newLineEdit(pLO, 'Interval SD', newDVal(10,0))
    timePMeanLineEdit.setMaximumWidth(50)
    timePSDLineEdit.setMaximumWidth(50)
    pLO.setAlignment(timePMeanLabel, Qt.AlignRight)
    pLO.setAlignment(timePMeanLineEdit, Qt.AlignRight)
    pLO.setAlignment(timePSDLabel, Qt.AlignRight)
    pLO.setAlignment(timePSDLineEdit, Qt.AlignRight)


    timeSRB.toggled.connect(lambda: radioButton(timeSRB, tsw, tuw, tpw, rWindow))
    timeURB.toggled.connect(lambda: radioButton(timeURB, tsw, tuw, tpw, rWindow))
    timePRB.toggled.connect(lambda: radioButton(timePRB, tsw, tuw, tpw, rWindow))

    #####tabbing setup
    timeSRB.setFocusPolicy(Qt.ClickFocus)
    timeURB.setFocusPolicy(Qt.ClickFocus)
    timePRB.setFocusPolicy(Qt.ClickFocus)

####creates the Weight GUI portion of the application
def setupWeight(rWindow, midLO):
    logDebug("gui.py::setupWeight() called\n")
                
    weightContainer = QVBoxLayout()
    weightContainer.setContentsMargins(5,5,5,5)
    midLO.addLayout(weightContainer)

    h1 = QHBoxLayout()
    h1.setContentsMargins(0,0,0,0)
    modLabel = newLabel(h1, "Module:")
    weightPicker = newComboBox(h1, ["I-Step", "Synaptic Input", "Custom"], "Weight Picker")
    h1.addStretch(1)
    clearButton = newButton(h1, "Clear List")
    clearButton.clicked.connect(lambda: clearButtonClicked(gv.weightInputs, gv.model, ['Module', 'Name', 'Weight'], 1, gv.wTable))

    weightContainer.addLayout(h1)
    
    leSize = 50
    ###################Synaptic Input################# 
    weightBox = QWidget()
    weightLO = QVBoxLayout(weightBox)
    weightLO.setContentsMargins(0,0,0,0)
    weightBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    weightBox.hide()
    
    hw1 = QHBoxLayout()
    hw1.setContentsMargins(0,0,0,0)
    weightLO.addLayout(hw1)
    wNameLabel = newLabel(hw1, "Name:")
    wNameLabel.setMaximumWidth(40)
    wNameLE = newLineEdit(hw1,"Weight Name")
    wNameLE.setMaximumWidth(80)
    hw1.setAlignment(wNameLE, Qt.AlignLeft)
    
    wSinw = QWidget()
    wSinw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    wUniw = QWidget()
    wUniw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    wUniw.hide()
    wPosw = QWidget()
    wPosw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    wPosw.hide()

    hw1.addStretch(1)
    hw1.addWidget(wSinw)
    hw1.addWidget(wUniw)
    hw1.addWidget(wPosw)
    hw1.setAlignment(wSinw, Qt.AlignRight)
    hw1.setAlignment(wUniw, Qt.AlignRight)
    hw1.setAlignment(wUniw, Qt.AlignRight)
    
    wSinLO = QHBoxLayout(wSinw)
    wSinLO.setContentsMargins(0,0,0,0)
    wSinLO.addStretch(1)
    ampLabel = newLabel(wSinLO, "Weight(uS): ")
    ampSingleLE = newLineEdit(wSinLO, 'Single Weight', newDVal(10,0))
    ampSingleLE.setMaximumWidth(leSize)
    wSinLO.setAlignment(ampSingleLE, Qt.AlignRight)
    wSinLO.setAlignment(ampLabel, Qt.AlignRight)

    wUniLO = QHBoxLayout(wUniw)
    wUniLO.setContentsMargins(0,0,0,0)
    ampUMinLabel = newLabel(wUniLO, "Mean(uS): ")
    ampUMinLE = newLineEdit(wUniLO, 'amp Uni Mean', newDVal(10, 0))
    ampUMinLE.setMaximumWidth(leSize)
    ampUMaxLabel = newLabel(wUniLO, "S.D.: ")
    ampUMaxLE = newLineEdit(wUniLO, 'amp Uni SD', newDVal(10,0))
    ampUMaxLE.setMaximumWidth(leSize)
    wUniLO.setAlignment(ampUMinLabel, Qt.AlignRight)
    wUniLO.setAlignment(ampUMinLE, Qt.AlignRight)
    wUniLO.setAlignment(ampUMaxLabel, Qt.AlignRight)
    wUniLO.setAlignment(ampUMaxLE, Qt.AlignRight)
    
    wPosLO = QHBoxLayout(wPosw)
    wPosLO.setContentsMargins(0,0,0,0)
    ampPMeanLabel = newLabel(wPosLO, "Mean(uS): ")
    ampPMeanLE = newLineEdit(wPosLO, 'ampMean', newDVal(10,0))
    ampPMeanLE.setMaximumWidth(leSize)
    ampPSDLabel = newLabel(wPosLO, "S.D.: ")
    ampPSDLE = newLineEdit(wPosLO, 'ampSD', newDVal(10, 0))
    ampPSDLE.setMaximumWidth(leSize)
    wPosLO.setAlignment(ampPMeanLabel, Qt.AlignRight)
    wPosLO.setAlignment(ampPMeanLE, Qt.AlignRight)
    wPosLO.setAlignment(ampPSDLabel, Qt.AlignRight)
    wPosLO.setAlignment(ampPSDLE, Qt.AlignRight)
    
    
    hw2 = QHBoxLayout()
    hw2.setContentsMargins(0,5,0,4)
    weightLO.addLayout(hw2)
    
    weightLabel = newLabel(hw2, "Weight:")

    hw3 = QHBoxLayout()
    hw3.setContentsMargins(0,0,0,0)
    weightLO.addLayout(hw3)
    hw4 = QHBoxLayout()
    hw4.setContentsMargins(0,0,0,0)
    weightLO.addLayout(hw4)
    hw5 = QHBoxLayout()
    hw5.setContentsMargins(0,0,0,0)
    weightLO.addLayout(hw5)
    ampSRB = newRadioButton(hw3, "Single", True, "ampSingle")
    ampURB = newRadioButton(hw4, "Multiple Uniform", False, "ampMult")
    ampPRB = newRadioButton(hw5, "Multiple Poisson", False, "ampPos")
    ampDisBG = newButtonGroup(rWindow, [ampSRB, ampURB, ampPRB], "ampDisBG")

    hw3.addStretch(1)
    hw4.addStretch(1)
    hw5.addStretch(1)
    
    eLabel = newLabel(hw3, "E(mV): ")
    tau1Label = newLabel(hw4, "Tau1(ms): ")
    tau2Label = newLabel(hw5, "Tau2(ms): ")
    eLineEdit = newLineEdit(hw3, 'E', newDVal(10))
    tau1LineEdit = newLineEdit(hw4,'Tau1', newDVal(10))
    tau2LineEdit = newLineEdit(hw5,'Tau2', newDVal(10))
    eLineEdit.setMaximumWidth(leSize)
    hw3.setAlignment(eLabel, Qt.AlignRight)
    hw3.setAlignment(eLineEdit, Qt.AlignRight)
    tau1LineEdit.setMaximumWidth(leSize)
    hw4.setAlignment(tau1Label, Qt.AlignRight)
    hw4.setAlignment(tau1LineEdit, Qt.AlignRight)
    tau2LineEdit.setMaximumWidth(leSize)
    hw5.setAlignment(tau2Label, Qt.AlignRight)
    hw5.setAlignment(tau2LineEdit, Qt.AlignRight)

    
    weightContainer.addWidget(weightBox)

    ##################### I-Step setup ################ 
    curBox = QWidget()
    curLO = QVBoxLayout(curBox)
    curLO.setContentsMargins(0,0,0,0)
    curBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


    hc1 = QHBoxLayout()
    curLO.addLayout(hc1)    
    cNameLabel = newLabel(hc1, "Name:")
    cNameLE = newLineEdit(hc1,"Current Name")
    hc1.setContentsMargins(0,0,0,0)
    cNameLabel.setMaximumWidth(40)
    cNameLE.setMaximumWidth(80)
    hc1.setAlignment(cNameLE, Qt.AlignLeft)

    
    cSinw = QWidget()
    cSinw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    cUniw = QWidget()
    cUniw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    cUniw.hide()
    cPosw = QWidget()
    cPosw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    cPosw.hide()

    hc1.addStretch(1)
    hc1.addWidget(cSinw)
    hc1.addWidget(cUniw)
    hc1.addWidget(cPosw)
    hc1.setAlignment(wSinw, Qt.AlignRight)
    hc1.setAlignment(wUniw, Qt.AlignRight)
    hc1.setAlignment(wUniw, Qt.AlignRight)

    cSinLO = QHBoxLayout(cSinw)
    cSinLO.setContentsMargins(0,0,0,0)
    cSinLO.addStretch(1)
    curLabel = newLabel(cSinLO, "Current(nA): ")
    curSingleLE = newLineEdit(cSinLO, 'Single Current', newDVal(10))
    curSingleLE.setMaximumWidth(leSize)
    cSinLO.setAlignment(curSingleLE, Qt.AlignRight)
    cSinLO.setAlignment(curLabel, Qt.AlignRight)

    cUniLO = QHBoxLayout(cUniw)
    cUniLO.setContentsMargins(0,0,0,0)
    curUMinLabel = newLabel(cUniLO, "Mean(nA): ") 
    curUMinLE = newLineEdit(cUniLO, 'cur Uni Mean', newDVal(10, 0))
    curUMinLE.setMaximumWidth(leSize)
    curUMaxLabel = newLabel(cUniLO, "S.D.: ")
    curUMaxLE = newLineEdit(cUniLO, 'cur Uni SD', newDVal(10,0))
    curUMaxLE.setMaximumWidth(leSize)
    cUniLO.setAlignment(curUMinLabel, Qt.AlignRight)
    cUniLO.setAlignment(curUMinLE, Qt.AlignRight)
    cUniLO.setAlignment(curUMaxLabel, Qt.AlignRight)
    cUniLO.setAlignment(curUMaxLE, Qt.AlignRight)
    
    
    cPosLO = QHBoxLayout(cPosw)
    cPosLO.setContentsMargins(0,0,0,0)
    curPMeanLabel = newLabel(cPosLO, "Mean(nA): ")
    curPMeanLE = newLineEdit(cPosLO, 'curMean', newDVal(10,0))
    curPMeanLE.setMaximumWidth(leSize)
    curPSDLabel = newLabel(cPosLO, "S.D.: ")
    curPSDLE = newLineEdit(cPosLO, 'curSD', newDVal(10, 0))
    curPSDLE.setMaximumWidth(leSize)
    cPosLO.setAlignment(curPMeanLabel, Qt.AlignRight)
    cPosLO.setAlignment(curPMeanLE, Qt.AlignRight)
    cPosLO.setAlignment(curPSDLabel, Qt.AlignRight)
    cPosLO.setAlignment(curPSDLE, Qt.AlignRight)


    hc2 = QHBoxLayout()
    hc2.setContentsMargins(0,5,0,6)
    curLabel = newLabel(hc2, "Current:")
    curLO.addLayout(hc2)
    
    hc3 = QHBoxLayout()
    hc3.setContentsMargins(0,0,0,0)
    curLO.addLayout(hc3)
    hc4 = QHBoxLayout()
    hc4.setContentsMargins(0,0,0,0)
    curLO.addLayout(hc4)
    hc5 = QHBoxLayout()
    hc5.setContentsMargins(0,0,0,0)
    curLO.addLayout(hc5)
    
    
    curSRB = newRadioButton(hc3, "Single", True, "curSingle")
    curURB = newRadioButton(hc4, "Multiple Uniform", False, "curMult")
    curPRB = newRadioButton(hc5, "Multiple Poisson", False, "curPos")
    curDisBG = newButtonGroup(rWindow, [curSRB, curURB, curPRB], "curDisBG")

    durLabel = newLabel(hc3, "Duration(ms): ")
    hc3.setAlignment(durLabel, Qt.AlignRight)
    durPicker = newComboBox(hc4, ['Single', 'Uniform', 'Poisson'], 'Duration Picker')
    hc4.setAlignment(durPicker, Qt.AlignRight)
    
    dSinw = QWidget()
    dSinw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    dUniw = QWidget()
    dUniw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    dPosw = QWidget()
    dPosw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    dUniw.hide()
    dPosw.hide()
    hc5.addWidget(dSinw)
    hc5.addWidget(dUniw)
    hc5.addWidget(dPosw)
    hc5.setAlignment(dSinw, Qt.AlignRight)
    hc5.setAlignment(dUniw, Qt.AlignRight)
    hc5.setAlignment(dPosw, Qt.AlignRight)
    
    dSinLO = QHBoxLayout(dSinw)
    dSinLO.setContentsMargins(0,0,0,0)
    durLineEdit = newLineEdit(dSinLO, 'Duration', newDVal(10))
    durLineEdit.setMaximumWidth(leSize)
    dSinLO.setAlignment(durLineEdit, Qt.AlignRight)
    
    dUniLO = QHBoxLayout(dUniw)
    dUniLO.setContentsMargins(0,0,0,0)
    durUMeanLabel = newLabel(dUniLO, 'Mean: ')
    durUMeanLE = newLineEdit(dUniLO, 'Duration Uniform Mean', newDVal(10))
    durUMeanLE.setMaximumWidth(leSize)
    dUniLO.setAlignment(durUMeanLabel, Qt.AlignRight)
    dUniLO.setAlignment(durUMeanLE, Qt.AlignRight)
    durUSDLabel = newLabel(dUniLO, 'S.D.: ')
    durUSDLE = newLineEdit(dUniLO, "Duration Uniform SD", newDVal(10))
    durUSDLE.setMaximumWidth(leSize)
    dUniLO.setAlignment(durUSDLabel, Qt.AlignRight)
    dUniLO.setAlignment(durUSDLE, Qt.AlignRight)

    dPosLO = QHBoxLayout(dPosw)
    dPosLO.setContentsMargins(0,0,0,0)
    durPMeanLabel = newLabel(dPosLO, 'Mean: ')
    durPMeanLE = newLineEdit(dPosLO, 'Duration Poisson Mean', newDVal(10))
    durPMeanLE.setMaximumWidth(leSize)
    dPosLO.setAlignment(durPMeanLabel, Qt.AlignRight)
    dPosLO.setAlignment(durPMeanLE, Qt.AlignRight)
    durPSDLabel = newLabel(dPosLO, 'S.D.: ')
    durPSDLE = newLineEdit(dPosLO, "Duration Poisson SD", newDVal(10))
    durPSDLE.setMaximumWidth(leSize)
    dPosLO.setAlignment(durPSDLabel, Qt.AlignRight)
    dPosLO.setAlignment(durPSDLE, Qt.AlignRight)

    durPicker.currentIndexChanged.connect(lambda: weightSelect(durPicker, [dSinw, dUniw, dPosw], rWindow))

    weightContainer.addWidget(curBox)

    ##############CUSTOM WEIGHT###############                                                        

    custBox = QWidget()
    custLO = QVBoxLayout(custBox)
    custLO.setContentsMargins(0,0,0,0)
    custBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    custBox.hide()
    hm1 = QHBoxLayout()
    hm1.setContentsMargins(0,0,0,0)
    modFileButton = newButton(hm1, ".mod File")
    modFile_le = newLineEdit(hm1, 'ModFile')
    modFileButton.clicked.connect(lambda: fileSelect(modFileButton, modFile_le, "MOD (*.mod)"))
    custLO.addLayout(hm1)

    hm2 = QHBoxLayout()
    hm2.setContentsMargins(0,5,0,2)

    customLabel = newLabel(hm2, "Custom:")
    
    mSinw = QWidget()
    mSinw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    mUniw = QWidget()
    mUniw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    mUniw.hide()
    mPosw = QWidget()
    mPosw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    mPosw.hide()
    hm2.addStretch(1)
    hm2.addWidget(mSinw)
    hm2.addWidget(mUniw)
    hm2.addWidget(mPosw)
    custLO.addLayout(hm2)
    
    mSinLO = QHBoxLayout(mSinw)
    mSinLO.setContentsMargins(0,0,0,0)
    custLabel = newLabel(mSinLO, "Weight(uS): ")
    custSingleLE = newLineEdit(mSinLO, 'Single Custom', newDVal(10,0))
    custSingleLE.setMaximumWidth(leSize)
    mSinLO.setAlignment(custSingleLE, Qt.AlignRight)
    mSinLO.setAlignment(custLabel, Qt.AlignRight)

    mUniLO = QHBoxLayout(mUniw)
    mUniLO.setContentsMargins(0,0,0,0)
    custUMinLabel = newLabel(mUniLO, "Mean(uS): ")
    custUMinLE = newLineEdit(mUniLO, 'cust Uni Mean', newDVal(10, 0))
    custUMinLE.setMaximumWidth(leSize)
    custUMaxLabel = newLabel(mUniLO, "S.D.: ")
    custUMaxLE = newLineEdit(mUniLO, 'cust Uni SD', newDVal(10,0))
    custUMaxLE.setMaximumWidth(leSize)
    mUniLO.setAlignment(custUMinLabel, Qt.AlignRight)
    mUniLO.setAlignment(custUMinLE, Qt.AlignRight)
    mUniLO.setAlignment(custUMaxLabel, Qt.AlignRight)
    mUniLO.setAlignment(custUMaxLE, Qt.AlignRight)

        
    mPosLO = QHBoxLayout(mPosw)
    mPosLO.setContentsMargins(0,0,0,0)
    custPMeanLabel = newLabel(mPosLO, "Mean(uS): ")
    custPMeanLE = newLineEdit(mPosLO, 'custMean', newDVal(10,0))
    custPMeanLE.setMaximumWidth(leSize)
    custPSDLabel = newLabel(mPosLO, "S.D.: ")
    custPSDLE = newLineEdit(mPosLO, 'custSD', newDVal(10, 0))
    custPSDLE.setMaximumWidth(leSize)
    mPosLO.setAlignment(custPMeanLabel, Qt.AlignRight)
    mPosLO.setAlignment(custPMeanLE, Qt.AlignRight)
    mPosLO.setAlignment(custPSDLabel, Qt.AlignRight)
    mPosLO.setAlignment(custPSDLE, Qt.AlignRight)

    hm3 = QHBoxLayout()
    hm3.setContentsMargins(0,0,0,0)
    hm4 = QHBoxLayout()
    hm4.setContentsMargins(0,0,0,0)
    hm5 = QHBoxLayout()
    hm5.setContentsMargins(0,0,0,0)
    custLO.addLayout(hm3)
    custLO.addLayout(hm4)
    custLO.addLayout(hm5)
    
    custSRB = newRadioButton(hm3, "Single", True, "custSingle")
    custURB = newRadioButton(hm4, "Multiple Uniform", False, "custMult")
    custPRB = newRadioButton(hm5, "Multiple Poisson", False, "custPos")
    custDisBG = newButtonGroup(rWindow, [custSRB, custURB, custPRB], "custDisBG")

    weightContainer.addWidget(custBox)
    
    ###########
    
    h2 = QHBoxLayout()
    h2.setContentsMargins(0,0,0,0)
    addInputButton = newButton(h2, "Save")
    delInputButton = newButton(h2, "Delete")
    h2.addStretch(1)
    
    weightContainer.addLayout(h2)

    gv.wTable = newTableView(weightContainer, "Weight Table")
    gv.wTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    gv.wTable.setAlternatingRowColors(True)
    gv.model = QStandardItemModel()
    gv.wTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    gv.model.setHorizontalHeaderLabels(['Module', 'Name', 'Weight'])
    gv.wTable.setModel(gv.model)

    #################HANDLER FUNCTIONS###############
    
    addInputButton.clicked.connect(lambda: saveButtonClicked(rWindow))
    delInputButton.clicked.connect(lambda: deleteButtonClicked(gv.wTable, gv.weightInputs, gv.model))
    gv.wTable.clicked.connect(lambda: editButtonClicked(rWindow, gv.wTable))
    
    ampSRB.toggled.connect(lambda: radioButton(ampSRB, wSinw, wUniw, wPosw, rWindow))
    ampURB.toggled.connect(lambda: radioButton(ampURB, wSinw, wUniw, wPosw, rWindow))
    ampPRB.toggled.connect(lambda: radioButton(ampPRB, wSinw, wUniw, wPosw, rWindow))
    curSRB.toggled.connect(lambda: radioButton(curSRB, cSinw, cUniw, cPosw, rWindow))
    curURB.toggled.connect(lambda: radioButton(curURB, cSinw, cUniw, cPosw, rWindow))
    curPRB.toggled.connect(lambda: radioButton(curPRB, cSinw, cUniw, cPosw, rWindow))
    custSRB.toggled.connect(lambda: radioButton(custSRB, mSinw, mUniw, mPosw, rWindow))
    custURB.toggled.connect(lambda: radioButton(custURB, mSinw, mUniw, mPosw, rWindow))
    custPRB.toggled.connect(lambda: radioButton(custPRB, mSinw, mUniw, mPosw, rWindow))

    weightPicker.currentIndexChanged.connect(lambda: weightSelect(weightPicker, [curBox, weightBox, custBox], rWindow))

    #####tabbing setup
    ampSRB.setFocusPolicy(Qt.ClickFocus)
    ampURB.setFocusPolicy(Qt.ClickFocus)
    ampPRB.setFocusPolicy(Qt.ClickFocus)
    curSRB.setFocusPolicy(Qt.ClickFocus)
    curURB.setFocusPolicy(Qt.ClickFocus)
    curPRB.setFocusPolicy(Qt.ClickFocus)
    custSRB.setFocusPolicy(Qt.ClickFocus)
    custURB.setFocusPolicy(Qt.ClickFocus)
    custPRB.setFocusPolicy(Qt.ClickFocus)
    weightPicker.setFocusPolicy(Qt.ClickFocus)
    durPicker.setFocusPolicy(Qt.ClickFocus)
    addInputButton.setFocusPolicy(Qt.ClickFocus)
    delInputButton.setFocusPolicy(Qt.ClickFocus)
    clearButton.setFocusPolicy(Qt.ClickFocus)
    gv.wTable.setFocusPolicy(Qt.ClickFocus)
    modFileButton.setFocusPolicy(Qt.ClickFocus)

####creates the Experiment GUI portion of the application
def setupInputControl(w, rightLO):
    logDebug("gui.py::setupInputControl() called\n")
                
    aWindow = QVBoxLayout()
    aWindow.setContentsMargins(5,5,5,5)
    rightLO.addLayout(aWindow)

    h1 = QHBoxLayout()
    h1.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h1)
    h2 = QHBoxLayout()
    h2.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h2)
    h3 = QHBoxLayout()
    h3.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h3)
    h4 = QHBoxLayout()
    h4.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h4)
    h5 = QHBoxLayout()
    h5.setContentsMargins(0,0,0,5)
    aWindow.addLayout(h5)
    h6 = QHBoxLayout()
    h6.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h6)
    h7 = QHBoxLayout()
    h7.setContentsMargins(0,0,0,0)
    aWindow.addLayout(h7)
    
    
    gv.inputTable = newTableView(aWindow, "Input Table")
    gv.inputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    gv.inputTable.setAlternatingRowColors(True)
    gv.allModel = QStandardItemModel()
    gv.inputTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    gv.allModel.setHorizontalHeaderLabels(['Tag', 'Num. Inputs', 'Color'])
    gv.inputTable.setModel(gv.allModel)

    h1.addStretch(1)
    clearButton = newButton(h1, "Clear List")
    h1.setAlignment(clearButton, Qt.AlignRight)
    clearButton.clicked.connect(lambda: clearButtonClicked(gv.experiments, gv.allModel, ['ID', '# of Points', 'Color'], 0, gv.inputTable))
    
    exNameLabel = newLabel(h2, "Tag:")
    exNameLE = newLineEdit(h2, "Experiment Name")
    exNameLE.setMaximumWidth(150)
    h2.addStretch(1)
    
    addInputButton = newButton(h7, "Save")
    delInputButton = newButton(h7, "Delete")
    h7.addStretch(1)

    locLimitsLabel = newLabel(h4, "Location Limits:")
    h4.addStretch(1)
    colorButton = newButton(h4, "Color")
    colorButton.clicked.connect(colorPicker)
    h4.setAlignment(colorButton, Qt.AlignRight)
    
    segLabel = newLabel(h3, "Number of Inputs: ")
    segLineEdit = newLineEdit(h3, "Inputs", QIntValidator())
    segLineEdit.validator().setBottom(0)
    segLineEdit.setMaximumWidth(80)
    h3.addStretch(1)
    
    somaCB = newCheckBox(h5, "Soma", True, "somaCB")
    apicalCB = newCheckBox(h6, "Apical Dendrite", True, "apicalCB")
    basalCB = newCheckBox(h5, "Basal Dendrite", True, "basalCB")
    axonCB = newCheckBox(h6, "Axon", True, "axonCB")
    h5.addStretch(1)
    h6.addStretch(1)
    
    addInputButton.clicked.connect(lambda: allSaveButtonClicked(w))
    delInputButton.clicked.connect(lambda: deleteButtonClicked(gv.inputTable, gv.experiments, gv.allModel))
    gv.inputTable.clicked.connect(lambda: editInputButtonClicked(w, gv.inputTable))

    ####tabbing setup
    addInputButton.setFocusPolicy(Qt.ClickFocus)
    delInputButton.setFocusPolicy(Qt.ClickFocus)
    somaCB.setFocusPolicy(Qt.ClickFocus)
    apicalCB.setFocusPolicy(Qt.ClickFocus)
    basalCB.setFocusPolicy(Qt.ClickFocus)
    axonCB.setFocusPolicy(Qt.ClickFocus)
    colorButton.setFocusPolicy(Qt.ClickFocus)
    clearButton.setFocusPolicy(Qt.ClickFocus)
    gv.inputTable.setFocusPolicy(Qt.ClickFocus)
