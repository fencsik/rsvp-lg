#!/usr/bin/env python3

import os, sys, argparse
import numpy as np
import pandas as pd

# variables to save
variables = [
    'exp',
    'ver',
    'mod-utc',
    'sub',
    'experimenter',
    'datetime',
    'blocktyp',
    'sess',
    'trial',
    'trial_type',
    'trial_time',
    't1_level',
    't2_level',
    't2_lag',
    'global_letters',
    'local_letters',
    't1_pos',
    't1',
    't1_corr',
    't1_resp',
    't1_acc',
    't2',
    't2_corr',
    't2_resp',
    't2_acc',
    't1_rt',
    't2_rt'
    ]
variables_set = set(variables)

# other global variables
output_file = 'alldata.csv'
first_file = True
warn_missing = False
output_var_names = False

class ListMismatch(Exception):
    pass

def OutputVarNames(infile):
    with open(infile, 'r') as f:
        header_line = f.readline()
        print('{},{}'.format(infile, header_line), end="")

def ProcessDataFile(infile):
    global first_file, all_data
    print(infile)
    d = pd.read_csv(infile)
    if variables_set <= set(d.columns):
        if first_file:
            first_file = False
            all_data = d[variables]
        else:
            all_data = pd.concat([all_data, d[variables]])
    else:
        raise ListMismatch(variables_set - set(d.columns))

def ProcessDataDirectory(dirname):
    global output_var_names
    if os.path.exists(dirname):
        files = os.listdir(dirname)
        files.sort()
        for f in files:
            if f in ('.DS_Store'):
                continue
            else:
                f = os.path.join(dirname, f)
            if os.path.isdir(f):
                ProcessDataDirectory(f)
            elif os.path.isfile(f) and (os.path.splitext(f)[1] == ".csv"):
                if output_var_names:
                    OutputVarNames(f)
                    continue
                try:
                    ProcessDataFile(f)
                except ListMismatch as err:
                    print("file {} is missing these variables: {}".format(f, err))
                    if not warn_missing:
                        sys.exit()
    else:
        print('directory {} not found'.format(dirname))

def Main():
    parser = argparse.ArgumentParser(
        prog='gatherdata.py',
        description="""
        gather data files into one csv file, making sure variable names match across files.
        """)
    parser.add_argument("dirname", nargs="?",
                        default=".",
                        help="directory name with data files (required)")
    parser.add_argument("-v", "--var-names",
                        help="output variable names prefaced by filename",
                        action="store_true")
    parser.add_argument("-o", "--output",
                        help="override default output file name")
    parser.add_argument("-w", "--warn-missing",
                        help="issue warning instead of exiting when a variable name is missing",
                        action="store_true")
    args = parser.parse_args()
    if args.output != None:
        global output_file
        output_file = args.output
    if args.warn_missing:
        global warn_missing
        warn_missing = True
    if args.var_names:
        global output_var_names
        output_var_names = True
    ProcessDataDirectory(args.dirname)
    if not output_var_names:
        all_data.to_csv(output_file, index=False)

if __name__ == '__main__':
    Main()
