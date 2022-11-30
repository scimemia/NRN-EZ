###################################################################
####
#### Version: 1.1.6
#### Date: 11/30/2022
#### Description: This file contains the class definition of the experiment object
#### Author: Evan Cobb
####
###################################################################
 
import globvar as gv
import datetime as dt
import shutil
from errorLogger import *
from weightClass import *
from timeClass import *
from locationClass import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class experimentObject:
    def __init__(self, name, loc, time, weight, numInputs, color, soma, apical, basal, axon):
        logDebug("experimentClass.py::init() called.\n")
        self.name = name
        self.loc = loc #locObject  
        self.time = time #timeObject 
        self.weight = weight #array of weight objects
        self.inputs = numInputs 
        self.color = color
        self.soma = soma
        self.apical = apical
        self.basal = basal
        self.axon = axon
        self.path = None ##holds the path of the experiment directory
        self.custom = []
        self.weightCount = False
        self.currentCount = False
        self.hocNames = []
        self.err = False
        self.errString = ""

        if(name == ""):
            self.err = True
            self.errString = "Please enter a name before saving!"
        if(numInputs == ""):
            self.err = True
            self.errString = "Please enter the number of inputs before saving!"
        if(len(weight) < 1):
            self.err = True
            self.errString = "Please enter at least one weight distribution before saving!"
        if not(soma or apical or basal or axon):
            self.err = "Please check at least one segment type before saving!"

    ##clears UI elements for pickling
    def clearElements(self):
        logDebug("experimentClass.py::clearElements() called.\n")
        self.loc.clearElements()
        self.time.clearElements()
        for w in self.weight:
            w.clearElements()

    ##fills GUI when the edit button is clicked
    def editGUI(self, parent):
        logDebug("experimentClass.py::editGUI() called.\n")
        parent.findChild(QLineEdit, "Experiment Name").setText(self.name)
        parent.findChild(QLineEdit, "Inputs").setText(self.inputs)
        parent.findChild(QCheckBox, "somaCB").setChecked(self.soma)
        parent.findChild(QCheckBox, "apicalCB").setChecked(self.apical)
        parent.findChild(QCheckBox, "basalCB").setChecked(self.basal)
        parent.findChild(QCheckBox, "axonCB").setChecked(self.axon)

        self.loc.setElements(parent)
        self.loc.editGUI()
        self.time.setElements(parent)
        self.time.editGUI()

        gv.color = QColor(self.color)
        ##weight##
        gv.editMode = None
        gv.model.clear()

        gv.model.setHorizontalHeaderLabels(['Module', 'Name', 'Weight'])
        for inputVar in self.weight:
            gv.model.appendRow([QStandardItem(inputVar.type), QStandardItem(inputVar.name), QStandardItem(inputVar.getFunc())])
        gv.wTable.setColumnWidth(0, 105)
        gv.wTable.setColumnWidth(1, 105)
        gv.wTable.setColumnWidth(2, 106)
        gv.weightInputs = self.weight

    ##generates output for the experiment
    def generate(self, parent):
        logDebug("experimentClass.py::generate() called.\n")
        ######location gen######
        self.loc.generate(self.path, int(self.inputs), self.availSect())
        ######time gen######
        self.time.generate(self.path, int(self.inputs))
        #######weight gen######
        weightOut = []
        weightVars = []
        currentOut = []
        currentVars = []
        customOut = []
        
        ##generate all the weights
        for synIn in self.weight:
            if synIn.type == "Syn-Input":
                weightOut.append(synIn.generate(int(self.inputs)))
                weightVars.append([synIn.e, synIn.tau1, synIn.tau2])
            elif synIn.type == "I-Step":
                currentOut.append(synIn.generate(int(self.inputs)))
                if(synIn.durType == 0): ##Single
                    currentVars.append(synIn.duration)
                elif(synIn.durType == 1): ##Uniform
                    currentVars.append(str(synIn.getDurationUniform()))
                else: ##Poisson
                    currentVars.append(str(synIn.getDurationPoisson()))
            else: ###custom
                self.customWriter(self.path, synIn.generate(int(self.inputs)), synIn.name)
                self.custom.append(synIn.name)
                try:
                    shutil.copy(synIn.path, gv.incPath + 'tmp/')
                except Exception as ex:
                    newMsgBox('Error copying tmp folder', str(ex))
                    logErr(str(ex), 'experimentClass :: generate()')
        if(len(weightOut) > 0):
            self.weightWriter(self.path, weightOut, weightVars)
            self.weightCount = True
        if(len(currentOut)  > 0):
            self.currentWriter(self.path, currentOut, currentVars)
            self.currentCount = True
            
    ##returns the segments of the neuron the user selected to be used for the output
    def availSect(self):
        logDebug("experimentClass.py::availSect() called.\n")
        allCheck = 0
        ret = []
        if(self.soma):
            allCheck = allCheck+1
            ret.extend(gv.morphObj.somaInputs)
        if(self.apical):
            allCheck = allCheck+1
            ret.extend(gv.morphObj.apicalInputs)
        if(self.basal):
            allCheck = allCheck+1
            ret.extend(gv.morphObj.basalInputs)
        if(self.axon):
            allCheck = allCheck+1
            ret.extend(gv.morphObj.axonInputs)

        if allCheck == 4:
            return gv.morphObj.morphParts
        else:
            return ret

    ###writes output data for synaptic input .dat files    
    def weightWriter(self, path, weightOut, weightVars):
        logDebug("experimentClass.py::weightWriter() called.\n")
        buf = ""
        varBuf = ""
        for x in range(0, int(self.inputs)):
            for arr in weightOut:
                buf = buf + str(arr[x]) + " "
            buf = buf + "\n"

        for x in range(len(weightOut)):
            varBuf = varBuf + weightVars[x][0] + " " + weightVars[x][1] + " " + weightVars[x][2] + "\n"

        try:
            fweight = open(path + "/syn_weight.dat", "w")
            fvars = open(path + "/vars_weight.dat", "w")
            fweight.write(str(self.inputs) + " " + str(len(weightOut)) + "\n")
            fvars.write(str(len(weightOut)) + " " + "3\n")
            fweight.write(buf)
            fvars.write(varBuf)
        except Exception as ex:
            newMsgBox("Error generating synaptic input files", str(ex))
            logErr(str(ex), 'experimentClass::weightWriter()')
        finally:
            fweight.close()
            fvars.close()

    ###writes output data for I-Step .dat files
    def currentWriter(self, path, currentOut, currentVars):
        logDebug("experimentClass.py::currentWriter() called.\n")
        buf = ""
        varBuf = ""
        for x in range(0, int(self.inputs)):
            for arr in currentOut:
                buf = buf + str(arr[x]) + " "
            buf = buf + "\n"

        for x in range(len(currentOut)):
            varBuf = varBuf + currentVars[x] + "\n"
        try:
            fcurrent = open(path + "/syn_current.dat", "w")
            fvars = open(path + "/vars_current.dat", "w")
            fcurrent.write(str(self.inputs) + " " + str(len(currentOut)) + "\n")
            fvars.write(str(len(currentVars)) + " " + "1\n")
            fcurrent.write(buf)
            fvars.write(varBuf)
        except Exception as ex:
            newMsgBox("Error generating I-Step files", str(ex))
            logErr(str(ex), 'experimentClass::currentWriter()')
        finally:
            fcurrent.close()
            fvars.close()

    ###writes output data for the custom weight .dat files 
    def customWriter(self, path, customOut, name):
        logDebug("experimentClass.py::customWriter() called.\n")
        buf = ""
        for x in range(0, int(self.inputs)):
            buf = buf + str(customOut[x]) + "\n"

        try:
            fcustom = open(path + "/" + name + ".dat", "w")
            fcustom.write(str(self.inputs) + " 1\n")
            fcustom.write(buf)
        except Exception as ex:
            newMsgBox("Error generating Custom weight files",  str(ex))
            logErr(str(ex), 'experimentClass::customWriter()')
        finally:
            fcustom.close()

    ##generates hoc files for each type of weight (i-step, synaptic, custom)
    def genHocFile(self, exclude, uid):
        logDebug("experimentClass.py::genHocFile() called.\n")
        bufIn = ""
        bufOut = ""
        try:
            #####create weight hoc file
            if(self.weightCount):
                fin = open(gv.incPath + "weight.tmplt", "r")
                fout = open(self.path + "/weight.hoc", "w")
                bufIn = fin.read()
                bufIn = self.replaceVar(bufIn, '//~~~STIMVAR~~~//', 'w_' + str(uid))
                bufIn = bufIn.split("\n")

                bufOut = self.replaceText(bufIn, '***PATH***', self.name)

                for ex in exclude:
                    bufOut = self.removeText(bufOut, ex)
                
                fout.write(getComments())
                fout.write(bufOut)
                
                fin.close()
                fout.close()
                self.hocNames.append('weight.hoc')
            ###create current hoc file
            if(self.currentCount):
                fin = open(gv.incPath + "current.tmplt", "r")
                fout = open(self.path + "/current.hoc", "w")
                bufIn = fin.read()
                bufIn = self.replaceVar(bufIn, '//~~~STIMVAR~~~//', 'cur_' + str(uid))
                bufIn = bufIn.split("\n")
                bufOut = self.replaceText(bufIn, '***PATH***', self.name)

                for ex in exclude:
                    bufOut = self.removeText(bufOut, ex)
                
                fout.write(getComments())
                fout.write(bufOut)
                
                fin.close()
                fout.close()
                self.hocNames.append('current.hoc')
            ###create custom hoc files
            customID = 1
            for c in self.custom:
                fin = open(gv.incPath + "custom.tmplt", "r")
                fout = open(self.path + '/' + c + '.hoc', 'w')
                bufIn = fin.read()
                bufIn = self.replaceVar(bufIn, '//~~~STIMVAR~~~//', 'cust_' + str(uid) + '_' + str(customID))
                bufIn = bufIn.split("\n")
                bufOut = self.replaceText(bufIn, '***PATH***', self.name)
                bufIn = bufOut.split('\n')
                bufOut = self.replaceText(bufIn, '~~**CUSTOM**~~', c)

                for ex in exclude:
                    bufOut = self.removeText(bufOut, ex)
                
                fout.write(getComments())
                fout.write(bufOut)

                fin.close()
                fout.close()
                self.hocNames.append(c + '.hoc')
                customID = customID + 1
                
        except Exception as err:
            newMsgBox("Error generating hoc files", str(err))
            logErr(str(err), "experimentClass::genHocFiles()")
        finally:
            fin.close()
            fout.close()
            self.weightCount = False
            self.currentCount = False
            del self.custom[:]

    ##used to insert custom code into hoc files
    def replaceText(self, bufIn, pattern, replace):
        logDebug("experimentClass.py::replaceText() called.\n")
        bufOut = ""
        for line in bufIn:
            l = line.partition(pattern)
            if l[2] != "":
                bufOut = bufOut + l[0] + replace + l[2] + "\n"
            else:
                bufOut = bufOut + l[0] + "\n"
        return bufOut

    ##used to remove patterns in the hoc file
    def removeText(self, bufIn, pattern):
        logDebug("experimentClass.py::removeText() called.\n")
        buf = bufIn.partition(pattern)
        buf2 = buf[2].partition(pattern)
        return buf[0] + buf2[2]

    ##used to replace text in hoc files
    def replaceVar(self, bufIn, pattern, replace):
        logDebug("experimentClass.py::replaceVar() called.\n")
        buf = bufIn.partition(pattern)
        
        if(buf[2] != ''):
            bufOut = buf[0] + replace
            while(buf[2] != ''):
                buf = buf[2].partition(pattern)
                if(buf[2] != ''):
                    bufOut = bufOut + buf[0] + replace
            bufOut = bufOut + buf[0]
        else:
            return bufIn
        return bufOut
