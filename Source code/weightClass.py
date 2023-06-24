###################################################################
####
#### Version: 1.1.7
#### Date: 6/24/2023
#### Description: This file contains the class definitions for the i-step, synaptic and custom weight objects
#### Author: Evan Cobb
####
###################################################################
 
import sys
import globvar as gv
import math
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from errorLogger import	*

####Weight Class contains general functions used by all the subclasses.
class Weight:
    def __init__(self, parent):
        logDebug("weightClass.py::init() called.\n")
        self.weightPicker = parent.findChild(QComboBox, "Weight Picker")
    
    def getFunc(self):
        logDebug("weightClass.py::getFunc() called.\n")
        if(self.func == 0):
            return "Single"
        elif(self.func == 1):
            return "Uniform"
        else:
            return "Poisson"

    ###takes a mean and standard deviation and returns a random, POSITIVE number based on a normal distribution
    def genRanPD(self, mean, sd):
        ran = random.normalvariate(mean, sd)
        while(ran < 0):
            ran = random.normalvariate(mean, sd)
        logDebug("weightClass.py::genRanPD() called. --Mean: " + str(mean) + " --S.D.: "+ str(sd) + " --Return Val: " + str(ran) + "\n")
        return ran

    ##generates weight data
    def generate(self, inputs):
        logDebug("weightClass.py::generate() called.\n")
        buf = []
        if(self.func == 0):
            for _ in range(0, inputs):
                    buf.append(self.weight)
        elif(self.func == 1):
            for _ in range(0, inputs):
                buf.append(random.uniform(float(self.mean) - float(self.sd), float(self.mean) + float(self.sd)))
        elif(self.func == 2):
            for _ in range(0, inputs):
                buf.append(self.genRanPD(float(self.mean), float(self.sd)))
        else:
            self.err = "An error occured while generating weight data"
        return buf


###############################################################################
###### SYNAPTIC INPUT WEIGHT CLASS ########################
###############################################################################
    
class synInput(Weight):
    type = "Syn-Input"
    def  __init__(self, func, name, e, tau1, tau2, parent, weight=None, mean=None, sd=None):
        logDebug("weightClass.py::synInput::init() called.\n")
        super().__init__(parent)
        self.func = func ## 0 - Single, 1 - Uniform, 2 - Poisson
        self.name = name
        self.e = e
        self.tau1 = tau1
        self.tau2 = tau2
        self.weight = weight
        self.mean = mean
        self.sd = sd
        self.err = ""

        if(self.name == ""):
            self.err = "Please enter a Name before saving!"
        if(self.e == "" or self.tau1 == "" or self.tau2 == ""):
            self.err = "Please fill out the E, Tau1, and Tau2 before saving!"
        if(self.weight == ""):
            self.err = "Please enter a Weight before saving!"
        if(self.mean == "" or self.sd == ""):
            self.err = "Please enter a Mean and S.D. for Synaptic Input before saving!"

    ##clears UI elements
    def clearElements(self):
        logDebug("weightClass.py::synInput::clearElements() called.\n")
        self.nameUI = None
        self.eUI = None
        self.tau1UI = None
        self.tau2UI = None
        self.funcUI = None
        self.weightUI = None
        self.meanUI = None
        self.sdUI = None
        self.weightPicker = None

    ##set UI elements 
    def setElements(self, parent):
        logDebug("weightClass.py::synInput::setElements() called.\n")
        self.weightPicker = parent.findChild(QComboBox, "Weight Picker")
        self.nameUI = parent.findChild(QLineEdit, "Weight Name")
        self.eUI = parent.findChild(QLineEdit, "E")
        self.tau1UI = parent.findChild(QLineEdit, "Tau1")
        self.tau2UI = parent.findChild(QLineEdit, "Tau2")

        if(self.func == 0):
            self.funcUI = parent.findChild(QRadioButton, "ampSingle")
            self.weightUI = parent.findChild(QLineEdit, "Single Weight")
            self.meanUI = None
            self.sdUI = None
        elif(self.func == 1):
            self.funcUI = parent.findChild(QRadioButton, "ampMult")
            self.weightUI = None
            self.meanUI = parent.findChild(QLineEdit, "amp Uni Mean")
            self.sdUI = parent.findChild(QLineEdit, "amp Uni SD")
        else:
            self.funcUI = parent.findChild(QRadioButton, "ampPos")
            self.weightUI = None
            self.meanUI = parent.findChild(QLineEdit, "ampMean")
            self.sdUI = parent.findChild(QLineEdit, "ampSD")

    ##set values in the GUI for editting
    def editGUI(self):
        logDebug("weightClass.py::synInput::editGUI() called.\n")
        self.weightPicker.setCurrentIndex(1)
        self.nameUI.setText(self.name)
        self.eUI.setText(self.e)
        self.tau1UI.setText(self.tau1)
        self.tau2UI.setText(self.tau2)
        self.funcUI.setChecked(True)
        if(self.weightUI is not None):
            self.weightUI.setText(self.weight)
        if(self.meanUI is not None):
            self.meanUI.setText(self.mean)
        if(self.sdUI is not None):
            self.sdUI.setText(self.sd)

#########################################################################
#########CURRENT CLASS##############
#######################################################################3
class curInput(Weight):
    type = "I-Step"
    def __init__(self, func, name, dur, parent, cur=None, mean=None, sd=None, durMean = None, durSD = None, durType = 0):
        logDebug("weightClass.py::curInput::init() called.\n")
        super().__init__(parent)
        self.func = func
        self.name = name
        self.duration = dur
        self.weight = cur  #####this is really current
        self.mean = mean
        self.sd = sd
        self.durMean = durMean
        self.durSD = durSD
        self.durType = durType ## 0 = Single, 1 = Uniform, 2 = Poisson
        self.err = ""
        
        if(self.name == ""):
            self.err = "Please enter a Name before saving!"
        if(self.duration == "" ):
            self.err = "Please enter a Duration before saving!"
        if(self.weight == ""):
            self.err = "Please enter a Current before saving!"
        if(self.mean == "" or self.sd == ""):
            self.err = "Please enter a Mean and S.D. for I-Step before saving!"
        if(self.durMean == "" or self.durSD == ""):
            self.err = "Please enter a Mean and S.D. for Duration before saving!"
            
    ##clear UI elements
    def clearElements(self):
        logDebug("weightClass.py::curInput::clearElements() called.\n")
        self.nameUI = None
        self.durationUI = None
        self.durMeanUI = None
        self.durSDUI = None
        self.funcUI = None
        self.currentUI = None
        self.meanUI = None
        self.sdUI = None
        self.weightPicker = None
        self.durPicker = None

    ##set UI elements
    def setElements(self, parent):
        logDebug("weightClass.py::curInput::setElements() called.\n")
        self.weightPicker = parent.findChild(QComboBox, "Weight Picker")
        self.durPicker = parent.findChild(QComboBox, "Duration Picker")
        self.nameUI = parent.findChild(QLineEdit, "Current Name")
        if(self.durType == 0):
            self.durationUI = parent.findChild(QLineEdit, "Duration")
            self.durMeanUI = None
            self.durSDUI = None
        elif(self.durType == 1):
            self.durationUI = None
            self.durMeanUI = parent.findChild(QLineEdit, "Duration Uniform Mean")
            self.durSDUI = parent.findChild(QLineEdit, "Duration Uniform SD")
        else:
            self.durationUI = None
            self.durMeanUI = parent.findChild(QLineEdit, "Duration Poisson Mean")
            self.durSDUI = parent.findChild(QLineEdit, "Duration Poisson SD")
        if(self.func == 0):
            self.funcUI = parent.findChild(QRadioButton, "curSingle")
            self.currentUI = parent.findChild(QLineEdit, "Single Current")
            self.meanUI = None
            self.sdUI = None
        elif(self.func == 1):
            self.funcUI = parent.findChild(QRadioButton, "curMult")
            self.currentUI = None
            self.meanUI = parent.findChild(QLineEdit, "cur Uni Mean")
            self.sdUI = parent.findChild(QLineEdit, "cur Uni SD")
        else:
            self.funcUI = parent.findChild(QRadioButton, "curPos")
            self.currentUI = None
            self.meanUI = parent.findChild(QLineEdit, "curMean")
            self.sdUI = parent.findChild(QLineEdit, "curSD")
            

    ##set values in the GUI for editting
    def editGUI(self):
        logDebug("weightClass.py::curInput::editGUI() called.\n")
        self.weightPicker.setCurrentIndex(0)
        self.durPicker.setCurrentIndex(self.durType)
        self.nameUI.setText(self.name)
        if(self.durationUI is not None):
            self.durationUI.setText(self.duration)
        if(self.durMeanUI is not None):
            self.durMeanUI.setText(self.durMean)
        if(self.durSDUI is not None):
            self.durSDUI.setText(self.durSD)
        self.funcUI.setChecked(True)
        if(self.currentUI is not None):
            self.currentUI.setText(self.weight)
        if(self.meanUI is not None):
            self.meanUI.setText(self.mean)
        if(self.sdUI is not None):
            self.sdUI.setText(self.sd)

    def getDurationUniform(self):
        return random.uniform(float(self.durMean) - float(self.durSD), float(self.durMean\
) + float(self.durSD))

    def getDurationPoisson(self):
        return self.genRanPD(float(self.durMean), float(self.durSD))

######################################################################### 
#########CUSTOM CLASS############## 
#########################################################################
class custInput(Weight):
    type = "Custom"
    def __init__(self, func, path, parent, weight=None, mean=None, sd=None):
        logDebug("weightClass.py::custInput::init() called.\n")
        super().__init__(parent)
        self.func = func
        self.path = path
        self.name = path.split("/")[-1][:-4]
        self.weight = weight
        self.mean = mean
        self.sd = sd
        self.err = ""

        if(self.path == ""):
            self.err = "Please add a Mod File before saving!"
        if(self.weight == ""):
            self.err = "Please enter a Weight before saving!"
        if(self.mean == "" or self.sd == ""):
            self.err = "Please enter a Mean and S.D. for Custom Weight before saving!"
        for x in range(0, len(gv.weightInputs)):
            if(gv.editMode is not None):
                if(gv.editMode == x):
                    continue
            if(gv.weightInputs[x].type == 'Custom'):
                if(gv.weightInputs[x].name == self.name):
                    self.err =  'Error: Mod file ' + self.name + ' has already been used!'

    ##clear UI elements
    def clearElements(self):
        logDebug("weightClass.py::custInput::clearElements() called.\n")
        self.pathUI = None
        self.funcUI = None
        self.weightUI = None
        self.meanUI = None
        self.sdUI = None
        self.weightPicker = None

    ##set UI elements
    def setElements(self, parent):
        logDebug("weightClass.py::custInput::setElements() called.\n")
        self.weightPicker = parent.findChild(QComboBox, "Weight Picker")
        self.pathUI = parent.findChild(QLineEdit, "ModFile")
        if(self.func == 0):
            self.funcUI = parent.findChild(QRadioButton, "custSingle")
            self.weightUI = parent.findChild(QLineEdit, "Single Custom")
            self.meanUI = None
            self.sdUI = None
        elif(self.func == 1):
            self.funcUI = parent.findChild(QRadioButton, "custMult")
            self.weightUI = None
            self.meanUI = parent.findChild(QLineEdit, "cust Uni Mean")
            self.sdUI = parent.findChild(QLineEdit, "cust Uni SD")
        else:
            self.funcUI = parent.findChild(QRadioButton, "custPos")
            self.weightUI = None
            self.meanUI = parent.findChild(QLineEdit, "custMean")
            self.sdUI = parent.findChild(QLineEdit, "custSD")

    ##set values in the GUI for editting
    def editGUI(self):
        logDebug("weightClass.py::custInput::editGUI() called.\n")
        self.weightPicker.setCurrentIndex(2)
        self.pathUI.setText(self.path)
        self.funcUI.setChecked(True)
        if(self.weightUI is not None):
            self.weightUI.setText(self.weight)
        if(self.meanUI is not None):
            self.meanUI.setText(self.mean)
        if(self.sdUI is not None):
            self.sdUI.setText(self.sd)
