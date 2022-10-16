###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This file contains the class definition for the location object.
#### Author: Evan Cobb
####
###################################################################
 
import sys
import globvar as gv
import math
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from errorLogger import *


class locObject:
    def __init__(self, func, sec, secNum, distance = None, mean=None, sd=None):
        logDebug("locationClass.py::init() called.\n")
        self.func = func ##0 - Single, 1 - Multiple, 2 - Poisson
        self.sec = sec
        self.secNum = secNum
        self.distance = distance
        self.mean = mean
        self.sd = sd
        self.err = ""
        
        if(secNum == ""):
            self.err = "Please enter a value for Section Number before saving!"
        if(distance == ""):
            self.err = "Please enter a value for Distance before saving!"
        if(mean == "" or sd == ""):
            self.err = "Please enter a Mean and S.D. for Location before saving!"

    ##clear UI elements
    def clearElements(self):
        logDebug("locationClass.py::clearElements() called.\n")
        self.funcUI = None
        self.secUI = None
        self.secNumUI = None
        self.meanUI = None
        self.sdUI = None
        self.distUI = None
        
    ###holds the GUI elements references in one place
    def setElements(self, parent):
        logDebug("locationClass.py::setElements() called.\n")
        if(self.func == 0): ##Single
            self.funcUI = parent.findChild(QRadioButton, "locSingle")
            self.secUI = parent.findChild(QComboBox, "Single Picker")
            self.secNumUI = parent.findChild(QLineEdit, "Section Number")
            self.distUI = parent.findChild(QLineEdit, "Distance")
            self.meanUI = None
            self.sdUI = None
        elif(self.func == 1): ##Uniform
            self.funcUI = parent.findChild(QRadioButton, "locMult")
            self.secUI = parent.findChild(QComboBox, "Uniform Picker")
            self.secNumUI = parent.findChild(QLineEdit, "Uniform Section Number")
            self.distUI = None
            self.meanUI = parent.findChild(QLineEdit, "Uniform Mean")
            self.sdUI = parent.findChild(QLineEdit, "Uniform SD")
        else: ##Poisson
            self.funcUI = parent.findChild(QRadioButton, "locPos")
            self.secUI = parent.findChild(QComboBox, "PD Picker")
            self.secNumUI = parent.findChild(QLineEdit, "PD Section Number")
            self.distUI = None
            self.meanUI = parent.findChild(QLineEdit, "Location Mean")
            self.sdUI = parent.findChild(QLineEdit, "Location SD")

    ##sets values for edit mode
    def editGUI(self):
        logDebug("locationClass.py::editGUI() called.\n")
        self.funcUI.setChecked(True)
        self.secUI.setCurrentIndex(self.sec)
        self.secNumUI.setText(self.secNum)
        if(self.distUI is not None):
            self.distUI.setText(self.distance)
        if(self.meanUI is not None):
            self.meanUI.setText(self.mean)
        if(self.sdUI is not None):
            self.sdUI.setText(self.sd)

    ##generates location data based on user inputs
    def generate(self, path, inputs, availSections):
        logDebug("locationClass.py::generate() called.\n")
        try:
            fout = open(path + "/syn_loc.dat", "w")
            buf = ""
            if(self.func == 0): ##Single
                #####check that distance is greater than 0 and if it is
                ##### generate a ranodm point and pass the point
                #### there probably will need to be a conversion from swc to hoc location
                ####convertToNeuron function
                if(float(self.distance) > 0):
                    rid = self.distSingle(availSections)
                    if(rid == None):
                        self.err = "There are no points within the given distance and sections selected."
                        return
                    sec = gv.morphObj.morphParts[rid-1].type-1
                    nid = self.convertToNeuron(sec, rid)
                    buf = self.genSingle(fout, inputs, 2, [sec, nid])
                else:
                    buf = self.genSingle(fout, inputs, 2, [int(self.sec), int(self.secNum) -1])
            elif(self.func == 1): ##Uniform
                part = self.getSecArr()[int(self.secNum)-1]
                dists = self.getDist(part, availSections)
                points = self.getValidDist(float(self.mean), float(self.sd), dists)
                if(len(points) < 1):
                    self.err = "There are no points within the mean and standard deviation given."
                    return
                output = []
                for x in range(inputs):
                    rid = random.choice(points)[0]
                    output.append([gv.morphObj.morphParts[rid-1].type-1, rid])
                buf = self.genLocDis(inputs, 2, output)
            elif(self.func == 2): ##Poisson
                part = self.getSecArr()[int(self.secNum)-1]
                dists = self.getDist(part, availSections)
                randDis = []
                for x in range(0, inputs):
                    randDis.append(self.genRanPD(float(self.mean), float(self.sd)))

                output = []
                for x in randDis:
                    p = self.getPoint(x, dists)
                    output.append([gv.morphObj.morphParts[p-1].type-1, p]) ##file part 0-3, nPart 1-4 ######
                buf = self.genLocDis(inputs, 2, output)
            else:
                self.err = "An error occured while generating Location data"
                return
            
            fout.write(buf)
        except Exception as ex:
            newMsgBox("An error occured while generating Location data", str(ex))
            logErr(str(ex), "locationClass::generate")
        finally:
            fout.close()

    ######randomly choose a single point from the given distance (+/- 5%)
    def distSingle(self, avail):
        part = self.getSecArr()[int(self.secNum)-1]
        dists = self.getDist(part, avail)
        ep = float(self.distance) * .05
        points = self.getValidDist(float(self.distance), ep, dists)
        if(len(points) < 1):
            return None

        return random.choice(points)[0]
        
            
    ##creates and writes data to .dat files for single location option 
    ##fout is the file to write to
    ## inputs is the number of inputs/ number of lines to gen
    ## col is the number of columns to write        
    ## num is an array containing the section type at the first index and the section number at the second index 
    def genSingle(self, fout, inputs, col, num):
        logDebug("locationClass.py::genLocSingle() called.\n")
        buf = str(inputs) + ' ' + str(col) + '\n'

        for i in range(0, inputs):
            buf = buf + str(num[0]) + " " + str(num[1]) + "\n"
        return buf

    ##used to create data points for uniform and poisson distributions
    def genLocDis(self, inputs, col, points):
        logDebug("locationClass.py::genLocDis() called.\n")
        buf = str(inputs) + ' ' + str(col) + '\n'

        for x in range(0, inputs):
            buf = buf + str(points[x][0]) + ' ' + str(self.convertToNeuron(points[x][0], points[x][1])) + '\n'
        return buf

    ##returns an array of inputs based on the segment type
    def getSecArr(self):
        logDebug("locationClass.py::getSecArr() called.\n")
        if self.sec == 0:
            secArr = gv.morphObj.somaInputs
        elif self.sec == 1:
            secArr = gv.morphObj.axonInputs
        elif self.sec == 2:
            secArr = gv.morphObj.basalInputs
        elif self.sec == 3:
            secArr = gv.morphObj.apicalInputs
        return secArr
    
    ###returns the distance of every segment from the given point in the form [[id, dist], [id,dist]....]
    def getDist(self, point, sect):
        logDebug("locationClass.py::getDist() called. --Point: (" + str(point.x)+"," + str(point.y) +")\n")
        ret = []
        for n in sect: 
            ret.append([n.id, math.hypot(n.x - point.x, n.y - point.y)])
        return ret

    #####This returns a list of points that fall within the mean +/- the sd, from the given list of distances (dlist)
    def getValidDist(self, mean, sd, dList):
        logDebug("locationClass.py::validDist() called. --Mean: " + str(mean) +" --S.D.: " + str(sd) + "\n")
        ret = []
        for d in dList:
            if d[1] <= (mean + sd) and d[1] >= (mean - sd):
                ret.append(d)
        return ret

    ###takes a mean and standard deviation and returns a random, POSITIVE number based on a normal distribution
    def genRanPD(self, mean, sd):
        ran = random.normalvariate(mean, sd)
        while(ran < 0):
            ran = random.normalvariate(mean, sd)
        logDebug("locationClass.py::genRanPD() called. --Mean: " + str(mean) + " --S.D.: " + str(sd) + " --Return Val: " + str(ran) + "\n")
        return ran

    ###This function returns the point that is closest to the distance given, from the list of points given (dList)
    def getPoint(self, distance, dList):
        logDebug("locationClass.py::getPoint() called. --Distance: " +str(distance) +"\n")
        ret = -1
        comp = float('inf')

        for d in dList:
            if abs(distance - d[1]) < comp:
                ret = d[0]
                comp = abs(distance - d[1])
        return ret

    ##This function converts ids in the swc file to ids used in Neuron
    def convertToNeuron(self, secType, secID):
        logDebug("locationClass.py::convertToNeuron() called. --secType: "+ str(secType) + " --secID: " + str(secID) + "\n")
        sec = []
        x = 0
        if secType == 0:
            sec = gv.morphObj.somaInputs
        elif secType == 3:
            sec = gv.morphObj.apicalInputs
        elif secType == 2:
            sec = gv.morphObj.basalInputs
        elif secType == 1:
            sec = gv.morphObj.axonInputs

        for part in sec:
            if part.id == secID:
                return x
            x = x + 1
        return -1
