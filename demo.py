import csv_handler
import csv_operators
import script_handler
#import time
  
cmds = script_handler.read_script('empty_script.txt')
print(cmds)


#t0 = timer()
#csv3 = csv_operators.filter(csv,'mark',50,'>','csv')
#t1 = timer() - t0
#print(t1)






#csv = script_handler.read_script('script1.txt')
#csv2 = csv_handler.read_csv('jimbo.csv')
#csv3 = csv_operators.join(csv,csv2,'csv','csv2')
#print(csv3)




"""
ordered_dict1 = csv_operators.order(csv1, headers1, 'first', True)
ordered_dict2 = csv_operators.order(csv1, headers1, 'first', False)
ordered_dict3 = csv_operators.order(csv2, headers2, 'mark', True)
ordered_dict4 = csv_operators.order(csv2, headers2, 'mark', False)

print(ordered_dict1)
print(ordered_dict2)
print(ordered_dict3)
print(ordered_dict4)

#Demo - Standard Deviation function - displays to 2dp

stand_dev = math_operators.get_stand_dev(csv2, headers2, 'mark')
print(stand_dev)

"""
"""

csv3, headers3 = csv_operators.join(csv1, csv2, headers1, headers2)
csv_handler.write_csv('Demo1.csv', csv3, headers3, True)

#Demo 2 - Concat
 
csv4, headers4 = csv_handler.read_csv('test_data3.csv')

csv5, headers5 = csv_operators.concat(csv2, csv4, headers2, headers4)

csv_handler.write_csv('Demo2.csv', csv5, headers5, True)


#Demo 3 - Concat - Duplicate Keys

csv6, headers6 = csv_handler.read_csv('test_data4.csv')

csv7, headers7 = csv_operators.concat(csv4, csv6, headers4, headers6)

csv_handler.write_csv('Demo3.csv', csv7, headers7, True)

#Demo 4 - Filter

#csv3_filtered = csv_operators.filter(csv3, headers3, 'mark', 40, '<')
#csv3_filtered = csv_operators.filter(csv3, headers3, 'mark', 70, '>')
#csv3_filtered = csv_operators.filter(csv3, headers3, 'mark', 40, '<=')
#csv3_filtered = csv_operators.filter(csv3, headers3, 'mark', 70, '>=')

#csv3_filtered = csv_operators.filter(csv3, headers3, 'last', 'Lamont', '==')
#csv3_filtered = csv_operators.filter(csv3, headers3, 'last', 'Lamont', '!=')

#csv3_filtered = csv_operators.filter(csv3, headers3, 'size',  87, '==')
csv3_filtered = csv_operators.filter(csv3, headers3, 'id', '1', '>')
#csv3_filtered = csv_operators.filter(csv3, headers3, 'mark', 70, '||')

print(csv3_filtered)

#Demo 5 - Select


csv8, headers8 = csv_operators.select(csv3, headers3, ['first', 'last'], True)
csv_handler.write_csv('Demo5_With_Key.csv', csv8, headers8, True)

csv9, headers9 = csv_operators.select(csv3, headers3, ['first', 'last'], False)
csv_handler.write_csv('Demo5_Without_Key.csv', csv9, headers9, False)

#Demo 6 - Math operators

csv10, headers10 = math_operators.get_min(csv3, headers3, ['mark'])
csv_handler.write_csv('Demo6_Min.csv', csv10, headers10, True)

csv11, headers11 = math_operators.get_max(csv3, headers3, ['mark'])
csv_handler.write_csv('Demo6_Max.csv', csv11, headers11, True)

count = math_operators.get_count(csv5)
print('Count: ' + str(count))

avg = math_operators.get_avg(csv3, headers3, ['mark'])
print('Average: ' + str(avg))

"""