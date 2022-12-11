###################################################################
####
#### Version: 1.1.6
#### Date: 10/26/2022
#### Description: This file contains the code for the configuration menu of Neuron EZ. The current config menu contains sections for about, reference, and an option to set debug mode.
#### Author: Evan Cobb
####
###################################################################
 
import sys
import hashlib as hl
import json
import os
import globvar as gv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

jsonPath = gv.incPath + 'config.json'

##Display config menu
def window():

    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(100,100,300,380)
    w.setWindowTitle("NEURON-EZ Configuration")

    aboutLabel = QLabel('About:', w)
    aboutLabel.move(5,5)
    aboutLE = QTextEdit(w)
    aboutLE.move(20, 30)
    aboutLE.setFixedWidth(260)
    aboutLE.setFixedHeight(100)

    
    refLabel = QLabel('Reference:', w)
    refLabel.move(5, 138)
    refLE = QTextEdit(w)
    refLE.move(20, 163)
    refLE.setFixedWidth(260)
    refLE.setFixedHeight(100)

    nrnezButton = QPushButton(w)
    nrnezButton.setText('.nrnez File')
    nrnezButton.move(20, 280)
    nrnezLE = QLineEdit(w)
    nrnezLE.setFixedWidth(260)
    nrnezLE.move(20, 310)

    nrnezButton.clicked.connect(lambda: nrnezLoad(w, nrnezLE))
    
    debugCB = QCheckBox("Debug", w)
    debugCB.move(5, 351)

    saveButton = QPushButton(w)
    saveButton.setText('Save')
    saveButton.move(200, 351)
    saveButton.clicked.connect(lambda: saveClicked(w, aboutLE, refLE, debugCB, nrnezLE))
    
    if(not load(aboutLE, refLE, debugCB, nrnezLE)):
        print('Error loading the configuration file')
        w.close()
        return
    
    w.show()
    sys.exit(app.exec_())
    
##load values to config window
def load(about, ref, debug, nrnez):
    ret = False
    fin = None
    try:
        ##if the config file doesn't exist for some reason, we still want to run so we can create it
        if(not os.path.exists(jsonPath)):
            ret = True
        else:
            fin = open(jsonPath, 'r')
            data = json.loads(fin.read())
            isValid = validate(data)
            if(isValid):
                about.setText(data['about'])
                ref.setText(data['reference'])
                debug.setChecked(data['debug'])
                nrnez.setText(data['nrnez'])
                ret = True
    except Exception as ex:
        print('Error loading the configuration file: ' + str(ex))
    finally:
        if(not fin is None):
            fin.close()
        return ret

##save config values
def saveClicked(w, about, ref, debug, nrnez):
    fout= None
    cs = genChecksum(about.toPlainText() + ref.toPlainText() + str(debug.isChecked()) + nrnez.text())
    data = {'about' : about.toPlainText(),
            'reference' : ref.toPlainText(),
            'debug': debug.isChecked(),
            'nrnez': nrnez.text(),
            'checksum' : cs
    }
    try:
        fout = open(jsonPath, 'w')
        fout.write(json.dumps(data))
    except Exception as ex:
        print('Error saving the configuration file: ' + str(ex))
    finally:
        if(fout is not None):
            fout.close()
        w.close()

##generate checksum value
def genChecksum(text):
    enc = text.encode('utf-8')
    hashobj = hl.md5()
    hashobj.update(enc)
    return hashobj.hexdigest()

##validate checksum value
def validate(data):
    cs = genChecksum(data['about'] + data['reference'] + str(data['debug']) + data['nrnez'])
    if(cs == data['checksum']):
        return True
    return False

###get .nrnez file name
def nrnezLoad(w, nrnez):
    try:
        fname = QFileDialog.getOpenFileName(w, 'Open File', '~/', "NRNEZ (*.nrnez)")[0]
        if(fname is None or fname == ''):
            return
        nrnez.setText(fname)
    except Exception as ex:
        print("Error loading .nrnez file: " + str(ex)) 

##load values into NRN_EZ
def loadValues():
    fin = None
    try:                                                                                 
        if(not os.path.exists(jsonPath)):
            gv.configErr = 'Error opening configuration file. File does not exist'
            return False
        else:
            fin = open(jsonPath, 'r')
            data = json.loads(fin.read())
            isValid = validate(data)
            if(isValid):
                gv.aboutText = data['about']
                gv.refText = data['reference']
                gv.debug = data['debug']
                gv.nrnezPath = data['nrnez']
            return True
    except Exception as ex:
        gv.configErr =  'Error loading the configuration file: ' + str(ex)
        return False
    finally:
        if fin is not None:
            fin.close()
