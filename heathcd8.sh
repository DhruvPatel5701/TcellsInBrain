python3 Scripts/reformattime.py BrainPaper/HeathLabCD8/OriginalData/movie1cd8.csv 30.68 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD8/OriginalData/movie2cd8.csv 30 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD8/OriginalData/movie3cd8.csv 32.76 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD8/OriginalData/movie4cd8.csv 30 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD8/OriginalData/movie5cd8.csv 30 30
mkdir BrainPaper/HeathLabCD8/ReformattedData
mkdir BrainPaper/HeathLabCD8/Analysis/
mkdir BrainPaper/HeathLabCD8/Analysis/30/
mv BrainPaper/HeathLabCD8/OriginalData/**reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD8/ReformattedData/ heathdatacd8.csv
mv BrainPaper/HeathLabCD8/ReformattedData/heathdatacd8.csv BrainPaper/HeathLabCD8/Analysis/30/heathdatacd8.csv
python3 Scripts/compiledata.py BrainPaper/HeathLabCD8/Analysis/30/heathdatacd8.csv 30.0

mkdir BrainPaper/HeathLabCD8/ReformattedData/6.5
mkdir BrainPaper/HeathLabCD8/ReformattedData/7
mkdir BrainPaper/HeathLabCD8/Analysis/6.5d
mkdir BrainPaper/HeathLabCD8/Analysis/6.5d/30/
mkdir BrainPaper/HeathLabCD8/Analysis/7d
mkdir BrainPaper/HeathLabCD8/Analysis/7d/30/

cp BrainPaper/HeathLabCD8/ReformattedData/movie1cd8reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/6.5/movie1cd8reformatted.csv
cp BrainPaper/HeathLabCD8/ReformattedData/movie2cd8reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/6.5/movie2cd8reformatted.csv
cp BrainPaper/HeathLabCD8/ReformattedData/movie3cd8reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/6.5/movie3cd8reformatted.csv
cp BrainPaper/HeathLabCD8/ReformattedData/movie4cd8reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/7/movie4cd8reformatted.csv
cp BrainPaper/HeathLabCD8/ReformattedData/movie5cd8reformatted.csv BrainPaper/HeathLabCD8/ReformattedData/7/movie5cd8reformatted.csv
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD8/ReformattedData/6.5/ heathdata6.5cd8.csv
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD8/ReformattedData/7/ heathdata7cd8.csv
mv BrainPaper/HeathLabCD8/ReformattedData/6.5/heathdata6.5cd8.csv BrainPaper/HeathLabCD8/Analysis/6.5d/30/heathdata6.5cd8.csv
mv BrainPaper/HeathLabCD8/ReformattedData/7/heathdata7cd8.csv BrainPaper/HeathLabCD8/Analysis/7d/30/heathdata7cd8.csv
python3 Scripts/compiledata.py BrainPaper/HeathLabCD8/Analysis/6.5d/30/heathdata6.5cd8.csv 30.0
python3 Scripts/compiledata.py BrainPaper/HeathLabCD8/Analysis/7d/30/heathdata7cd8.csv 30.0
