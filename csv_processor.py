import script_handler
import csv_handler
import csv_operators
import math_operators
import sys, getopt

#checks if command is valid then ensures the correct number of args is present
def checkCmdArgs(l):
    cmd = l[0]
    
    if cmd == 'filter':
        expectedArgs = 6
    elif cmd == 'update':
        expectedArgs = 5
    elif cmd in ['order','rename','insert_column','insert_row']:
        expectedArgs = 4
    elif cmd in ['join','concat','select','min','max','subtract','extract','delete_column','delete_row']:
        expectedArgs = 3
    elif cmd in ['read','avg','stand_dev','write']:
        expectedArgs = 2
    elif cmd == 'count':
        expectedArgs = 1
    else:
        print("WARNING: The following command is not valid - " + str(cmd) + ". Please update the command script! Terminating program")
        print("Try 'py csv_processor.py -h or --Help' for more information.")
        sys.exit()

    if len(l)-1 != expectedArgs:
        print("WARNING: Number of arguments is incorrect for " + str(cmd) + " command. Expected " + str(expectedArgs) + " instead of " + str(len(l)-1) + ". Please update the command script! Terminating program")
        print("Try 'py csv_processor.py -h or --Help' for more information.")
        sys.exit()
        
#reads number of lines x
def read_n(file, x):
    with open(file, 'r') as f:
        while True:
            data = ''.join(f.readline() for _ in range(x))
                    
            if not data:
                break

            yield data

def getFileLen(file):
    with open(file, 'r') as f:
        return len(f.readlines())

#grabs command line arguments
argList = sys.argv[1:]
options = "hs:"
long_options = ["Help", "Script"]

try:
    args, values = getopt.getopt(argList, options, long_options)

    for currentArg,currentVal in args:
        if currentArg in ("-h", "--Help"):
            #prints contents of help.txt to console for user
            counter = 0
            for nlines in read_n('help.txt', 10):
                counter+=10
                print(nlines.rstrip())
                if not counter >= getFileLen('help.txt'): 
                    user_input = input("Press Enter to continue...")
                    #back to previous line
                    sys.stdout.write("\033[F")
                    #clear line
                    sys.stdout.write("\033[K")

                    if user_input == 'q':
                        sys.exit(0)



        elif currentArg in ("-s", "--Script"):
            #reads commands to perform from text file and stores within list
            cmds = script_handler.read_script(sys.argv[2])

            try: 
                #loop through each command and call appropriate function 
                for cmd in cmds:
                    if cmd[0] != 'echo':
                        checkCmdArgs(cmd)
                    match cmd[0]:
                        case 'read':
                            globals()[cmd[2]] = csv_handler.read_csv(cmd[1])
                        case 'write':
                            csv_handler.write_csv(cmd[2], globals()[cmd[1]])
                        case 'join':
                            globals()[cmd[3]] = csv_operators.join(globals()[cmd[1]], globals()[cmd[2]], cmd[1], cmd[2])
                        case 'concat':
                            globals()[cmd[3]] = csv_operators.concat(globals()[cmd[1]], globals()[cmd[2]], cmd[1], cmd[2])
                        case 'filter':
                            if cmd[5] == 'True':
                                globals()[cmd[6]] = csv_operators.filter(globals()[cmd[1]], cmd[2], float(cmd[3]), cmd[4], cmd[1])
                            elif cmd[5] == 'False':
                                globals()[cmd[6]] = csv_operators.filter(globals()[cmd[1]], cmd[2], cmd[3], cmd[4], cmd[1])
                            else:
                                print("WARNING: 5th argument must be either True or False for the filter command! Amend script and retry. Terminating program")
                                sys.exit()
                        case 'select':
                                globals()[cmd[3]] = csv_operators.select(globals()[cmd[1]], cmd[2].strip('[]').split(','), cmd[1])
                        case 'order':
                            globals()[cmd[4]] = csv_operators.order(globals()[cmd[1]], cmd[2], cmd[3], cmd[1])
                        case 'subtract':
                            globals()[cmd[3]] = csv_operators.subtract(globals()[cmd[1]], globals()[cmd[2]])
                        case 'extract':
                            globals()[cmd[3]] = csv_operators.extract(globals()[cmd[1]], globals()[cmd[2]])
                        case 'rename':
                            globals()[cmd[4]] = csv_operators.rename(globals()[cmd[1]], cmd[2], cmd[3], cmd[1])
                        case 'update':
                            globals()[cmd[5]] = csv_operators.update(globals()[cmd[1]], cmd[2], cmd[3], cmd[4], cmd[1])
                        case 'insert_column':
                            globals()[cmd[4]] = csv_operators.insert_column(globals()[cmd[1]], cmd[2], cmd[3], cmd[1])
                        case 'delete_column':
                            globals()[cmd[3]] = csv_operators.delete_column(globals()[cmd[1]], cmd[2], cmd[1])
                        case 'insert_row':
                            globals()[cmd[4]] = csv_operators.insert_row(globals()[cmd[1]], cmd[2], cmd[3].strip('[]').split(','), cmd[1])
                        case 'delete_row':
                            globals()[cmd[3]] = csv_operators.delete_row(globals()[cmd[1]], cmd[2], cmd[1])
                        case 'echo':
                            csv_operators.echo(cmd[1:])
                        case 'min':
                            globals()[cmd[3]] = math_operators.get_min(globals()[cmd[1]], cmd[2], cmd[1])
                        case 'max':
                            globals()[cmd[3]] = math_operators.get_max(globals()[cmd[1]], cmd[2], cmd[1])
                        case 'count':
                            count = math_operators.get_count(globals()[cmd[1]])
                            print("Count: " + str(count))
                        case 'avg':
                            avg = math_operators.get_avg(globals()[cmd[1]], cmd[2], cmd[1])
                            print("Average: " + str(avg))
                        case 'stand_dev':
                            stand_dev = math_operators.get_stand_dev(globals()[cmd[1]], cmd[2], cmd[1])
                            print("Standard Deviation: " + str(stand_dev))
                print('Script has been executed successfully!')
            except KeyError as err: 
                print("WARNING: Attempting to refer to a unknown CSV (" + str(err) + ")!")
            except ValueError as err:
                if cmd == 'filter':
                    print("WARNING: Attempting to filter with an invalid condition value! Ensure condition value is a number if filtering based on a numeric column vice versa for a non-numeric column!")
                else:
                    print("WARNING: Attempting mathematical operation on non-numeric column!")
            except:
                print("An error has occurred whilst running the script! Ensure command script is correct!")
                print("Try 'py csv_processor.py -h or --Help' for more information.")


except getopt.error as err:
    print(str(err))
    print("Try 'py csv_processor.py -h or --Help' for more information.")