#!/usr/bin/env python3

import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)

infile = 'alldata.csv'

df = pd.read_csv(infile)
print(df.dtypes)
df2 = df[df['trial_type'] == 'exp']
print(df2['trial'].groupby([df2['sub'], df2['blocktyp']]).count().unstack())
df.loc[(df['sub'] == 317) & (df['experimenter'] == 'SN'), 'sub'] = 137
df.loc[(df['sub'] == 514) & (df['experimenter'] == 'AGM'), 'sub'] = 154
df2 = df[df['trial_type'] == 'exp']
print(df2['trial'].groupby([df2['sub'], df2['blocktyp']]).count().unstack())
