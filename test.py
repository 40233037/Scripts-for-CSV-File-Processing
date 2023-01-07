import unittest
import os
import csv_handler
import csv_operators
import math_operators
import script_handler

"""
How to run the unit tests from the commandline:  
    py -m unittest test -b (-b hides console output)
"""
class TestOperators(unittest.TestCase):
    def test_read_csv(self):
        file = 'test/testread.csv'
        act_csv = csv_handler.read_csv(file)
        expected_csv = {
            'student_number': ['firstname' , 'lastname', 'mark'],
            '1': ['FirstName1', 'LastName1', '80'],
            '2': ['FirstName2', 'LastName2', '70'],
            '3': ['FirstName3', 'LastName3', '60']
        }
        self.assertDictEqual(act_csv, expected_csv) 
    
    def test_read_csv_double_quotes(self):
        file = 'test/testreaddoublequotes.csv'
        act_csv = csv_handler.read_csv(file)
        expected_csv = {
            'student_number': ['firstname' , 'lastname', 'mark'],
            '1': ['"FirstName1", jamie', 'LastName1', '80'],
            '2': ['FirstName2', 'LastName2', '70'],
            '3': ['FirstName3', 'LastName3', '60']
        }
        self.assertDictEqual(act_csv, expected_csv) 

    def test_write_csv(self):
        csv = {
            'student_number': ['firstname' , 'lastname', 'mark'],
            '1': ['FirstName1', 'LastName1', '80'],
            '2': ['FirstName2', 'LastName2', '70'],
            '3': ['FirstName3', 'LastName3', '60']
        }
        csv_handler.write_csv('test/test_write.csv', csv)
        with open('test/test_write.csv', 'r') as f1:
            act_contents = f1.read()
        with open('test/testwrite.csv','r') as f2:
            expected_contents = f2.read()

        os.remove('test/test_write.csv')

        self.assertEqual(act_contents, expected_contents)

    def test_join_matching_key(self):
        csv1 = {
            'student_number': ['firstname', 'lastname'],
            '1': ['FirstName1', 'LastName1'],
            '2': ['FirstName2', 'LastName2'],
            '3': ['FirstName3', 'LastName3']
        }

        csv2 = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        act_csv = csv_operators.join(csv1, csv2, 'csv1', 'csv2')
 
        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['FirstName1', 'LastName1', 'CSC1234', '40'],
            '2': ['FirstName2', 'LastName2', 'CSC1234', '30'],
            '3': ['FirstName3', 'LastName3', 'CSC1234', '50']
            }

        self.assertDictEqual(act_csv, expected_csv)

    def test_join_no_matching_key(self):
        csv1 = {
            'student_number': ['firstname', 'lastname'],
            '1': ['FirstName1', 'LastName1'],
            '2': ['FirstName2', 'LastName2'],
            '3': ['FirstName3', 'LastName3']
        }

        csv2 = {
            'prac': ['mark'],
            'CSC3001': [40],
            'CSC3002': [30],
            'CSC3003': [50]
        }

        act_csv = csv_operators.join(csv1, csv2, 'csv1', 'csv2')
 
        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['FirstName1', 'LastName1'],
            '2': ['FirstName2', 'LastName2'],
            '3': ['FirstName3', 'LastName3']
            }

        self.assertDictEqual(act_csv, expected_csv)

    def test_concat_no_dups(self):
        csv1 = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        csv2 = {
            'student_number': ['prac', 'mark'],
            '4': ['CSC1234', '80'],
            '5': ['CSC1234', '70'],
            '6': ['CSC1234', '60']
        }

        act_csv = csv_operators.concat(csv1, csv2, 'csv1', 'csv2')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '80'],
            '5': ['CSC1234', '70'],
            '6': ['CSC1234', '60']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_concat_dups(self):
        csv1 = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        csv2 = {
            'student_number': ['prac', 'mark'],
            '3': ['CSC1234', '80'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        act_csv = csv_operators.concat(csv1, csv2, 'csv1', 'csv2')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_concat_headers_not_matching(self):
        csv1 = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        csv2 = {
            'student_number': ['firstname', 'lastname'],
            '4': ['FirstName1', 'LastName1'],
            '5': ['FirstName2', 'LastName2'],
            '6': ['FirstName3', 'LastName3']
        }

        act_csv = csv_operators.concat(csv1, csv2,'csv1','csv2')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_lt(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'<','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_gt(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'>','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_le(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'<=','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_ge(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'>=','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '60']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_eq(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '50']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'==','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '3': ['CSC1234', '50'],
            '5': ['CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_num_field_ne(self):
        csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '3': ['CSC1234', '50'],
            '4': ['CSC1234', '70'],
            '5': ['CSC1234', '50']
        }

        act_csv = csv_operators.filter(csv,'mark',50.0,'!=','csv')

        expected_csv = {
            'student_number': ['prac', 'mark'],
            '1': ['CSC1234', '40'],
            '2': ['CSC1234', '30'],
            '4': ['CSC1234', '70']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_lt(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','<','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '2': ['Adam', 'Ford'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_gt(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','>','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '3': ['Zach', 'Meade']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_le(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','<=','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '2': ['Adam', 'Ford'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_ge(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','>=','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_eq(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','==','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '4': ['Gary', 'Lawlor']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_string_field_ne(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','!=','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_invalid_op_key_field(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'student_number','1','?','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_invalid_op_non_key_field(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'firstname','Gary','&','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_filter_invalid_field(self):
        csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        act_csv = csv_operators.filter(csv,'mark',40.0,'<','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname'],
            '1': ['Joe', 'Bloggs'],
            '2': ['Adam', 'Ford'],
            '3': ['Zach', 'Meade'],
            '4': ['Gary', 'Lawlor'],
            '5': ['Frank', 'Lampard']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_select(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.select(csv, ['lastname', 'mark'],'csv')

        expected_csv = {
            'student_number': ['lastname', 'mark'],
            '1': ['Bloggs', '40'],
            '2': ['Ford', '60'],
            '3': ['Meade', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_select_invalid_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.select(csv, ['last', 'mark'],'csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv) 

    def test_order_num_field(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.order(csv,'mark','<','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40']
        }

        self.assertDictEqual(act_csv, expected_csv) 

    def test_order_string_field(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.order(csv,'firstname', '>','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_order_invalid_field(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.order(csv,'first','>','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_min(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = math_operators.get_min(csv,'mark','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_max(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = math_operators.get_max(csv,'mark','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '2': ['Adam', 'Ford', 'CSC1234', '60']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_count(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        count = math_operators.get_count(csv)

        self.assertEqual(count, 3)

    def test_avg(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        avg = math_operators.get_avg(csv,'mark','csv')

        self.assertEqual(avg, 50.00)

    def test_stand_dev(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        stand_dev = math_operators.get_stand_dev(csv,'mark','csv')

        self.assertEqual(stand_dev, 8.16)

    def test_read_command_script(self):
        file = 'test/testreadscript.txt'
        cmds = script_handler.read_script(file)
        print(cmds)

        expected_cmds = [['read'], ['write'], ['join'], ['concat'], ['select'], ['filter'], ['order'], ['min'], ['max'], ['avg'], ['stand_dev'], ['count']]

        self.assertEqual(cmds, expected_cmds)

    def test_subtract(self):
        csv1 = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50'],
            '4': ['Joe', 'Lavelle', 'CSC1234', '90'],
            '5': ['Finn', 'Russell', 'CSC1234', '70'],
            '6': ['Zach', 'Lamont', 'CSC1234', '80']
        }

        csv2 = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.subtract(csv1, csv2)

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '4': ['Joe', 'Lavelle', 'CSC1234', '90'],
            '5': ['Finn', 'Russell', 'CSC1234', '70'],
            '6': ['Zach', 'Lamont', 'CSC1234', '80']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_extract(self):
        csv1 = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50'],
            '4': ['Joe', 'Lavelle', 'CSC1234', '90'],
            '5': ['Finn', 'Russell', 'CSC1234', '70'],
            '6': ['Zach', 'Lamont', 'CSC1234', '80']
        }

        csv2 = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.extract(csv1, csv2)

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)
    
    def test_rename_key_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.rename(csv,'student_number','id','csv')

        expected_csv = {
            'id': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_rename_non_key_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.rename(csv,'firstname','first','csv')

        expected_csv = {
            'student_number': ['first', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)
    
    def test_rename_invalid_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.rename(csv,'header','new_header','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_update(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.update(csv,'2','lastname','Audi','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Audi', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_update_invalid_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.update(csv,'2','last','Audi','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)
    
    def test_update_invalid_key(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.update(csv,'4','lastname','Audi','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)
    
    def test_insert_column(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.insert_column(csv,'new_column','123','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark', 'new_column'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40', '123'],
            '2': ['Adam', 'Ford', 'CSC1234', '60', '123'],
            '3': ['Zach', 'Meade', 'CSC1234', '50', '123']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_insert_existing_column(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.insert_column(csv,'mark','123','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_delete_column(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark', 'new_column'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40', '123'],
            '2': ['Adam', 'Ford', 'CSC1234', '60', '123'],
            '3': ['Zach', 'Meade', 'CSC1234', '50', '123']
        }

        act_csv = csv_operators.delete_column(csv,'new_column','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_delete_column_key_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.delete_column(csv,'student_number','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_delete_column_invalid_header(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.delete_column(csv,'header','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_insert_row(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.insert_row(csv,'4',['Jamie','Lamont','CSC1234','70'],'csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50'],
            '4': ['Jamie', 'Lamont', 'CSC1234', '70']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_insert_row_existing_key(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.insert_row(csv,'2',['Jamie','Lamont','CSC1234','70'],'csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_delete_row(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.delete_row(csv,'2','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_delete_row_invalid_key(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_csv = csv_operators.delete_row(csv,'4','csv')

        expected_csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        self.assertDictEqual(act_csv, expected_csv)

    def test_getHeaders(self):
        csv = {
            'student_number': ['firstname', 'lastname', 'prac', 'mark'],
            '1': ['Joe', 'Bloggs', 'CSC1234', '40'],
            '2': ['Adam', 'Ford', 'CSC1234', '60'],
            '3': ['Zach', 'Meade', 'CSC1234', '50']
        }

        act_headers = csv_operators.getHeaders(csv)
        expected_headers = ['student_number','firstname','lastname','prac','mark']

        self.assertEqual(act_headers, expected_headers)