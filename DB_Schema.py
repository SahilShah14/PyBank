import mysql.connector

config = {
  'user': 'root',
  'password': '1234',
  'host': 'localhost',
  'port': int(3306),
  'database': 'banking_app_db',
  'raise_on_warnings': True,
}

try:
    db = mysql.connector.connect(**config)
    print("Connected successfully to database.")

    # Check if the connection was successful
    if not db.is_connected():
        print("Error connecting with MySQL")

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Check if the database exists
    cursor.execute("SHOW DATABASES LIKE 'banking_app_db'")
    result = cursor.fetchone()
    if not result:
        # Create the database
        cursor.execute("CREATE DATABASE banking_app_db")

    # Select the database
    cursor.execute("USE banking_app_db")

    # Check if the table "customer" already exists or not
    cursor.execute("SHOW TABLES LIKE 'customer'")
    result = cursor.fetchone()
    if not result:
        # Create the customer table
        cursor.execute("""
            CREATE TABLE customer (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(25) NOT NULL,
                email_id VARCHAR(50),
                password VARCHAR(100) NOT NULL unique,
                pwd_salt varchar(100) not null,
                phone_number BIGINT NOT NULL CHECK (phone_number REGEXP '^[0-9]{10}$'),
                aadhar_id VARCHAR(12) NOT NULL UNIQUE CHECK (LENGTH(aadhar_id) = 12)
            )
        """)

    # Create Account Table
    cursor.execute("SHOW TABLES LIKE 'Account'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("""CREATE TABLE IF NOT EXISTS account (
                    account_number VARCHAR(10) Primary key check (length(account_number) = 10),
                    balance DECIMAL(15, 2) NOT NULL CHECK (balance >= 1000),  
                    customer_id INT NOT NULL,
                    opening_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    closing_date TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
                )""")

    # Create Transaction Table
    cursor.execute("SHOW TABLES LIKE 'Transaction'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("""Create Table if not exists transaction (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    sender_account_number VARCHAR(10) NOT NULL,
                    recipient_account_number VARCHAR(10) NOT NULL,
                    transaction_amount DECIMAL(10,2) NOT NULL,
                    transaction_type ENUM ('debit', 'credit', 'withdrawal', 'deposit') not null,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (sender_account_number) REFERENCES account (account_number),
                    FOREIGN KEY (recipient_account_number) REFERENCES account (account_number)
                )""")

    # Create Employees Table
    cursor.execute("SHOW TABLES LIKE 'Employees'")
    result = cursor.fetchone()
    if not result:
        cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                    employee_id INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(25) NOT NULL,
                    password VARCHAR(100) NOT NULL unique,
                    pwd_salt varchar(100) not null, 
                    pan_number varchar(10) NOT NULL UNIQUE CHECK (LENGTH(pan_number) = 10),
                    email_id VARCHAR(50),
                    phone_number BIGINT NOT NULL CHECK (phone_number REGEXP '^[0-9]{10}$'),
                    joining_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    leaving_date TIMESTAMP,
                    designation varchar(25) not null,
                    salary Decimal(10,2) not null
                )""")

    # Commit the changes and close the cursor and connection
    db.commit()

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
