python3 Scripts/reformattime.py BrainPaper/HeathLabCD4/OriginalData/movie1cd4.csv 30.68 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD4/OriginalData/movie2cd4.csv 30 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD4/OriginalData/movie3cd4.csv 32.76 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD4/OriginalData/movie4cd4.csv 30 30
python3 Scripts/reformattime.py BrainPaper/HeathLabCD4/OriginalData/movie5cd4.csv 30 30
mkdir BrainPaper/HeathLabCD4/ReformattedData
mkdir BrainPaper/HeathLabCD4/Analysis/
mkdir BrainPaper/HeathLabCD4/Analysis/30/
mv BrainPaper/HeathLabCD4/OriginalData/**reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD4/ReformattedData/ heathdatacd4.csv
mv BrainPaper/HeathLabCD4/ReformattedData/heathdatacd4.csv BrainPaper/HeathLabCD4/Analysis/30/heathdatacd4.csv
python3 Scripts/compiledata.py BrainPaper/HeathLabCD4/Analysis/30/heathdatacd4.csv 30.0

mkdir BrainPaper/HeathLabCD4/ReformattedData/6.5
mkdir BrainPaper/HeathLabCD4/ReformattedData/7
mkdir BrainPaper/HeathLabCD4/Analysis/6.5d
mkdir BrainPaper/HeathLabCD4/Analysis/6.5d/30/
mkdir BrainPaper/HeathLabCD4/Analysis/7d
mkdir BrainPaper/HeathLabCD4/Analysis/7d/30/

cp BrainPaper/HeathLabCD4/ReformattedData/movie1cd4reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/6.5/movie1cd4reformatted.csv
cp BrainPaper/HeathLabCD4/ReformattedData/movie2cd4reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/6.5/movie2cd4reformatted.csv
cp BrainPaper/HeathLabCD4/ReformattedData/movie3cd4reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/6.5/movie3cd4reformatted.csv
cp BrainPaper/HeathLabCD4/ReformattedData/movie4cd4reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/7/movie4cd4reformatted.csv
cp BrainPaper/HeathLabCD4/ReformattedData/movie5cd4reformatted.csv BrainPaper/HeathLabCD4/ReformattedData/7/movie5cd4reformatted.csv
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD4/ReformattedData/6.5/ heathdata6.5cd4.csv
python3 Scripts/mergefiles.py BrainPaper/HeathLabCD4/ReformattedData/7/ heathdata7cd4.csv
mv BrainPaper/HeathLabCD4/ReformattedData/6.5/heathdata6.5cd4.csv BrainPaper/HeathLabCD4/Analysis/6.5d/30/heathdata6.5cd4.csv
mv BrainPaper/HeathLabCD4/ReformattedData/7/heathdata7cd4.csv BrainPaper/HeathLabCD4/Analysis/7d/30/heathdata7cd4.csv
python3 Scripts/compiledata.py BrainPaper/HeathLabCD4/Analysis/6.5d/30/heathdata6.5cd4.csv 30.0
python3 Scripts/compiledata.py BrainPaper/HeathLabCD4/Analysis/7d/30/heathdata7cd4.csv 30.0
