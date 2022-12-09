# NRN-EZ

**SYNOPSIS AND MOTIVATION**

NRN-EZ is a software that allows to distribute synaptic inputs onto digitally reconstructed neurons. With NRN-EZ, users can select the location, strength, and activation time of a population of synaptic inputs. These inputs can be in selected sub-cellular compartments, identified by the user or generated through NRN-EZ itself. The location, strength and activation time can be the same for all inputs or vary according to uniform or Poisson distributions. NRN-EZ provides an intuitive graphical user interface to generate code that can then be integrated with other .hoc files, typically used when running multi-compartmental models of synaptic integration and cell excitability using software like NEURON. This framework allows users to test mechanistic hypothesis quickly and accurately for further experimental validation, without necessarily having extensive background in the .hoc programming language.

**OVERVIEW**

NRN-EZ is an open-source software, able to generate output files that can then be used for running NEURON simulations. It has an intuitive interface that lowers the barrier for running computer simulations, especially in young trainees with minimal programming skills. NRN-EZ is compatible with Linux, Mac OS and Microsoft Windows operating systems. NRN-EZ was built using the Python language and the PyQt and PyQtGraph libraries. Source code and executable, standalone versions of NRN-EZ are available for Linux (Ubuntu and Pop!_OS), Mac OS, and Microsoft Windows platforms.

•	Linux (Ubuntu 18.04.5 LTS):
NRNEZ_Installation_Media_Ubuntu.zip

•	Linux (Pop!_OS 18.04 LTS):
NRNEZ_Installation_Media_Pop.zip

•	Mac OS (Monterey 12.5.1):
NRNEZ_Installation_Media_Mac.zip

•	Microsoft Windows (Win 10):
NRNEZ_Installation_Media_Win.zip

The Sample neurons folder contains an .swc file, a description of the settings used to control the spatial distribution and time of onset of multiple synaptic inputs, and the corresponding output file generated by NRN-EZ. 

**INSTALLATION FOR VERSION 1.1.6**

NRN-EZ was built with PyInstaller 3.6, and requires the following languages and libraries:

•	Python 3.6.9 and higher (currently up to 3.10)

•	PyQt 5.10.1

•	PyQtGraph 0.11.0

Installation instructions for Linux (Ubuntu and Pop!_OS): download the Linux zip file and, from the command window, run a bash command for the install.sh file, in the corresponding installation folder. 

Installation instructions for Mac OS: download the Mac zip file and copy the NRN-EZ app to the Applications folder. 

Installation instructions for Windows: download the Win zip file and run the installation wizard.


**NOTES FOR LINUX USERS**

Users need to execute the nrnez.py file to run the NEURON simulations using the Python output of NRN-EZ. This opens the NEURON GUI and imports the simulation settings. This can be done from the shell without using the sudo command if NEURON was installed with the pip command in any location without using sudo. If instead NEURON was installed in a location that required the use of the sudo command, then sudo should also be used to run the nrnez.py file.


**TESTS**

To test NRN-EZ, load the .swc file containing the description of the cell morphology, which is in the Samples folder. Then, fill all fields that describe the spatiotemporal pattern of activation of the synaptic inputs and run the application according to the instructions described in the Instructions folder.

**CONTRIBUTORS**

NRN-EZ was created by: Evan A. Cobb (evancbb@gmail.com)

NRN-EZ was tested and validated by: Maurice A. Petroccione (reecepetroccione@gmail.com) 

NRN-EZ was supervised by Annalisa Scimemi (scimemia@gmail.com; ascimemi@albany.edu)

For support and questions, please contact Annalisa Scimemi (scimemia@gmail.com)
All work was funded by SUNY Albany, SUNY Albany Research Foundation and NSF IOS1655365 and IOS2011998 to A.S.

**HISTORY**

11-2019 – The first version of NRN-EZ was created by Evan Cobb and tested by Maurice A. Petroccione and Annalisa Scimemi. This version is compatible with Microsoft Windows 10, Mac OS12 and Linux Ubuntu 22.04 platforms and used Python 3.6.9, PyQt 5.10.1 and PyQtGraph 0.11.0

**LICENSE**

Please review the terms and conditions of the license in the LICENSE_NPOSL-3.0 section of this repository before downloading the NRN-EZ software. By downloading the NRN-EZ software from this site you agree to be legally bound by the terms and conditions of the Open Source Initiative Non-Profit Open Software License 3.0
(NPOSL-3.0; https://tldrlegal.com/license/non-profit-open-software-license-3.0-(nposl-3.0)).
