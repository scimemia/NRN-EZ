10/26/2022 Version 1.1.5:
-Fixed relative path references to absolutee paths. 

10/10/2022 Version 1.1.4:
-Redid GUI to a relative layout, resizing keeps elements in place. 
-Changed title bar to 'NRN-EZ'
-Added feature to run nrnivmodl. 

7/21/2022 Version 1.1.3:
-Fixed issue with reload button not working with the number of runs feature added.
-Fixed a small bug when editting/deleting table rows

2/5/2022 Verison 1.1.2:
-Added a field to set the number of times to run the input data. Effectively, the number of times the user would hit the "Run" button, automated.
-Added a field to the .nrnez file interface to include the run number field added.
-Decided to only plot the last run on the graph after the files are generated. 

6/10/2021 Version 1.1.1
-Finished the I-Step duration fields. This includess tabbinng, editting, and the adding fields to the interface file. 
-Updated the interface file logic.

5/20/2021 Version 1.1.0
-Defined a '.nrnez' file format for loading default values into Neuron-EZ.
-Added new module to the code for loading .nrnez files.
-Added a field to the configuration menu for auto-loading .nrnez files on startup.
-Added Uniform and Poisson options for the duration field under I-Step, including the GUI elements and the generation logic.

4/29/2021 - Version 1.0.8
-Changed "Mod File" button label to ".mod File".
-Changed morphology graph to properly scale units.
-Added a 'Distance' variable for the Single Location to allow randomly choosing a single point at a given distance. 

3/8/2021 - Version 1.0.7
-Fixed issue with pickling data when a segment is highlighted in the graph.
-Changed digits allowed after the decimal point from 2 to 10. 

3/3/2021 - Version 1.0.6
-Added ability to highight a segment in the morphology manually by clicking once on both sides to select it. 
-Removed 'Edit' buttons. Deemed unnecessary with the ability to edit by clicking the row of data. 
-Added functionality to remove .log files older than 1 week.
-Added comments to each file.
-Added logging to each file.
-Added error handling to the code.
-Fixed tabbbing for synaptic and custom weight options.

12/5/2020 - Version 1.0.5
-Changed Location mean/sd and Time onset text edits to accept decimal numbers. 
-Added units label to Location mean label. 
-Fixed application to copy Custom mod files to output directory. 
-Changed the highlight color for apical segments to a darker yellow 
-Changed Poisson labels to 'Multiple Poisson'
-Changed tables to auto edit on selecting the data row.
-Added a configuration menu to support configurable variables without reving the code. 

11/16/2020 - Version 1.0.4
-Fixed issue with inputs being displayed incorrectly for the Soma sections.
-Fixed issue with incorrect outputs in Neuron. 
-Fixed GUI issues. 
-Added version number to code, and to comments of generated output.

10/17/2020 - Version 1.0.3
-Fixed issue with Morphologies that don't have expected segments.

9/29/2020 - Version 1.0.2
-Aligned the 'S.D.' label to the 'Mean' label in the Location and Timing sections
-Fixed issue with the custom.tmplt file.

8/24/2020 - Version 1.0.1
-Fixed weight Poisson generation error.
-Fixed timing Multiple Uniform generation error.
-Added check for canceling reload. 

8/23/2020 - Version 1.0.0
-Initial build
