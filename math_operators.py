import csv_operators
import math
import copy

def get_count(dict):
    return len(dict.keys())-1

def get_min(dict, field, csv_name):
    min_keys=[]
    old_dict=copy.deepcopy(dict)
    #selects keys and values of field from args
    temp_dict = csv_operators.select(old_dict, [field], csv_name)
    #creates list of keys 
    keys=list(temp_dict.keys())[1:]
    #creates list of values
    values=list(temp_dict.values())[1:]

    #gets min value 
    min_value = min(values)
    
    #gets keys which have same value as min
    for i, x in enumerate(values):
        if x == min_value:
            min_keys.append(keys[i])     

    new_dict={}
    new_dict[list(old_dict.keys())[0]] = list(old_dict.values())[0]
    for k in min_keys:
        v = old_dict.get(k)
        new_dict[k] = v
    
    return new_dict

def get_max(dict, field, csv_name):
    max_keys=[]
    old_dict=copy.deepcopy(dict)
    #selects keys and values of field from args
    temp_dict = csv_operators.select(old_dict, [field], csv_name)
    #creates list of keys 
    keys=list(temp_dict.keys())[1:]
    #creates list of values
    values=list(temp_dict.values())[1:]

    #gets max value 
    max_value = max(values)
    
    #gets keys which have same value as max
    for i, x in enumerate(values):
        if x == max_value:
            max_keys.append(keys[i])     

    new_dict={}
    new_dict[list(old_dict.keys())[0]] = list(old_dict.values())[0]
    for k in max_keys:
        v = old_dict.get(k)
        new_dict[k] = v
    
    return new_dict

def get_avg(dict, field, csv_name):
    old_dict=copy.deepcopy(dict)
    #select values for field specified without the key
    temp_dict = csv_operators.select(old_dict, [field], csv_name)
    #store dictionary values within a list
    temp_values = list(temp_dict.values())[1:]
    values = []
    for v in temp_values:
        if v[0] != '':
            values.append(v[0])
        else:
            values.append('0')
    #convert all values within list to float
    values = list(map(float, values))
    #return mean 
    return float("{:.2f}".format(sum(values)/len(values)))

def get_stand_dev(dict, field, csv_name):
    old_dict = copy.deepcopy(dict)
    #call get_avg method to calculate mean
    mean = get_avg(old_dict, field, csv_name)
    #find each score deviation from mean
    temp_dict = csv_operators.select(old_dict, [field], csv_name)
    temp_values = list(temp_dict.values())[1:]
    values = []
    for v in temp_values:
        if v[0] != '':
            values.append(v[0])
        else:
            values.append('0')
    #convert all values within list to float
    values = list(map(float, values))

    dev_from_mean=[]
    for v in values:
        dev_from_mean.append(v-mean)
    #square each deviation
    dev_from_mean_sqred=[]
    for v in dev_from_mean:
        x = v ** 2
        dev_from_mean_sqred.append(x)

    #find sum of squares
    sum_of_squares = sum(dev_from_mean_sqred)
    #find variance
    denom = get_count(old_dict)
    variance = sum_of_squares/denom

    return float("{:.2f}".format(math.sqrt(variance)))