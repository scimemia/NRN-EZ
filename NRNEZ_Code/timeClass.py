###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This file contains the class definition for the Time object
#### Author: Evan Cobb
####
###################################################################
 
import sys
import globvar as gv
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from errorLogger import	*
import random

class timeObject:
    def __init__(self, func, onset, interval=None, mean=None, sd=None):
        logDebug("timeClass.py::init() called.\n")
        self.func = func ##0 - Single, 1 - Multiple, 2 - Poisson 
        self.onset = onset
        self.interval = interval
        self.mean = mean
        self.sd = sd
        self.err = ""

        if(onset == ""):
            self.err = "Please enter a Time of Onset before saving!"
        if(interval == ""):
            self.err = "Please enter an Interval before saving!"
        if(mean == "" or sd == ""):
            self.err = "Please enter a Mean and S.D. for Time before saving!"

    ##clear UI elements 
    def clearElements(self):
        logDebug("timeClass.py::clearElements() called.\n")
        self.onsetUI = None
        self.funcUI = None
        self.intervalUI = None
        self.meanUI = None
        self.sdUI = None

    
    ###holds the GUI elements references in one place 
    def setElements(self, parent):
        logDebug("timeClass.py::setElements() called.\n")
        self.onsetUI = parent.findChild(QLineEdit, "Time of Onset")
        if(self.func == 0): ##Single
            self.funcUI = parent.findChild(QRadioButton, "timeSingle")
            self.intervalUI = parent.findChild(QLineEdit, "Interval")
            self.meanUI = None
            self.sdUI = None
        elif(self.func == 1): ##Uniform
            self.funcUI = parent.findChild(QRadioButton, "timeMult")
            self.intervalUI = None
            self.meanUI = parent.findChild(QLineEdit, "Interval M Mean")
            self.sdUI = parent.findChild(QLineEdit, "Interval M SD")
        else: ##Poisson
            self.funcUI	= parent.findChild(QRadioButton, "timePos")
            self.intervalUI = None
            self.meanUI	= parent.findChild(QLineEdit, "Interval Mean")
            self.sdUI =	parent.findChild(QLineEdit, "Interval SD")

    ##set values in the GUI for the edit mode
    def editGUI(self):
        logDebug("timeClass.py::editGUI() called.\n")
        self.onsetUI.setText(self.onset)
        self.funcUI.setChecked(True)
        if(self.intervalUI is not None):
            self.intervalUI.setText(self.interval)
        if(self.meanUI is not None):
            self.meanUI.setText(self.mean)
        if(self.sdUI is not None):
            self.sdUI.setText(self.sd)

    ##generates time data based on user inputs
    def generate(self, path, inputs):
        logDebug("timeClass.py::generate() called.\n")
        try:
            fout = open(path + "/syn_time.dat", "w")
            buf = ""
            if(self.func == 0): ##Single
                buf = self.genTimeSingle(inputs, 1, float(self.interval), float(self.onset))
            elif(self.func == 1): ##Uniform
                minVal = float(self.mean) - float(self.sd) 
                maxVal = float(self.mean) + float(self.sd)
                ranNums = []
                for x in range(0, inputs):
                    ranNums.append(random.uniform(minVal, maxVal))
                buf = self.genTimeDis(inputs, 1, ranNums, float(self.onset))
            elif(self.func == 2): ##Poisson
                ranNums = []
                for x in range(0, inputs):
                    ranNums.append(self.genRanPD(float(self.mean), float(self.sd)))
                buf = self.genTimeDis(inputs, 1, ranNums, float(self.onset))
            else:
                self.err = "Error generating time data"
            fout.write(buf)
        except Exception as ex:
            newMsgBox("Error generating Time data", str(ex))
            logErr(str(ex), "timeClass::generate")
        finally:
            fout.close()

    ##generates single data for Time class
    def genTimeSingle(self, inputs, col, interval, onset):
        logDebug("timeClass.py::genTimeSingle() called. Interval:: " + str(interval) +" --Onset:: "+ str(onset) +"\n")

        buf = str(inputs) + ' ' + str(col) + '\n'
        for x in range(0, inputs):
            buf = buf + str((x * interval) + onset) + '\n'
        return buf

    ##generates Uniform and Poisson data for Time class
    def genTimeDis(self, inputs, col, interval, onset):
        logDebug("timeClass.py::genTimeDis() called. Interval:: " + str(interval) +" --Onset:: "+ str(onset) +"\n")
        buf = str(inputs) + ' ' + str(col) + '\n'

        prev = onset + interval[0]
        buf = buf + str(prev) + '\n'
        for x in range(1, inputs):
            prev = prev + interval[x]
            buf = buf + str(prev) + '\n'
        return buf

    ###takes a mean and standard deviation and returns a random, POSITIVE number based on a normal distribution  
    def genRanPD(self, mean, sd):
        ran = random.normalvariate(mean, sd)
        while(ran < 0):
            ran = random.normalvariate(mean, sd)
        logDebug("timeClass.py::genRanPD() called. --Mean: " + str(mean) + " --S.D.: " + str(sd) + " --Return Val: " + str(ran) + "\n")
        return ran
