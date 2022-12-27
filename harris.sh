python3 Scripts/reformattime.py BrainPaper/Harris/OriginalData/original22.csv 22 20
python3 Scripts/reformattime.py BrainPaper/Harris/OriginalData/original19.25.csv 19.25 20
mkdir BrainPaper/Harris/ReformattedData
mv BrainPaper/Harris/OriginalData/**reformatted.csv BrainPaper/Harris/ReformattedData/
python3 Scripts/mergefiles.py BrainPaper/Harris/ReformattedData/ harrisdata20.csv
mkdir BrainPaper/Harris/Analysis/
mkdir BrainPaper/Harris/Analysis/20/
mv BrainPaper/Harris/ReformattedData/harrisdata20.csv BrainPaper/Harris/Analysis/20/harrisdata20.csv
python3 Scripts/compiledata.py BrainPaper/Harris/Analysis/20/harrisdata20.csv 20.0

mkdir BrainPaper/Harris/Analysis/22/
cp BrainPaper/Harris/OriginalData/original22.csv BrainPaper/Harris/Analysis/22/harris22.csv
python3 Scripts/compiledata.py BrainPaper/Harris/Analysis/22/harris22.csv 22.0

mkdir BrainPaper/Harris/Analysis/19.25/
cp BrainPaper/Harris/OriginalData/original19.25.csv BrainPaper/Harris/Analysis/19.25/harris19.25.csv
python3 Scripts/compiledata.py BrainPaper/Harris/Analysis/19.25/harris19.25.csv 19.25
