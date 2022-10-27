###################################################################
####
#### Version: 1.1.5
#### Date: 10/26/2022
#### Description: This files contains functions for logging, error handling, pickling, and other global functions.
#### Author: Evan Cobb
####
###################################################################
 
import datetime as dt
import traceback
import pickle
from PyQt5.QtWidgets import QMessageBox
import globvar as gv
import os
logPath = os.path.dirname(os.path.realpath(__file__)) + '/logs/'

##function to write exceptions to error log.
def logErr(err, func):
    errMsg = dt.datetime.now().strftime("%H_%M_%S.%f") + "-- The following error occurred in " + func + " :: " + err + "\n"
    try:
        if gv.errorFile is None:
            gv.errorFile = open(logPath + "error_" + dt.datetime.now().strftime("%Y_%m_%d") + ".log", "a")
        gv.errorFile.write(errMsg)
        traceback.print_exc(file=gv.errorFile)
    except Exception as ex:
        print("Error creating error log file.\n" + str(ex))

##function to write information to the runtime log.
def logRun(msg):
    timestamp = dt.datetime.now().strftime("%H_%M_%S.%f") + "-- "
    try:
        if gv.runFile is None:
            gv.runFile = open(logPath + "runtime_" + dt.datetime.now().strftime("%Y_%m_%d") + ".log", "a")
        gv.runFile.write(timestamp + msg + "\n")
    except Exception as ex:
        print("Error creating runtime log file.\n" + str(ex))

##function to write information to debug log
def logDebug(msg):
    ##if not in debug mode, no log writing occurs
    if not gv.debug:
        return
    timestamp = dt.datetime.now().strftime("%H_%M_%S.%f") + "-- "
    try:
        if gv.debugFile is None:
            gv.debugFile = open(logPath + "debug_" + dt.datetime.now().strftime("%Y_%m_%d") + ".log", "a")
            print("created debug")
        gv.debugFile.write(timestamp + msg + "\n")
    except Exception as ex:
        print("Error creating debug log file.\n" + str(ex))


def cleanLogFiles():
    now = dt.datetime.now()
    try:
        files = os.listdir(logPath)
        for f in files:
            if(f[-4:] == '.log'):
                parts = f[:-4].split('_')
                date = dt.datetime.strptime(parts[1] + '_' + parts[2] + '_' + parts[3], '%Y_%m_%d')
                if((now - dt.timedelta(days = 7)) > date):
                    os.remove(logPath + f)
                    
    except Exception as ex:
        print("Error cleaning log files" + str(ex))

######### A few relevant global functions ############

###message box popup, mainly for errors
def newMsgBox(text, details=None, title = 'Error'):
    logDebug("errorLogger.py::mewMsgBox() called. Message text: " + text + "\n")
                
    msg = QMessageBox()
    msg.setText(text)
    if(details):
        msg.setDetailedText(details)
    msg.setWindowTitle(title)
    msg.exec_()

##pickle data for reloading sessions
def savePickle(path):
    logDebug("errorLogger.py::savePickle() called. Path: " + path + "\n")
    
    try:
        pfile = open(path, "wb")
        pickle.dump([gv.morphObj, gv.experiments], pfile)
        pfile.close()
    except Exception as ex:
        logErr(str(ex), 'savePickle( ' + path + ' )')
        newMsgBox("Error pickling data", str(ex))

##load pickled data
def loadPickle(path):
    logDebug("errorLogger.py::loadPickle() called. Path: " + path +"\n")
                
    try:
        pfile = open(path, "rb")
        arr = pickle.load(pfile)
        gv.morphObj =arr[0] 
        gv.experiments = arr[1]
        pfile.close()
    except Exception as ex:
        logErr(str(ex), 'loadPickle( ' + path + ' )')
        newMsgBox("Error loading the pickle file: " + path, str(ex))
        
##close log files before exiting 
def closingApp():
    if gv.runFile is not None:
        gv.runFile.close()
    if gv.errorFile is not None:
        gv.errorFile.close()
    if gv.debugFile is not None:
        gv.debugFile.close()

##generic comment for generated files
def getComments():
    logDebug("errorLogger.py::getComment() called.\n")
    return ('//This file was generated using NRN-EZ\n'
            + '//Reference: ' + sanitize(gv.refText) + '\n'
            + '//Creation time: ' + dt.datetime.now().strftime("%H:%M:%S")
            + '  ' + dt.datetime.now().strftime("%m/%d/%Y") + '\n'
            + '//Version: ' + gv.version + '\n')

##this is for potential newline chars used in the config, put the // in front of them
def sanitize(string):
    logDebug("errorLogger.py::sanitize() called. Text: " + string +"\n")
    buf = string.split("\n")
    ret = buf[0]
    buf = buf[1:]
    for b in buf:
        ret = ret + '\n//// ' + b
    return ret
