###################################################################
####
#### Version: 1.1.4
#### Date: 10/10/2022
#### Description: This file contains the starting point of the application and handles command line arguments, as well as OS specific code. 
#### Author: Evan Cobb
####
###################################################################
 
import sys
import globvar as gv
from gui import window
import config
from errorLogger import *
import platform

############ OS specific code goes here##############

if platform.system() == 'Windows':
    gv.nrnscript = ['.\incl\nrn.bat']
else: ##mac and linux
    gv.nrnscript = ['./incl/nrn.sh']


############

############handle command line args#############
if len(sys.argv) > 1:
    if sys.argv[1] == '-d':   ##set debug mode
        gv.debug = True
    if sys.argv[1] == '-v':   ##print current version of the application
        print('NRN-EZ Version: ' + gv.version)
        exit(0)
    if sys.argv[1] == '-config':   ##launch the configuration window
        config.window()
        exit(0)
        
########### Load the configuration file#########
if(config.loadValues()):
    logRun('Config file loaded successfully!\n\t Values:\n\t\t About:: '
           + gv.aboutText + '\n\t\t Reference:: ' + gv.refText
           + '\n\t\t Debug:: ' + str(gv.debug))
else:
    logErr(gv.configErr, 'config.loadValues()')
    gv.configErr = ''
    
########### clean up log files older than 1 week#################
cleanLogFiles()

############ Run the application #################
window()
