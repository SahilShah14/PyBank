import Customer
from DB_Schema import db
import datetime
import random
import string
from decimal import Decimal

def open_account():

    with db.cursor() as cursor:

        # Add the new customer and get the customer_id
        customer_id = Customer.add_customer()

        account_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  #generate a random value
        balance = int(input("Enter initial balance of 1000 or more to open account: "))

        # Check that initial balance is greater than 1000
        if balance < 1000:
            print("Error: Initial balance must be at least 1000")
            return

        # Insert the new account into the account table
        cursor.execute("""INSERT INTO account (account_number, customer_id, balance) VALUES (%s, %s, %s)""", (account_number, customer_id, balance))

        cursor.execute(
            """INSERT INTO transaction (sender_account_number, recipient_account_number,transaction_type, transaction_amount)
            VALUES (%s, %s, %s, %s)""", (account_number, account_number, "Deposit", balance))

        print(f"Account created successfully. Your account number is {account_number}.")

        # Commit the changes to the database
        db.commit()

        return account_number

def withdraw_amount():
    account_number = input("Enter your account number: ")
    amount = float(input("Enter the amount to be withdrawn : "))

    with db.cursor() as cursor:

        try:
            # Check that the account exists
            cursor.execute("""SELECT balance FROM account WHERE account_number = %s""", (account_number,))

            result = cursor.fetchone()

            if result is None:
                print("Error: Account not found")
                return False
            balance = result[0]

            # Check that the account has sufficient balance
            if balance < amount:          #balance - 1000 < amount
                print("Error: Insufficient balance to withdraw money.")
                return False

            # Update the balance in the account table
            cursor.execute("""UPDATE account SET balance = balance - %s WHERE account_number = %s""", (amount, account_number,))

            # Insert a new transaction into the transaction table
            cursor.execute(
                "INSERT INTO transaction (sender_account_number, recipient_account_number, transaction_type, transaction_amount) VALUES (%s, %s, %s, %s)",
                (account_number, account_number, "Withdrawal", amount))

            # Commit the changes to the database
            db.commit()

            print(f"{amount} Rs. withdrawn successfully from account number {account_number}.")   #show current balance

        except Exception as e:
            db.rollback()
            print("Error occurred while withdrawing money. Transaction rolled back.")
            return False

def deposit_money():
    account_number = input("Enter your account number: ")
    amount = float(input("Enter the amount to be deposited: "))

    with db.cursor() as cursor:

        try:
            # Check that the account exists
            cursor.execute("""SELECT balance FROM account WHERE account_number = %s""", (account_number,))
            balance = cursor.fetchone()

            if balance is None:
                print("Error: Account not found")
                return False

            # Update the balance in the account table
            cursor.execute("""UPDATE account SET balance = balance + %s WHERE account_number = %s""", (amount, account_number,))

            # Insert a new transaction into the transaction table
            cursor.execute("INSERT INTO transaction (sender_account_number, recipient_account_number, transaction_type, transaction_amount) VALUES (%s, %s, %s, %s)",
                           (account_number, account_number, "Deposit", amount))

            # Commit the changes to the database
            db.commit()

            print(f"{amount} Rs. deposited successfully in account number {account_number}.")

        except Exception as e:
            db.rollback()
            return "Error occurred while depositing money. Transaction rolled back."

def transfer_money():
    sender_account_number = input("Enter your account number: ")
    recipient_account_number = input("Enter recipient's account number to transfer money to: ")
    transaction_amount = Decimal(input("Enter amount you want to transfer: "))

    with db.cursor() as cursor:

        # Check that the from_account has sufficient balance
        cursor.execute("""SELECT balance FROM account WHERE account_number = %s""", (sender_account_number,))
        result = cursor.fetchone()

        if result is None:
            print("Error: Account not found")
            return False
        balance = result[0]

        if balance < transaction_amount:
            print("Error: Insufficient balance")
            return False

        try:
            # Update the balance in the from_account
            cursor.execute("""UPDATE account SET balance = balance - %s WHERE account_number = %s""", (transaction_amount, sender_account_number))

            # Update the balance in the to account
            cursor.execute("""UPDATE account SET balance = balance + %s WHERE account_number = %s""", (transaction_amount, recipient_account_number))

            cursor.execute("INSERT INTO transaction (sender_account_number, recipient_account_number,transaction_type, transaction_amount) "
                           "VALUES (%s, %s, %s, %s)", (sender_account_number, recipient_account_number, "Debit", transaction_amount))

            cursor.execute(
                "INSERT INTO transaction (sender_account_number, recipient_account_number,transaction_type, transaction_amount) "
                "VALUES (%s, %s, %s, %s)", (recipient_account_number, sender_account_number, "Credit", transaction_amount))

            db.commit()

            print("transfer successful")

        except Exception as e:
            db.rollback()
            print("Error occurred while transferring money. Transaction rolled back.")

def close_account():

    account_number = input("Enter your account number: ")

    with db.cursor() as cursor:
        try:
            # Get the account details
            cursor.execute("SELECT * FROM account WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account:
                # Check if the account is open or closed already
                if account['closing_date']:
                    print("Account is already closed. No further updates allowed.")
                    return

                # Update the account table with the closing date
                closing_date = datetime.datetime.now().strftime('%Y-%m-%d')
                cursor.execute("""UPDATE account SET closing_date = %s WHERE account_number = %s""", (closing_date, account_number))

                # Commit the changes to the database
                db.commit()

                print("Account deleted successfully.")  # also show account details

            else:
                print(f"Account {account_number} does not exist.")

        except Exception as e:
            db.rollback()
            print("unable to delete your account.")


'''
    # Get the account details for a given account number
    def get_account_details(self, account_number):
        c = con.cursor(buffered = True)
        self.c.execute("SELECT * FROM account INNER JOIN customer ON account.customer_id = customer.customer_id WHERE account_number = %s",
            (account_number,))
        result = self.c.fetchone()

        if result is None:
            print("Account not found.")
        elif result :
            account = Account(result[0], result[1])
            return account

        c.close()
        con.close()
     
'''