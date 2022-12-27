import sys
import os
import glob
import pandas as pd

os.chdir(sys.argv[1])
all_filenames = sorted([i for i in glob.glob('*.csv')])
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

combined_csv.to_csv(sys.argv[2], index=False)
