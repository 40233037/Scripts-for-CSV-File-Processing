import sys
import os.path

def custom_split(line):
    prev_c = ''
    init_c = ''
    item = ''
    count = 0
    items = []
    for c in line:
        if c == line[0] and count == 0:
            item = c
        elif count == len(line)-1:
            if init_c == '"' and c == '"':
                items.append(item)
                item = ''
                prev_c = ''
            elif c == ' ':
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
        elif c == ' ':
            if init_c == '"':
                item += c
                prev_c = c
            elif item != '':
                items.append(item)
                item = ''
                prev_c = c
            elif prev_c == ' ':
                item = ''
                items.append(item)
                prev_c = c
        elif prev_c == ' ':
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

def read_script(filename):
    #check if file exists
    if os.path.isfile(filename):
        #check file is a text file
        if filename[-3:] == "txt": 
            #obtain number of lines within file to ensure it is not empty
            f = open(filename, 'r')
            row_count = 0
            for l in f:
                if l != '\n':
                    row_count += 1
            f.close()

            if row_count > 0:
                #create list of commands and their arguments
                cmds=[]
                with open(filename, 'r') as f:
                    for line in f:
                        if line != '\n':
                            line = line.strip().replace('\n','')
                            items = custom_split(line)
                            cmds.append(items)
                return cmds
            else:
                print("WARNING: " + str(filename) + " is empty therefore no commands to execute! Terminating program")
                sys.exit()
        else:
            print("WARNING: Script must be a .txt file! Terminating program")
            sys.exit()
    else:
        print("WARNING: " + str(filename) + " does not exist! Terminating program")
        sys.exit()