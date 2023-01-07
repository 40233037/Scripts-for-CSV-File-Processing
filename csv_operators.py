import operator
import copy

ops = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

#obtains headers from a dictionary
def getHeaders(dict):
    key_header = list(dict.keys())[0]
    non_key_headers = list(dict.values())[0]
    headers = []
    headers.append(key_header)
    headers.extend(non_key_headers)
    return headers


def join(dict1, dict2, csv1_name, csv2_name):
    if list(dict1.keys())[0] == list(dict2.keys())[0]:
        new_dict=copy.deepcopy(dict1)
        uniqueKeysCSV2 = []
        #check if each key from csv2 is present in csv1 - if present extend dictionary else add to list of keys which are unique
        for k, v in dict2.items():
            if k in new_dict:
                new_dict[k].extend(v)
            else:
                uniqueKeysCSV2.append(k)
        
        #numOfNonKeyHeaders = len(list(dict2.values())[0])
        #v = [''] * numOfNonKeyHeaders
        uniqueKeysCSV1 = []
        #check for keys present in csv1 but not csv2 - remove keys unique to csv1
        for k in dict1.keys():
            if not k in dict2:
                uniqueKeysCSV1.append(k)
                del new_dict[k]
                #new_dict[k].extend(v)
        
        #print any unique keys to console
        if len(uniqueKeysCSV1) > 0 or len(uniqueKeysCSV2) > 0:
            print("WARNING: Following keys have been excluded as they do not appear across both CSVs!")
            print(csv1_name)
            for k in uniqueKeysCSV1:
                print(k)
            
            print(csv2_name)
            for k in uniqueKeysCSV2:
                print(k)
    
        return new_dict
    else:
        print("WARNING: Could not join the CSVs (" + csv1_name + ", " + csv2_name + ") Key headers do not match")
        return dict1

def concat(dict1, dict2, csv1_name, csv2_name):
    dup_keys=[]
    headers1 = getHeaders(dict1)
    headers2 = getHeaders(dict2)
    if headers1==headers2:
        count = 0
        new_dict=copy.deepcopy(dict1)
        #add each key and its values from csv2 to csv1 (except headers) if key not already present in csv1. If already present add key to list of duplicate keys and increment counter by 1
        for k, v in dict2.items():
            if k != list(dict2.keys())[0]:
                if k in new_dict:
                    dup_keys.append(k)
                    count+=1
                else:
                    new_dict[k] = v

        if count > 0:
            print("WARNING: " + str(count) + " duplicate keys found")
            for k in dup_keys:
                print(k)

        return new_dict
    else:
        print("WARNING: Could not concat the CSVs (" + csv1_name + ", " + csv2_name + ") Headers from each file must match")
        return dict1

def filter(dict, condition_field, condition_value, op, csv_name):
    filtered_dict=copy.deepcopy(dict)
    old_dict=copy.deepcopy(dict)

    headers = getHeaders(old_dict)
    if condition_field in headers:
        if condition_field == headers[0]:
            if op in ops:
                old_dict.pop(list(old_dict.keys())[0])
                for k in old_dict.keys():
                    #check current field against condition value for operator passed in
                    if ops[op](k, str(condition_value)):
                        continue
                    else:
                        del filtered_dict[k]
            else:
                print("WARNING: Chosen operator is not applicable! Unable to filter CSV (" + csv_name + ")")            
        else:
            index = headers.index(condition_field)-1
            old_dict.pop(list(old_dict.keys())[0])
            for k, v in old_dict.items():
                #check if condition value is a float or integer
                if isinstance(condition_value, float) or isinstance(condition_value, int):
                    if v[index] != '':
                        #cast each field value to float
                        act_value=float(v[index])
                    else:
                        act_value = 0
                else:
                    act_value=v[index]
                if op in ops:
                    if ops[op](act_value, condition_value):
                        continue
                    else:  
                        del filtered_dict[k]   
                else:
                    print("WARNING: Chosen operator is not applicable! Unable to filter CSV (" + csv_name + ")")
                    break                
        return filtered_dict
    else:
        print("WARNING: Cannot filter by " + condition_field + ". This header does not exist in the CSV (" + csv_name + ")")
        return dict

def select(dict, fields, csv_name):
    #Check all fields exist within the csv
    headers = getHeaders(dict)
    if set(fields).issubset(headers):
        new_dict={}
        indexes=[]

        for field in fields:
            indexes.append(headers.index(field)-1)

        #select fields including the key field
        for k, v in dict.items():
            accessed_mapping = map(v.__getitem__, indexes)
            accessed_list = list(accessed_mapping)
            new_dict[k] = accessed_list
        
        """
        Old code which enabled selection of fields not including key field
        else:
            #select fields not including the key field
            i=1
            for k, v in dict.items():
                accessed_mapping = map(v.__getitem__, indexes)
                if len(indexes) > 1:
                    accessed_list = list(accessed_mapping)
                else:
                    accessed_list = list(accessed_mapping)[0]
                new_dict[i] = accessed_list
                i += 1
        
            new_headers = fields
        """
        return new_dict
    else:
        print("WARNING: Not all of the following headers exist within the CSV (" + csv_name + ") \n" + str(fields))
        return dict

def order(dict, field, dir, csv_name):
    #assign direction
    if dir in ['>','<']:
        if dir == '>':
            dir = False
        else:
            dir = True

        old_dict=copy.deepcopy(dict)

        headers = getHeaders(old_dict)
        if field in headers:
            if field == headers[0]:
                sorted_dict={}
                sorted_dict[list(old_dict.keys())[0]] = list(old_dict.values())[0]
                old_dict.pop(list(old_dict.keys())[0])
                sorted_dict_as_list = sorted(old_dict.items(), key=lambda e: e[0], reverse=dir)
                for i in sorted_dict_as_list:
                    sorted_dict[i[0]] = i[1]
            else:    
                index = headers.index(field) - 1
                sorted_dict={}
                sorted_dict[list(old_dict.keys())[0]] = list(old_dict.values())[0]
                old_dict.pop(list(old_dict.keys())[0])
                sorted_dict_as_list = sorted(old_dict.items(), key=lambda e: e[1][index], reverse=dir)
                for i in sorted_dict_as_list:
                    sorted_dict[i[0]] = i[1]

            return sorted_dict
        else:
            print("WARNING: Cannot order by " + field + ". This header does not exist in the CSV (" + csv_name + ")")
            return dict
    else:
        print("WARNING: Chosen operator is not applicable! Unable to order CSV (" + csv_name + ")")
        return dict

def subtract(dict1, dict2):
    new_dict=copy.deepcopy(dict1)

    for k in list(dict2.keys())[1:]:
        if k in new_dict:
            del new_dict[k]

    return new_dict

def extract(dict1, dict2):
    new_dict={}
    new_dict[list(dict1.keys())[0]] = list(dict1.values())[0]

    for k in list(dict2.keys())[1:]:
        if k in dict1.keys():
            new_dict[k] = dict1.get(k)

    return new_dict

def rename(dict,old_header,new_header,csv_name):
    if old_header == list(dict.keys())[0]:
        old_dict=copy.deepcopy(dict)
        new_dict={}
        new_dict[new_header] = list(dict.values())[0]
        old_dict.pop(list(old_dict.keys())[0])
        new_dict.update(old_dict)
    elif old_header in list(dict.values())[0]:
        old_dict=copy.deepcopy(dict)
        index = list(old_dict.values())[0].index(old_header)
        headers = list(old_dict.values())[0]
        headers[index] = new_header
        new_dict={}
        new_dict[list(old_dict.keys())[0]] = headers
        old_dict.pop(list(old_dict.keys())[0])
        new_dict.update(old_dict)
    else:
        print("WARNING: " + old_header + " is not an existing header within the CSV (" + csv_name + ")")
        return dict

    return new_dict

def update(dict,key,field,new_value,csv_name):
    new_dict=copy.deepcopy(dict)
    if key in new_dict.keys():
        if field in list(new_dict.values())[0]:
            index = list(new_dict.keys()).index(key)

            field_index = list(new_dict.values())[0].index(field)

            values = list(new_dict.values())[index]

            values[field_index] = new_value
    
            new_dict[key] = values
        else:
            print("WARNING: " + field + " is not an existing header within the CSV (" + csv_name + ")")
    else:
        print("WARNING: " + key + " is not an existing key within the CSV (" + csv_name + ")")

    return new_dict

def insert_column(dict,column_name,default_value,csv_name):
    old_dict=copy.deepcopy(dict)
    if not column_name in list(old_dict.values())[0] and column_name != list(old_dict.keys())[0]:
        non_key_headers = list(old_dict.values())[0]
        non_key_headers.append(column_name)

        new_dict={}
        new_dict[list(old_dict.keys())[0]] = non_key_headers
        for k, v in list(old_dict.items())[1:]:
            v.append(default_value)
            new_dict[k] = v
    
        return new_dict
    else:
        print("WARNING: " + column_name + " is already a column within the CSV (" + csv_name + ")")
        return old_dict

def delete_column(dict,column_name,csv_name):
    old_dict=copy.deepcopy(dict)
    non_key_headers = list(old_dict.values())[0]
    if column_name in non_key_headers:
        indexPos = non_key_headers.index(column_name)

        new_dict={}
        for k,v in list(old_dict.items()):
            del v[indexPos]
            new_dict[k] = v

        return new_dict
    elif column_name == list(old_dict.keys())[0]:
        print("WARNING: You cannot delete the key header (" + column_name + ")!")
        return dict
    else:
        print("WARNING: The following header does not exist within the CSV (" + csv_name + "): " + column_name)
        return dict
    
def insert_row(dict,key,values,csv_name):
    new_dict=copy.deepcopy(dict)
    if len(values) == len(list(new_dict.values())[0]): 
        if not key in new_dict.keys():
            new_dict[key] = values
        else:
            print("WARNING: Key (" + key + ") already exists within the CSV (" + csv_name + ")")
    else:
        if len(values) < len(list(new_dict.values())[0]):
            print("WARNING: Number of values passed in for new row are lower than expected!")
        else:
            print("WARNING: Too many values have been passed in for new row!")
    return new_dict

def delete_row(dict, key, csv_name):
    new_dict=copy.deepcopy(dict)
    if not key == list(new_dict.keys())[0]:
        if key in new_dict.keys():
            del new_dict[key]
        else:
            print("WARNING: Key (" + key + ") does not exist within the CSV (" + csv_name + ")")
    else:
        print("WARNING: Cannot delete the row containing the headers!")

    return new_dict

def echo(list): # pragma: no cover
    #join each item from list in a single string then print to console
    text = ' '.join([str(item) for item in list])
    print(text)
