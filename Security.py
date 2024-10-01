# from getpass import getpass  # Import getpass module to get password securely and anonymously
import bcrypt
from DB_Schema import db

def create_password():

    # Get the password from the user
    #password = getpass(prompt="Enter your password: ")
    password = input("Enter your password: ")

    # Generate a salt for the password hash
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password, salt

def verify_customer():

    # Get the cust_id from the user
    customer_id = input("Enter your id: ")

    # Get the password from the user
    #password = getpass(prompt="Enter your password: ")
    password = input("Enter your password: ")
    # the getpass function from the getpass module is used to securely prompt the user to enter their password.
    # This ensures that the password is not visible on the command line as it is being typed.

    with db.cursor() as cursor:

        # Retrieve the hashed password for the customer ID from the database
        cursor.execute("SELECT password, name FROM customer WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()

        name = result[1]

        # Verify the password using stored hashed password and salt
        if result is not None:
            stored_hashed_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                print(f"Welcome, {name}! (ID : {customer_id})")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Customer not found")
            return False


def verify_employee():
    # Get the emp_id from the user
    employee_id = input("Enter your id: ")

    # Get the password from the user
    password = input("Enter your password: ")

    with db.cursor() as cursor:

        cursor.execute("SELECT name FROM employees WHERE employee_id = %s", (employee_id,))
        name = cursor.fetchone()

        # Verify the password using bcrypt
        cursor.execute("SELECT password FROM employees WHERE employee_id = %s", (employee_id,))
        result = cursor.fetchone()

        if result is not None:
            stored_hashed_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                print(f"Welcome, {name}! (ID : {employee_id})")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("Customer not found.")
            return False

def head_manager_login():
    # Get the emp_id from the user
    employee_id = input("Enter your id: ")

    # Get the password from the user
    password = input("Enter your password: ")

    with db.cursor() as cursor:

        cursor.execute("SELECT password, pwd_salt, designation, name FROM employees WHERE employee_id = %s", (employee_id,))
        result = cursor.fetchone()

        stored_hashed_password = result[0]
        designation = result[2]
        name = result[3]

        if result is not None:
            # Verify the password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                if designation is None or designation != "head manager":
                    print("Only head managers are authorized to update the respective data.")
                    return None
                print(f"Welcome, {name}! (ID : {employee_id})")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("No Head Manager found.")
            return False
