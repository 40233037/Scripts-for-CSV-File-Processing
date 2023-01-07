import sys
import csv_handler

#read in csv files from command line
csv1 = csv_handler.read_csv(sys.argv[1])
csv2 = csv_handler.read_csv(sys.argv[2])

#Compare to see if dictionaries are the same
if csv1 == csv2:
    print("No differences between the CSVs")
else:
    print("Differences between the CSVs")