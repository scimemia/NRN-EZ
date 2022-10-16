###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This file contains global variables used throughout the application.
#### Author: Evan Cobb
####
###################################################################
 
from PyQt5.QtGui import QColor

graphWin = None ##window used to display the morphology
morphObj = None ## object that holds the loaded morphology
inPoints = []  ##array to hold the points from the morphology
lastPoint = None  ##holds the last point clicked on the graph
lines = [] ##array of line segments imported from the morphology
#### weight list view
weightInputs = []  ##array of all weight objects added 
model = None ##holds reference to the weight table view data
editMode = None  ##flag to indicate if a weight object is being editted
wTable = None  ##holds refence to the weight table view window
#### all list view
experiments = [] ##array of all the experiment objects
allModel = None  ##holds reference to the experiment table view data
color = QColor(0,0,0)  ##color of the current experiment's inputs for the morphology
allEditMode = None ##flag to indicate if an experiment is being editted
inputTable = None  ##holds reference to the experiment table view window
#### error logging
debug = False ##flag to indicate if we are in debug mode
runFile = None  ##holds runtime log file object
errorFile = None  ##holds error log file object
debugFile = None  ##holds debug log file object
#### meta data
version = '1.1.4' ##current version as a string
vMajor = 1  ##current major version as an int
vMinor = 1  ##current minor version as an int
vBuild = 4  ##current build version as an int
aboutText = ''  ##about text
refText = ''  ##reference text
configErr = ''  ##holds error string for configuration menu
nrnezPath = '' ##.nrnez file path from config file.
