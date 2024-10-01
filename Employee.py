from DB_Schema import db
import Security
import datetime

def add_employee():

    # Prompt the user to enter the details
    name = input("Enter employee's name: ")
    pan_number = input("Enter employee's Pan-Card number: ")
    email = input("Enter employee's email_id: ")
    phone_number = int(input("Enter the working phone_number: "))
    designation = input("Enter employee's Designation: ")
    salary = input("Enter employee's salary: ")
    password, salt = Security.create_password()

    with db.cursor() as cursor:

        # Insert the new employee into the employee table
        cursor.execute("""INSERT INTO employees (name, designation, salary, email_id, phone_number, Pan_Number, password, pwd_salt)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (name, designation, salary, email, phone_number, pan_number, password, salt))

        # Get the ID of the new employee
        employee_id = cursor.lastrowid

        print(f"Employee {name} added successfully with ID {employee_id}")

        # Commit the changes to the database
        db.commit()

        return employee_id

def delete_employee():

    employee_id = input("Enter employee's id: ")

    with db.cursor() as cursor:

        # Get the employee details
        cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()

        if employee:
            # Check if the employee has already left
            if employee['leaving_date']:
                print("Employee has already left. No further updates allowed.")
                return

            # Update the employee table with the leaving date
            leaving_date = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                UPDATE employees
                SET leaving_date = %s
                WHERE employee_id = %s
            """, (leaving_date, employee_id))

            # Commit the changes to the database
            db.commit()

            # Commit the changes to the database
            db.commit()

        else:
            print(f"Employee with ID {employee_id} does not exist.")

def view_particular_customer():        #view_account_details()

    identifier = input("Enter customer's id or account-number: ")

    with db.cursor() as cursor:

        # Check if the identifier is an account number or customer id
        if identifier.isdigit():
            # Retrieve the customer associated with the given customer id
            cursor.execute("""
                SELECT c.name, c.email_id, c.phone_number, c.Aadhar_id, a.balance
                FROM customer c
                JOIN account a ON c.customer_id = a.customer_id
                WHERE c.customer_id = %s
            """, (identifier,))
        else:
            # Retrieve the customer associated with the given account number
            cursor.execute("""
                SELECT c.name, c.email_id, c.phone_number, c.Aadhar_id, a.balance
                FROM customer c
                JOIN account a ON c.customer_id = a.customer_id
                WHERE a.account_number = %s
            """, (identifier,))

        result = cursor.fetchone()
        if result is None:
            print("Error: Customer not found or Incorrect credentials.")
            return
        name, email, phone_number, aadhar_id, balance = result

        # Print the customer information
        print("Name:", name)
        print("Email:", email)
        print("Phone number:", phone_number)
        print("Aadhar ID:", aadhar_id)
        print("Balance:", balance)

def update_employee_salary():

    employee_id = input("Enter employee's id-number: ")

    salary = input("Update employee's salary to :")  #Show current salary first

    with db.cursor() as cursor:

        # Update the salary of the employee with the given ID
        cursor.execute("""UPDATE employees SET salary = %s WHERE employee_id = %s""", (salary, employee_id))

        # Commit the changes to the database
        db.commit()

def view_all_customers():

    with db.cursor() as cursor:

        # Retrieve all the customers from the database
        cursor.execute(""" SELECT * FROM customer """)
        result = cursor.fetchall()
        if result is None:
            print("Error: No customers found")
            return

        # Print the customer information
        for row in result:
            print("Customer ID:", row[0])
            print("Name:", row[1])
            print("Email:", row[2])
            print("Phone number:", row[5])
            print("Aadhar ID:", row[6])
            print("")

        # Commit the changes to the database
        db.commit()


'''
# Revoke and grant privileges
cursor.execute("REVOKE ALL PRIVILEGES ON *.* FROM 'employee'")
cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON bank.* TO 'employee'@'localhost'")
'''
