###################################################################  
####                                                           
#### Version: 1.1.4
#### Date: 10/10/2022         
#### Description: This file contains the functions used for loading .nrnez files
#### Author: Evan Cobb                
####                    
###################################################################  

import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from errorLogger import *

##loads each section of the .nrnez file.
def loadNRNEZ(w, path):
    logDebug("loader.py::loadNRNEZ() called. --Path: " + path + "\n")
    try:
        fin = open(path, 'r')
        buf = json.loads(fin.read())

        swcpath = buf["swc_path"]
        swcfile = buf['swc']
        output = buf['output_path']
        run = buf['runs']
        exp = buf['experiment'][0]
        loc = buf['location'][0]
        time = buf['time'][0]
        weight = buf['weight'][0]

        loadPaths(w, swcpath, swcfile, output, run)
        loadExp(w, exp)
        loadLoc(w, loc)
        loadTime(w, time)
        loadWeight(w, weight)
        
    except Exception as ex:
        newMsgBox("Error loading file: " + path, str(ex))
        logErr(str(ex), 'loader::loadNRNEZ()')


##loads the swc file path and the output path into the application.
def loadPaths(w, path, sfile, output, run):
    logDebug("loader.py::loadPaths() called.\n")
    numRuns = int(run) if run is not "" else None
    ### logic check first ###
    if(path == '' and sfile != ''):
        w.findChild(QLineEdit, 'fileName').setText('./' + sfile)

    if(path != ''):
        if(sfile == ''): ###if file name is empty, don't load anything
            pass
        else:
            ### path is missing backslash, so add it
            if(path[-1] != '/'):
                path = path + '/'
            w.findChild(QLineEdit, 'fileName').setText(path + sfile)

    if(output != ''):
        ### output should end in backslash
        if(output[-1] != '/'):
            output = output + '/'
        w.findChild(QLineEdit, 'Output File').setText(output)

    w.findChild(QLineEdit, "Run Number").setText(str(numRuns)) if numRuns is not None else True
    
###loads the experiment portion of the .nrnez file into the application
def loadExp(w, exp):
    logDebug("loader.py::loadExp() called.\n")
    tag = exp['tag']
    inputs = int(exp['inputs']) if exp['inputs'] is not "" else None
    soma = exp['soma']
    axon = exp['axon']
    basal = exp['basal']
    apical = exp['apical']
    color = exp['color']
    
    if(tag is not None and tag != ''):
        w.findChild(QLineEdit, 'Experiment Name').setText(tag)

    w.findChild(QLineEdit, 'Inputs').setText(str(inputs)) if inputs is not None else True

    if(soma == 't'):
        w.findChild(QCheckBox, "somaCB").setChecked(True)
    elif(soma == 'f'):
        w.findChild(QCheckBox, "somaCB").setChecked(False)

    if(axon == 't'):
        w.findChild(QCheckBox, "axonCB").setChecked(True)
    elif(axon == 'f'):
        w.findChild(QCheckBox, "axonCB").setChecked(False)

    if(basal == 't'):
        w.findChild(QCheckBox, "basalCB").setChecked(True)
    elif(basal == 'f'):
        w.findChild(QCheckBox, "basalCB").setChecked(False)

    if(apical == 't'):
        w.findChild(QCheckBox, "apicalCB").setChecked(True)
    elif(apical == 'f'):
        w.findChild(QCheckBox, "apicalCB").setChecked(False)

    if(color == 'white' or color == 'black' or color == 'gray' or color == 'red' or color == 'green' or color == 'blue' or color == 'yellow' or color == 'cyan' or color == 'magenta'):
        gv.color = QColor(color)

###loads the location portion of the .nrnez file into the application.
def loadLoc(w, loc):
    logDebug("loader.py::loadLoc() called.\n")
    ltype = loc['type']
    sec = loc['section']
    seg = int(loc['segment']) if loc['segment'] is not "" else None
    dist = float(loc['distance']) if loc['distance'] is not "" else None
    mean = float(loc['mean']) if loc['mean'] is not "" else None
    sd = float(loc['sd']) if loc['sd'] is not "" else None
    
    if(ltype == 's'):
        w.findChild(QRadioButton, 'locSingle').setChecked(True)
        w.findChild(QLineEdit, 'Section Number').setText(str(seg)) if seg is not None else True

        picker = w.findChild(QComboBox, 'Single Picker')
        if(sec == 's'):
            picker.setCurrentIndex(0)
        elif(sec == 'x'):
            picker.setCurrentIndex(1)
        elif(sec == 'b'):
            picker.setCurrentIndex(2)
        elif(sec == 'a'):
            picker.setCurrentIndex(3)

        w.findChild(QLineEdit, "Distance").setText(str(dist)) if dist is not None else True

    elif(ltype == 'u'):
        w.findChild(QRadioButton, 'locMult').setChecked(True)
        w.findChild(QLineEdit, 'Uniform Section Number').setText(str(seg)) if seg is not None else True

        picker = w.findChild(QComboBox, 'Uniform Picker')
        if(sec == 's'):
            picker.setCurrentIndex(0)
        elif(sec == 'x'):
            picker.setCurrentIndex(1)
        elif(sec == 'b'):
            picker.setCurrentIndex(2)
        elif(sec == 'a'):
            picker.setCurrentIndex(3)

        w.findChild(QLineEdit, "Uniform Mean").setText(str(mean)) if mean is not None else True
        w.findChild(QLineEdit, "Uniform SD").setText(str(sd)) if sd is not None else True
        
    elif(ltype == 'p'):
        w.findChild(QRadioButton, 'locPos').setChecked(True)
        w.findChild(QLineEdit, 'PD Section Number').setText(str(seg)) if seg is not None else True

        picker = w.findChild(QComboBox, 'PD Picker')
        if(sec == 's'):
            picker.setCurrentIndex(0)
        elif(sec == 'x'):
            picker.setCurrentIndex(1)
        elif(sec == 'b'):
            picker.setCurrentIndex(2)
        elif(sec == 'a'):
            picker.setCurrentIndex(3)
        
        w.findChild(QLineEdit, "Location Mean").setText(str(mean)) if mean is not None else True
        w.findChild(QLineEdit, "Location SD").setText(str(sd)) if sd is not None else True

##loads the time portion of the .nrnez file into the application.
def loadTime(w, time):
    logDebug("loader.py::loadTime() called.\n")
    ttype = time['type']
    onset = float(time['onset']) if time['onset'] is not "" else None
    interval = float(time['interval']) if time['interval'] is not "" else None
    mean = float(time['mean']) if time['mean'] is not "" else None
    sd = float(time['sd']) if time['sd'] is not "" else None

    w.findChild(QLineEdit, 'Time of Onset').setText(str(onset))
    if(ttype == 's'):
        w.findChild(QRadioButton, 'timeSingle').setChecked(True)
        w.findChild(QLineEdit, 'Interval').setText(str(interval)) if interval is not None else True
    elif(ttype == 'u'):
        w.findChild(QRadioButton, 'timeMult').setChecked(True)
        w.findChild(QLineEdit, 'Interval M Mean').setText(str(mean)) if mean is not None else True
        w.findChild(QLineEdit, 'Interval M SD').setText(str(sd)) if sd is not None else True
    elif(ttype == 'p'):
        w.findChild(QRadioButton, 'timePos').setChecked(True)
        w.findChild(QLineEdit, 'Interval Mean').setText(str(mean)) if mean is not None else True
        w.findChild(QLineEdit, 'Interval SD').setText(str(sd)) if sd is not None else True

###loads the weight portion of the .nrnez file into the application.
def loadWeight(w, weight):
    logDebug("loader.py::loadWeight() called.\n")
    mod = weight['module']
    wtype = weight['type']
    name = weight['name']
    current = float(weight['current']) if weight['current'] is not "" else None
    durType = weight['duration_type'] 
    duration = float(weight['duration']) if weight['duration'] is not "" else None
    durMean = float(weight['duration_mean']) if weight['duration_mean'] is not "" else None
    durSD = float(weight['duration_sd']) if weight['duration_sd'] is not "" else None
    wei = float(weight['weight']) if weight['weight'] is not "" else None
    e = float(weight['e']) if weight['e'] is not "" else None
    tau1 = float(weight['tau1']) if weight['tau1'] is not "" else None
    tau2 = float(weight['tau2']) if weight['tau2'] is not "" else None
    mean = float(weight['mean']) if weight['mean'] is not "" else None
    sd = float(weight['sd']) if weight['sd'] is not "" else None
    custPath = weight['custom_path']
    custName = weight['custom']

    if(mod == 'i'):
        w.findChild(QComboBox, 'Weight Picker').setCurrentIndex(0)
        w.findChild(QLineEdit, 'Current Name').setText(name)
        durPicker = w.findChild(QComboBox, 'Duration Picker')
        if(durType == 's'):
            durPicker.setCurrentIndex(0)
            w.findChild(QLineEdit, 'Duration').setText(str(duration)) if duration is not None else True
        elif(durType == 'u'):
            durPicker.setCurrentIndex(1)
            w.findChild(QLineEdit, 'Duration Uniform Mean').setText(str(durMean)) if durMean is not None else True
            w.findChild(QLineEdit, 'Duration Uniform SD').setText(str(durSD)) if durSD is not None else True
        elif(durType == 'p'):
            durPicker.setCurrentIndex(2)
            w.findChild(QLineEdit, 'Duration Poisson Mean').setText(str(durMean)) if durMean is not None else True
            w.findChild(QLineEdit, 'Duration Poisson SD').setText(str(durSD)) if durSD is not None else True
            
        if(wtype == 's'):
            w.findChild(QRadioButton, 'curSingle').setChecked(True)
            w.findChild(QLineEdit, 'Single Current').setText(str(current)) if current is not None else True
        elif(wtype == 'u'):
            w.findChild(QRadioButton, 'curMult').setChecked(True)
            w.findChild(QLineEdit, 'cur Uni Mean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'cur Uni SD').setText(str(sd)) if sd is not None else True
        elif(wtype == 'p'):
            w.findChild(QRadioButton, 'curPos').setChecked(True)
            w.findChild(QLineEdit, 'curMean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'curSD').setText(str(sd)) if sd is not None else True

    elif(mod == 's'):
        w.findChild(QComboBox, 'Weight Picker').setCurrentIndex(1)
        w.findChild(QLineEdit, 'Weight Name').setText(name)
        w.findChild(QLineEdit, 'E').setText(str(e)) if e is not None else True
        w.findChild(QLineEdit, 'Tau1').setText(str(tau1)) if tau1 is not None else True
        w.findChild(QLineEdit, 'Tau2').setText(str(tau2)) if tau2 is not None else True
        if(wtype == 's'):
            w.findChild(QRadioButton, 'ampSingle').setChecked(True)
            w.findChild(QLineEdit, 'Single Weight').setText(str(wei)) if wei is not None else True
        elif(wtype == 'u'):
            w.findChild(QRadioButton, 'ampMult').setChecked(True)
            w.findChild(QLineEdit, 'amp Uni Mean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'amp Uni SD').setText(str(sd)) if sd is not None else True
        elif(wtype == 'p'):
            w.findChild(QRadioButton, 'ampPos').setChecked(True)
            w.findChild(QLineEdit, 'ampMean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'ampSD').setText(str(sd)) if sd is not None else True

    elif(mod == 'c'):
        w.findChild(QComboBox, 'Weight Picker').setCurrentIndex(2)
        
        if(custPath == '' and custName != ''):
            w.findChild(QLineEdit, 'ModFile').setText('./' + custName)
        if(custPath != ''):    
            if(custName == ''):
                pass
            else:
                if(custPath[-1] != '/'):
                    custPath = custPath + '/'
                w.findChild(QLineEdit, 'ModFile').setText(custPath + custName)

        if(wtype == 's'):
            w.findChild(QRadioButton, 'custSingle').setChecked(True)
            w.findChild(QLineEdit, 'Single Custom').setText(str(wei)) if wei is not None else True
        elif(wtype == 'u'):
            w.findChild(QRadioButton, 'custMult').setChecked(True)
            w.findChild(QLineEdit, 'cust Uni Mean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'cust Uni SD').setText(str(sd)) if sd is not None else True
        elif(wtype == 'p'):
            w.findChild(QRadioButton, 'custPos').setChecked(True)
            w.findChild(QLineEdit, 'custMean').setText(str(mean)) if mean is not None else True
            w.findChild(QLineEdit, 'custSD').setText(str(sd)) if sd is not None else True


    
