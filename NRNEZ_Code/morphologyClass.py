###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This file contains the class definitions for the Morphology object, and the nPart object
#### Author: Evan Cobb
####
###################################################################
 
import sys
import shutil
import globvar as gv
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import math
from errorLogger import *
import pyqtgraph as pg
import os
import datetime as dt
from gui_handler import segSelect

##nPart is an object that contains a row of data from SWC files
class nPart:
    def __init__(self, id, type, x, y, z, r, pid):
        logDebug("morphologyClass.py::nPart::init() called.\n")
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.pid = pid

###This class contains all functions that deal with the morphology graph and generating morphology data
class morphologyClass():
    def __init__(self):
        logDebug("morphologyClass.py::init() called.\n")
        self.initVars()

    ##create plot object
    def setPlotObj(self):
        logDebug("morphologyClass.py::setPlotObj() called.\n")
        try:
            self.plotObj = gv.graphWin.addPlot()
            self.plotObj.setLabel('left', text="y-position", units= "m")
            self.plotObj.setLabel('bottom', text="x-position",units= "m")
            self.plotObj.getAxis('bottom').setScale(1e-6)
            self.plotObj.getAxis('left').setScale(1e-6)
            self.plotObj.setObjectName(self.swcfname)
            self.plotObj.setParent(gv.graphWin)
            self.plotObj.scene().sigMouseClicked.connect(segSelect)
            gv.plotObj = self.plotObj
        except Exception as ex:
            newMsgBox("An error occured while creating the plot", str(ex))
            logErr(str(ex), "mophologyClass::setPlotObj")

    ##initiate object variables
    def initVars(self):
        logDebug("morphologyClass.py::initVars() called.\n")
        self.morphParts = []  ## all parts loaded
        self.somaInputs = [] ## soma parts loaded
        self.apicalInputs = []
        self.basalInputs = []
        self.axonInputs = []
        self.swcfname = None  ###file to be loaded
        self.swcPath = None
        self.totalInputs = 0  ###count of segs loaded
        self.fLoadFlag = False ##flag to check if file is loaded. 
        self.highlighted = None

    ##clears the plot object
    def clearPlot(self):
        logDebug("morphologyClass.py::clearPlot() called.\n")
        self.plotObj = None
        self.highlighted = None

    ##restores the plot object
    def restorePlot(self):
        logDebug("morphologyClass.py::restorePlot() called.\n")
        plot = gv.graphWin.findChild(pg.PlotItem, self.swcfname)
        if(plot is not None):
            self.plotObj = plot
        else:
            self.setPlotObj()

    ##loads SWC file 
    def loadFile(self, fileName, lineEdits):
        logDebug("morphologyClass.py::loadFile() called. Filename:: " + fileName + "\n")
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        msg = ''
        ##do some cleanup first, in case of loading a new file
        self.initVars()
        self.swcPath = fileName
        self.swcfname = fileName.split('/')[-1][:-4] ##remove path and swc ext
        gv.graphWin.clear()
        self.setPlotObj()
        
        try:
            morph = open(fileName, 'r')
        except Exception as ex:
            QApplication.restoreOverrideCursor()
            newMsgBox("Error opening file: " + fileName, "Error" + "\n" + str(ex))
            logErr(str(ex), "morphologyClass::loadFile")
            return
        
        logRun("morphology file opened: " + fileName + "\n")

        try:
            for line in morph:
                if line[:1] != '#':
                    var = line.split()
                    newPart = nPart(int(var[0]), int(var[1]), float(var[2]), float(var[3]), float(var[4]), float(var[5]), int(var[6]))

                    self.morphParts.append(newPart)
                    if(int(var[1]) == 1):
                        self.somaInputs.append(newPart)
                    elif(int(var[1]) == 4):
                        self.apicalInputs.append(newPart)
                    elif(int(var[1]) == 3):
                        self.basalInputs.append(newPart)
                    elif(int(var[1]) == 2):
                        self.axonInputs.append(newPart)
                    else:
                        msg = msg + var[0] + "\n"

            logRun("every line in morphology processed\n")
            morph.close()

            self.setPartsLE(lineEdits)
            
            self.totalInputs = len(self.somaInputs) + len(self.apicalInputs) + len(self.basalInputs) + len(self.axonInputs)
        
            if(msg != ''):
                newMsgBox('The following part ids in the SWC file were not of the expected type: \n', msg, "Warning!")

            self.fLoadFlag = True
            self.buildGraph()
        except Exception as err:
            newMsgBox("An error occured while loading the morphology file", str(err))
            logErr( str(err), "morphologyClass::loadFile")
        finally:
            QApplication.restoreOverrideCursor()

    ##sets meta data about morphology in the GUI
    def setPartsLE(self, lineEdits):
        logDebug("morphologyClass.py::setPartsLE() called.\n")
        lineEdits[0].setText(str(len(self.somaInputs)-1)) #minus one because ofthe origin point
        lineEdits[1].setText(str(len(self.apicalInputs)))
        lineEdits[2].setText(str(len(self.basalInputs)))
        lineEdits[3].setText(str(len(self.axonInputs)))

    ##creates the graph for the morphology
    def buildGraph(self):
        logDebug("morphologyClass.py::buildGraph() called.\n")
        logRun("buildGraph function\n")
        self.plotObj.clear() ##clear graph
        del gv.lines[:]
        
        arrX = []
        arrY = []
        somaPen = pg.mkPen('k', width=2)
        apicPen = pg.mkPen('b', width=2)
        basPen = pg.mkPen('c', width=2)
        axonPen = pg.mkPen('m', width=1)

        ##The plotting works by plotting "branches" of the morphology instead of each line individually
        ##This is to decrease overhead
        ##A branch is created when the parent id is non-sequential to the child id
        for part in self.morphParts:
            if part.pid < 1:
                continue
            px = self.morphParts[part.pid-1].x
            py = self.morphParts[part.pid-1].y
            gv.lines.append([px, py, part.x, part.y, part.id])
            ###if the segment branches, plot it and continue
            if(part.type != 1 and (part.id - part.pid) != 1):
                self.plotObj.plot(arrX, arrY, pen=pen)
                del arrX[:]
                del arrY[:]
            ##set line based on segment
            if part.type == 1:
                pen = somaPen
            elif part.type == 4:
                pen = apicPen
            elif part.type == 3:
                pen = basPen
            elif part.type == 2:
                pen = axonPen
            #remove plotting points, only want lines
            if(len(arrX) == 0 or (arrX[len(arrX) - 1] != px and arrY[len(arrY) - 1] != py)):
                arrX.append(px)
                arrY.append(py)
            arrX.append(part.x)
            arrY.append(part.y)
        
        self.plotObj.plot(arrX, arrY, pen=pen) ##one last plot after the loop

    ##this is for user highlighting segments
    def textChanged(self, le, picker):
        logDebug("morphologyClass.py::textChanged() called.\n")
        if not(self.highlighted is None):
            self.plotObj.removeItem(self.highlighted)
        if not(self.fLoadFlag) or len(le.text()) == 0:
            return

        if picker.currentIndex() == 0:
            if self.somaInputs[0].pid == -1: ##skip the origin point
                inputs = self.somaInputs[1:]
            else:
                inputs = self.somaInputs
            pen = pg.mkPen(QColor("lightGray"), width=4)
        elif picker.currentIndex() == 1:
            inputs = self.axonInputs
            pen = pg.mkPen("g", width=4)
        elif picker.currentIndex() == 2:
            inputs = self.basalInputs
            pen = pg.mkPen("r", width=4)
        else:
            inputs = self.apicalInputs
            pen = pg.mkPen(QColor("goldenrod"), width=4)

        ##point doesn't exist
        if int(le.text()) > len(inputs):
            return

        part = inputs[int(le.text())-1]
        px = self.morphParts[part.pid-1].x
        py = self.morphParts[part.pid-1].y
        self.highlighted = self.plotObj.plot([px, part.x], [py, part.y], pen=pen)

    ##plots the data generated from the user inputs
    def plotInputs(self, path, color):
        logDebug("morphologyClass.py::plotInputs() called. Path:: " + path + "\n")
        
        try:
            fin = open(path, "r")
        except Exception as ex:
            newMsgBox("Error opening the data file: " + path, str(ex))
            logErr(str(ex), "morphologyClass::plotInputs")
            return
        
        try:
            plot = self.plotObj.plot()

            x = 0 ##handle the first line which isn't an input  
            xp = []
            yp = []
            for line in fin:
                if x == 0:
                    x = 1
                    continue
                ##Type should always be first, then section number
                p = line.split()
                section = int(p[0]) ##file is 0-3, nPart is 1-4
                sec = []
                if section == 0:
                    sec = self.somaInputs
                elif section == 3:
                    sec = self.apicalInputs
                elif section == 2:
                    sec = self.basalInputs
                elif section == 1:
                    sec = self.axonInputs

                if section == 0: ###soma is a litle weird                                   
                    part = sec[int(p[1])+1]
                else:
                    part = sec[int(p[1])]
                
                parent = self.morphParts[part.pid - 1]
                xp.append((part.x + parent.x)/2)
                yp.append((part.y + parent.y)/2)

            plot.setData(xp, yp, pen=None, symbol='o', symbolSize=6, symbolBrush=pg.mkBrush(QColor(color)))
            gv.inPoints.append(plot)
        except Exception as ex:
            newMsgBox("Error plotting inputs", str(ex))
            logErr(str(ex), "morphologyClass::plotInputs")
            
    ##clear current inputs on the graph
    def clearInputs(self):
        logDebug("morphologyClass.py::clearInputs() called.\n")
        for p in gv.inPoints:
            self.plotObj.removeItem(p)
        del gv.inPoints[:]
        
    ##generates .hoc and .nrn files
    def genOverall(self, exp, path):
        if gv.debug:
            buf = "File names:\n"
            for ex in exp:
                buf = buf + "\t" + ex.name + "\n"
            logDebug("morphologyClass.py::genOverall() called. Path: " + path + "\n" + buf)

        try:
            fout = open(path + "/nrnez.hoc", "w")
    
            fout.write(getComments())

            fout.write('xopen("' + self.swcfname + '.nrn")\n')
            fout.write('xopen("headers.hoc")\n')
            for ex in exp:
                for hoc in ex.hocNames:
                    fout.write('xopen("./' + ex.name + '/' + hoc + '")\n')
                del ex.hocNames[:]
            ##copy files
            shutil.copy('./incl/headers.hoc', path)
            shutil.copy('./incl/mods/netstims.mod', path)
            files = os.listdir('./incl/tmp') 
            for f in files:
                if(os.path.isfile('./incl/tmp/' + f)):
                    shutil.copy('./incl/tmp/' + f, path)
            ##clean up
            ##shutil.rmtree('./incl/tmp')
        ###raise exception here?    
        except Exception as err:
            newMsgBox("An error occured while generating .hoc files: " + str(err))
            logErr(str(err), "morphologyClass::genOverall")
        finally:
            fout.close()

    ##generates the .nrn file 
    def genNrn(self, path):
        logDebug("morphologyClass.py::genNrn() called. SWC File: "+ self.swcfname + " --Path: " + path +"\n")

        buf = 'create '
        if(len(self.somaInputs) > 0):
            buf = buf + "soma[" + str(len(self.somaInputs)) + "],"
        if(len(self.apicalInputs) > 0):
            buf = buf + " apical[" + str(len(self.apicalInputs)) + "],"
        if(len(self.basalInputs) > 0):
            buf = buf + " basal[" + str(len(self.basalInputs)) + "],"  
        if(len(self.axonInputs) > 0):
            buf = buf + " axon[" + str(len(self.axonInputs)) + "]"

        if(buf[-1] == ','):
            buf = buf[:-1]
        
        buf = buf + "\n\n"

        somaBuild = self.buildParts("soma", self.somaInputs)
        apicalBuild = self.buildParts("apical", self.apicalInputs)
        basalBuild = self.buildParts("basal", self.basalInputs)
        axonBuild = self.buildParts("axon", self.axonInputs)

        buf = buf + somaBuild[0] + "\n" + apicalBuild[0] + "\n" + basalBuild[0] + "\n" + axonBuild[0] + "\n\n" + self.buildConnect(somaBuild[1], apicalBuild[1], basalBuild[1], axonBuild[1])

        try:
            fout = open(path + "/" + self.swcfname + ".nrn", "w")
            fout.write(getComments())
            fout.write(buf)
        except Exception as err:
            newMsgBox("Error generating .nrn file", str(err))
            logErr(str(err), "morphologyClass:genNrn")
        finally:
            fout.close()

    ##used to write .nrn file
    def recID(self, rid, soma, apical, basal, axon):
        logDebug("morphologyClass.py::recID() called.\n")

        for a in soma:
            if soma[a] == rid:
                return "soma[" + str(a) + "]"
        for a in apical:
            if apical[a] == rid:
                return "apical[" + str(a) + "]"
        for a in basal:
            if basal[a] == rid:
                return "basal[" + str(a) + "]"
        for a in axon:
            if axon[a] == rid:
                return "axon[" + str(a) + "]"

    ##used to build .nrn file
    def buildParts(self, pname, parts):
        logDebug("morphologyClass.py::buildParts() called. Segment: " + pname + " --Number of sections: " + str(len(parts)) + "\n")

        count = 0
        defBuf = ""
        sdict = {}

        for sec in parts:
            if(sec.pid == -1):
                continue
            else:
                parent = self.morphParts[sec.pid-1]
                length = math.hypot(sec.x - parent.x, sec.y - parent.y)
                defBuf = defBuf + pname +"[" + str(count) + "] {nseg=1 diam=" + str(sec.r*2) + " L=" + str(length) + "}\n"

                sdict[count] = sec.id
                count = count + 1
            
        return [defBuf, sdict]

    ##used to build .nrn file. There is a conversion needed from swc to Neuron ids that this handles
    def buildConnect(self, soma, apical, basal, axon):
        logDebug("morphologyClass.py::buildConnect() called.\n")
        pdict = {}
        buf = "soma[0] {"
        try:
            ##initate the dictionary                                                    
            for sec in self.morphParts:
                pdict[sec.id] = []
            ###fill the dictionary 
            for sec in self.morphParts:
                if not(sec.pid == -1):
                    pdict[sec.pid].append(sec.id)
        except Exception as ex:
            newMsgBox("Error creating the .nrn file", str(ex))
            logErr(str(ex), "morphologyClass::buildConnect")
            return
        
        ###build connector string 
        #####1 and 2 are special cases, every other id should have a good mapping
        for p in pdict[1]:
            if p == 2:
                continue
            else:
                buf = buf + " connect " + self.recID(p, soma, apical, basal, axon) + "(0), 0\n"
        for p in pdict[2]:
            buf = buf + " connect " + self.recID(p, soma, apical, basal, axon) + "(0), 1\n"
        buf = buf + "}\n"

        try:
            for id in pdict:
                if len(pdict[id]) == 0 or id == 1 or id == 2:
                    continue
                buf = buf + self.recID(id, soma, apical, basal, axon)
                if len(pdict[id]) == 1:
                    buf = buf + " connect " + self.recID(pdict[id][0], soma, apical, basal, axon) +"(0), 1\n"
                else:
                    buf = buf + " {"
                    for pid in pdict[id]:
                        buf = buf + " connect " + self.recID(pid, soma, apical, basal, axon) +"(0), 1\n"
                    buf = buf + "}\n"

        except Exception as ex:
            newMsgBox("Error creating the .nrn file", str(ex))
            logErr(str(ex), "morphologyClass::buildConnect")
        return buf
