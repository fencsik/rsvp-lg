#!/usr/bin/env python3

import os, sys, argparse

output_file = 'alldata.csv'
header = None
first_file = True
warn_on_mismatch = False
output_headers = False

class HeaderMismatch(Exception):
    pass

def ProcessHeader(header_line):
    global header
    header_items = header_line.rstrip(', \n').split(',')
    if header == None:
        header = header_items
    elif header != header_items:
        raise HeaderMismatch()

def ProcessDataFile(infile):
    global output_file
    global first_file
    first_line = True
    with open(infile, 'r') as fin:
        with open(output_file, 'a') as fout:
            for line in fin:
                if first_line:
                    # current line is the 1st line
                    ProcessHeader(line)
                    first_line = False
                    if first_file:
                        # save the first line the first time
                        fout.write(line)
                        first_file = False
                else:
                    # we've handled the 1st line already
                    fout.write(line)

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
                try:
                    ProcessDataFile(f)
                except HeaderMismatch:
                    print('header mismatch in {}'.format(f))
                    global warn_on_mismatch
                    if not warn_on_mismatch:
                        sys.exit()
    else:
        print('directory {} not found'.format(dirname))

def Main():
    parser = argparse.ArgumentParser(
        prog='gatherdata.py',
        description="gather data files")
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
    parser.add_argument("--warn-on-mismatch",
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
