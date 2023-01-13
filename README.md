# TcellsInBrain
Data/HeathLabData.xlsx contains data from Ghazanfari 2021.


Data from Harris 2012 is are freely available from Dr. Harris on request.


The provided bash files provide the commands and sequence used for this project. Use as examples.


Note: Data to be used with scripts is to be in the following format:
movie,time (s),track ID,x,y,z


Scripts are to be ran in the following order. Data files regarding HeathLabData.xlsx were separated by day and cell type, and re-merged (cell type still kept separated) after reformatting. See bash files for example of procedure.

Scripts/reformattime.py [original data file] [original time frequency] [new time frequency] - Changes time stamps to a common frequency

If wanting to merge data:
Scripts/mergefiles.py [directory] [output file] - Merges all csv's in directory to a common csv

Scripts/compiledata.py [reformatted data file] [time frequency] - Compiles all data & analytics

Scripts/steplengthanalysis.py [output file] - Runs simulations for possible muRun and muPause combinations to demonstrate step-length tail analysis is robust in determing Levy vs Non-Levy behavior.

Scripts/brainpaperfigures.py - Creates figures used in the paper. Directories will have to be modified within the file for this script to function properly.


====================

Other Tools:

Scripts/simulate.py [output file] [# of cells] [# of steps] [muRun] [muPause] [kappa] [optional: pausePattern] - creates simulated cells based on parameters. Possible pausePattern options as 'alternate' and 'random' with the default being 'alternate'.

Scripts/resampledata.py [file] [new sampling interval] - Resamples the data at given sampling interval
