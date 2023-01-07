import sys
import os.path

#custom split method to create list of items from csv row
def custom_split(line):
    prev_c = ''
    init_c = ''
    item = ''
    count = 0
    items = []
    for c in line:
        if c == line[0] and count == 0:
            if c == '"':
                init_c = c
            elif c == ',':
                items.append(item)
                prev_c = c
                print("WARNING: A row's key field is empty!")
            else:
                item = c
                if len(line) == 1:
                    items.append(item)
        elif count == len(line)-1:
            if init_c == '"' and c == '"':
                items.append(item)
                item = ''
                prev_c = ''
            elif c == ',':
                items.append(item)
                item = ''
                prev_c = c
                items.append(item)
            else:
                item += c
                items.append(item)
                item = ''
                prev_c = ''
        elif init_c == '"' and c == '"' and prev_c != '\\':
            items.append(item)
            item = ''
            init_c = ''
            prev_c = ''
        elif c == '"':
            if prev_c == '\\':
                item += c
                prev_c = c
            else:
                init_c = c
                prev_c = c
        elif c == ',':
            if init_c == '"':
                item += c
                prev_c = c
            elif item != '':
                items.append(item)
                item = ''
                prev_c = c
            elif prev_c == ',':
                item = ''
                items.append(item)
                prev_c = c
        elif prev_c == ',':
            if c != '\\':
                item += c
                prev_c = c
            else:
                prev_c = c
        else:
            if c != '\\':
                item += c
                prev_c = c
            else:
                prev_c = c
        
        count += 1

    return items

def adjustItem(item):
    count = 0
    adjusted_item = item
    for c in item:
        if c == '"':
            if count == 0:
                adjusted_item = '\\' + adjusted_item
            else:
                adjusted_item = adjusted_item[:count+1] + '\\' + adjusted_item[count+1:]
        count += 1

    if ',' in adjusted_item:
        adjusted_item = '"' + adjusted_item + '"'
    
    return adjusted_item

def read_csv(filename):
    if os.path.isfile(filename):
        if filename[-3:] == "csv":
            f = open(filename, 'r')
            row_count = 0
            for l in f:
                if l != '\n':
                    row_count += 1
            f.close()
        
            if row_count > 1:
                #Creates empty dicitonary
                dict={}
                with open (filename, 'r') as f:
                    #Creates new dictionary item for each line in csv
                    for line in f.readlines():
                        line = line.strip().replace('\n','')
                        items = custom_split(line)
                        key = items[0]
                        del items[0]
                        dict[key] = items            
                return dict
            else:
                print("WARNING: " + str(filename) + " is empty! Terminating program")
                sys.exit()
        else:
            print("WARNING: Can only read .csv files! Terminating program")
            sys.exit()
    else:
        print("WARNING: " + str(filename) + " does not exist! Terminating program")
        sys.exit()

def write_csv(filename, dict):
    #check if writing to csv file
    if filename[-3:] == "csv":
        with open(filename, 'w') as f:
            for k,v in dict.items():
                f.write(k)
                for item in v:
                    item = adjustItem(item)
                    f.write(',' + item)
                if k != list(dict)[-1]:
                    f.write('\n')
    else:
        print("WARNING: Cannot write to file. File extension must be .csv! Terminating program")

    """
    Provides ability to write a csv without the key field - No longer required (2 additional parameters; headers and with_key)

    with open (filename, 'w') as f:
        f.write(headers[0])
        for header in headers[1:]:
            f.write(',' + header)
        
        f.write('\n')

        
        if with_key == True:
            for k, v in dict.items():
                f.write(k)
                for item in v:
                    f.write(',' + item)
                if k != list(dict)[-1]:
                    f.write('\n')
        else:
            for k, v in dict.items():
                for item in v:
                    if v.index(item) == 0:
                        f.write(item)
                    else:
                        f.write(',' + item)
                if k != list(dict)[-1]:
                    f.write('\n')
        """