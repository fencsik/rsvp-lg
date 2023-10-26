#!/usr/bin/env python3

import os, sys, argparse

output_file = 'alldata.csv'
header_template = None
variable_index = None
first_file = True
warn_on_mismatch = False
output_headers = False

class ListMismatch(Exception):
    pass

def MatchListOrder(original_list, new_list):
    # indentify an ordering for new_list that matches sequence of original_list
    index = [-1] * len(original_list)
    for i in range(len(index)):
        try:
            j = new_list.index(original_list[i])
        except ValueError as err:
            raise ListMismatch(original_list[i])
        index[i] = j
    return index

def ProcessHeader(header_items):
    global header_template, variable_index
    if header_template == None:
        header_template = header_items
        variable_index = list(range(len(header_template)))
    elif header_template == header_items:
        variable_index = list(range(len(header_template)))
    else:
        variable_index = MatchListOrder(header_template, header_items)

def OutputHeaders(infile):
    with open(infile, 'r') as f:
        header_line = f.readline()
        print('{},{}'.format(infile, header_line), end="")

def ProcessDataFile(infile):
    global output_file
    global first_file
    first_line = True
    print(infile)
    with open(infile, 'r') as fin:
        with open(output_file, 'a') as fout:
            for line in fin:
                line_items = line.rstrip(', \n').split(',')
                if first_line:
                    # current line is the 1st line
                    ProcessHeader(line_items)
                    first_line = False
                    if first_file:
                        # save the first line the first time
                        fout.write(','.join([line_items[i] for i in variable_index]) + '\n')
                        first_file = False
                else:
                    # we've handled the 1st line already
                    fout.write(','.join([line_items[i] for i in variable_index]) + '\n')

def ProcessDataDirectory(dirname):
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
                if output_headers:
                    OutputHeaders(f)
                    continue
                try:
                    ProcessDataFile(f)
                except ListMismatch as err:
                    print("Cannot find variable '{}' in {}".format(err, f))
                    if not warn_on_mismatch:
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
    parser.add_argument("-a", "--append",
                        help="append to output file instead of overwriting",
                        action="store_true")
    parser.add_argument("--headers",
                        help="output headers prefaced by filename",
                        action="store_true")
    parser.add_argument("-o", "--output",
                        help="override default output file name")
    parser.add_argument("-w", "--warn-on-mismatch",
                        help="issue warning instead of exiting when headers mismatch",
                        action="store_true")
    args = parser.parse_args()
    global output_file
    if args.output != None:
        output_file = args.output
    if (not args.append) and os.path.isfile(output_file):
        os.remove(output_file)
    if args.warn_on_mismatch:
        global warn_on_mismatch
        warn_on_mismatch = True
    if args.headers:
        global output_headers
        output_headers = True
    ProcessDataDirectory(args.dirname)


if __name__ == '__main__':
    Main()
