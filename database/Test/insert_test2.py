from __future__ import print_function
from datetime import date, datetime, timedelta
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Swsh123$',
                             db='employees',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        tomorrow = datetime.now().date() + timedelta(days=1)

        add_employee = ("INSERT INTO employees "
                       "(first_name, last_name, hire_date, gender, birth_date) "
                       "VALUES (%s, %s, %s, %s, %s)")
        add_salary = ("INSERT INTO salaries "
                      "(emp_no, salary, from_date, to_date) "
                      "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

        data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))   

        # Insert new employee
        cursor.execute(add_employee, data_employee)
        emp_no = cursor.lastrowid

        # Insert salary information
        data_salary = {
          'emp_no': emp_no,
          'salary': 50000,
          'from_date': tomorrow,
          'to_date': date(9999, 1, 1),
        }
        cursor.execute(add_salary, data_salary)

        # Make sure data is committed to the database
        connection.commit()

        cursor.close()
        #connection.close() 

    
finally:
    connection.close()