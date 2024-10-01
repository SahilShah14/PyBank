from DB_Schema import db
import Security

def add_customer():

    with db.cursor() as cursor:
        # Prompt the user to enter the details
        name = input("Enter your name: ")
        aadhar_id = input("Enter your aadhar_id: ")
        email_id = input("Enter your email_id: ")
        phone_number = int(input("Enter the working phone_number: "))
        password, salt = Security.create_password()

        # Insert the customer into the customer table
        cursor.execute(""" INSERT INTO customer (name, email_id, phone_number, aadhar_id, password, pwd_salt) VALUES (%s, %s, %s, %s, %s, %s)""",
                       (name, email_id, phone_number, aadhar_id, password, salt))

        # Get the ID of the new customer
        customer_id = cursor.lastrowid

        print(f"Customer {name} added successfully with ID {customer_id}")

        # Commit the changes to the database
        db.commit()

        return customer_id

def get_balance():

    with db.cursor() as cursor:
        account_number = input("Enter your account-number: ")
        # Retrieve balance your account from the database
        cursor.execute("SELECT balance FROM account WHERE account_number = %s", (account_number,))
        balance = cursor.fetchone()
        if balance:
            print(f"Account balance: {balance} Rs.")
            return balance[0]
        else:
            return None

#update customer info
#current users

'''
   def get_transactions(self, account_id):
        # Retrieve all transactions for a specific account from the database
        self.c3.execute("SELECT * FROM transactions WHERE account_id = %s", (account_id,))
        result = self.c3.fetchall()
        if result:
            transactions = []
            for row in result:
                transaction = Transaction(row[0], row[1], row[2], row[3], row[4])
                transactions.append(transaction)
            return transactions
        else:
            return None
'''

'''
# Grant access to the customer and customer_passwords tables
cursor.execute("""
    GRANT SELECT, UPDATE, DELETE ON banking_app_db.customer TO 'customer_user'@'localhost'
""")
cursor.execute("""
    GRANT SELECT ON banking_app_db.customer_passwords TO 'customer_user'@'localhost'
""")
cursor.execute("""
    GRANT SELECT, UPDATE, DELETE ON banking_app_db.customer_passwords TO 'customer_user'@'localhost'
""")

# Revoke the INSERT and UPDATE privileges from the customer_user
cursor.execute("""
    REVOKE UPDATE ON banking_app_db.customer FROM 'customer_user'@'localhost'
""")

# Revoke INSERT and UPDATE privileges on the `customer_passwords` table
cursor.execute("""
    REVOKE UPDATE ON banking_app_db.customer_passwords FROM 'customer_user'@'localhost'
""")

# Grant access to the customer_user for all customers in the customer table
cursor.execute("""
    GRANT SELECT ON banking_app_db.customer TO 'customer_user'@'%'
""")

# Commit the changes to the database
db.commit()
'''