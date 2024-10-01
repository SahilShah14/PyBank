import Account
import Customer
import Employee
import Security
from DB_Schema import db, cursor

def login_page():
    print('                                  LOGIN PAGE')
    print('                        ->Enter 1 to sign up as a new customer.')
    print('                        ->Enter 2 to login as a customer ')
    print('                        ->Enter 3 to login as an employee.')
    print('                        ->Enter 4 to login as a head-manager.')
    print('                        ->Enter 5 to Exit.')

    while True:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_customer_menu()

        elif choice == 2:
            if Security.verify_customer():
                while True:
                    main_menu_customer()
                    choice = int(input("Enter your choice: "))

                    if choice == 1:
                        Account.withdraw_amount()
                        print()

                    elif choice == 2:
                        Account.deposit_money()
                        print()

                    elif choice == 3:
                        Account.transfer_money()

                    elif choice == 4:
                        Customer.get_balance()

                    elif choice == 5:
                        Account.close_account()

                    elif choice == 6:
                        break

                    else:
                        print("Invalid choice. Please enter a valid option.")

            else:
                print("Invalid login. Exiting program.")
                exit()

        elif choice == 3:
            print("Please enter your employee login credentials.")

            if Security.verify_employee():
                while True:
                    main_menu_employee()
                    choice = int(input("Enter your choice: "))

                    if choice == 1:
                        Employee.view_particular_customer()

                    elif choice == 2:
                        Employee.view_all_customers()

                    elif choice == 3:
                        break

                    else:
                        print("Invalid choice. Please enter a valid option.")

            else:
                print("Invalid login. Exiting program.")
                exit()

        elif choice == 4:
            print("Please enter your head manager login credentials.")

            if Security.head_manager_login():
                while True:
                    main_menu_head_manager()
                    choice = int(input("Enter your choice: "))

                    if choice == 1:
                        Employee.add_employee()
                        print()

                    elif choice == 2:
                        Employee.view_particular_customer()
                        print()

                    elif choice == 3:
                        Employee.view_all_customers()

                    elif choice == 4:
                        Employee.update_employee_salary()

                    elif choice == 5:
                        Employee.delete_employee()

                    elif choice == 6:
                        break

                    else:
                        print("Invalid choice. Please enter a valid option.")

            else:
                print("Invalid login. Exiting program.")
                exit()

        elif choice == 5:
            cursor.close()
            db.close()
            exit()

        else:
            print("Invalid choice. Please choose again.")

def new_customer_menu():
    print('                                  NEW CUSTOMER SIGN UP MENU')
    print('                        ->Enter 1 to Create a new account. ')

    choice = int(input("Enter your choice: "))
    if choice == 1:
        Account.open_account()

def main_menu_customer():
    print('                                  CUSTOMER MENU')
    print('                        ->Enter 1 to Withdraw money.')
    print('                        ->Enter 2 to Deposit money.')
    print('                        ->Enter 3 to Transfer money.')
    print('                        ->Enter 4 to get your balance details.')
    print('                        ->Enter 5 to Close your account.')
    print('                        ->Enter 6 to Exit.')


def main_menu_employee():
    print('                                  EMPLOYEE MENU')
    print('                        ->Enter 1 to view particular customer details.')
    print('                        ->Enter 2 to view customer database')
#    print('                        ->Enter 4 to freeze customer account.')        # freeze customer account if suspicious activity is found
    print('                        ->Enter 3 to Exit.')

def main_menu_head_manager():
    print('                                  Head Manager MENU')
    print('                        ->Enter 1 to add employee details.')
    print('                        ->Enter 2 to view a particular customer details.')
    print('                        ->Enter 3 to view entire customer database')
#    print('                        ->Enter 4 to freeze customer account.')        # freeze customer account if suspicious activity is found
    print('                        ->Enter 4 to update an employee salary.')
    print('                        ->Enter 5 to add employee leaving details.')
    print('                        ->Enter 6 to Exit.')

# If a customer closes his account - he has to signup again
