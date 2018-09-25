import csv
import os

def WriteDictToCSV(csv_file,csv_columns,dict_data,csv_function='a'):
    global flag
    try:
        with open(csv_file, csv_function) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if csvfile.tell() == 0:
                writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return

"""
csv_columns = ['Row','Name','Country']
dict_data = [
    {'Row': 1, 'Name': 'zzzz', 'Country': 'India'},
    {'Row': 2, 'Name': 'Ben', 'Country': 'USA'},
    {'Row': 3, 'Name': 'Shri Ram', 'Country': 'India'},
    {'Row': 4, 'Name': 'Smith', 'Country': 'USA'},
    {'Row': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
    ]

#currentPath = os.getcwd()
csv_file = "Names.csv"

WriteDictToCSV(csv_file,csv_columns,dict_data)
""" 
