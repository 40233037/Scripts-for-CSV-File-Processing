import string
import random
import csv_handler 

def getStrVals(str_fields):
    str_vals=[]
    for field in str_fields:
        str_vals.append(''.join(random.choice(string.ascii_lowercase) for i in range(5)))
    return str_vals

def getNumVals(num_fields):
    if (num_fields != []):
        num_vals=[] 
        for fields in num_fields:
            num_vals.append(''.join(random.choice(string.digits) for i in range(2)))
        return num_vals
    else:
        return []

def create_csv(str_fields, num_fields, num_records, filename):
    new_csv={}
    
    if (num_fields != []):
        for i in range(num_records):
            new_csv['student_number'] = str_fields + num_fields
            new_csv[str(i)] = getStrVals(str_fields)+getNumVals(num_fields)

    else:
        for i in range(num_records):
            new_csv['student_number'] = str_fields + num_fields
            new_csv[str(i)] = getStrVals(str_fields)

    csv_handler.write_csv(filename, new_csv)

create_csv(['first','last','prac'],['mark'], 100000, 'Read_Perf_Test_100000.csv')