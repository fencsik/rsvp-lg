#!/usr/bin/env python3

import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)

infile = 'alldata.csv'

df = pd.read_csv(infile)
df = df[df['trial_type'] == 'exp']
print(df['trial'].groupby([df['sub'], df['blocktyp']]).count().unstack())
