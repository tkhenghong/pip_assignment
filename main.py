# TEOH KHENG HONG
# TP030562
import decimal
import fileinput
import os
import platform
import sys

'''
3 files will be created by the system, which are:
1. User.txt (Store user's credentials and profile information)
2. Balance.txt (Store Customer's balance)
3. Transaction.txt (Store Customer's transaction)
'''


# GENERAL SNIPPETS
# Strip whitespace first and check the string is empty or not: (https://stackoverflow.com/a/9573278)
def string_is_blank(value):
    return not (value and value.strip())


# Read last line of file efficiently (Reference: https://stackoverflow.com/a/54278929)
def get_last_line_of_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
                return f.readline().decode()
            except OSError:
                f.seek(0)
                return f.readline().decode()
    else:
        return ''


# Clear console in Python to ensure clear outputs between screens.
# Reference: https://www.delftstack.com/howto/python/python-clear-console/
def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


# Get the info of a user in the User.txt data file.
# Returns a list of strings. (Reference: https://stackoverflow.com/a/39397293)
def get_user_info(username, password) -> list[str]:
    if os.path.isfile('User.txt'):
        user_file = open('User.txt')
        for line in user_file:
            line = line.rstrip().split('\t')
            if username in line and password not in line:
                print('Incorrect Username/password. Please try again.')
            elif username in line and password in line:
                # ID \t username \t password \t name \t user_type
                # Returning ID, username and user type.
                return line
        print('Incorrect Username/password. Please try again.')
        return []
    else:
        print('User not found.')
        return []


def get_username(user_type, default_username):
    while True:
        customer_username = input('Please enter the ' + user_type + '\'s username. ' + (
            '(Default ' + user_type + '\'s' + ' username: ' + default_username + ')' if default_username else ''))
        if string_is_blank(customer_username):
            if default_username:
                customer_username = default_username
                break
            else:
                print(user_type + '\'s username is empty. Please try again.')
                continue
        else:
            break
    return customer_username


def get_user_password(user_type, default_password):
    while True:
        password = input(
            'Please enter the ' + user_type + '\'s password. ' + (
                '(Default ' + user_type + '\'s' + ' password: ' + default_password + ')' if default_password else ''))
        if string_is_blank(password):
            if default_password:
                password = default_password
                break
            else:
                print(user_type + '\'s password is empty. Please try again')
                continue
        else:
            confirm_password = input('Confirm the ' + user_type + '\'s password: ')
            if string_is_blank(confirm_password):
                print('Please try again. Confirm the ' + user_type + '\'s password: ')
            else:
                if password != confirm_password:
                    print('The passwords are not the same. Please enter the details again.')
                else:
                    break
    return password


def get_user_name(user_type):
    while True:
        name = input('Please enter the ' + user_type + '\'s name: ')
        if string_is_blank(name):
            print(user_type + '\'s name is empty.')
            continue
        else:
            break
    return name


# Search user in the User.txt data file by ID
def find_user(user_id) -> list[list[str]]:
    result_users = []
    if os.path.isfile('User.txt'):
        user_file = open('User.txt')
        for line in user_file:
            line = line.rstrip().split('\t')
            print('line: ', line)
            if user_id in line:
                result_users.append(line)

    else:
        return []
    return result_users


# FUNCTIONS
# Admin
# ID \t username \t password \t name \t user_type
# Customer
# ID \t username \t password \t name \t balance \t user_type
# Save user (Admin/Customer) into User.txt file
def create_user(username, password, name, user_type):
    try:
        print('Saving user info...')

        last_user_line = get_last_line_of_file('User.txt')

        # Split the last line user info into an array of texts
        last_user_info = last_user_line.rstrip().split('\t')

        # Get the 1st information of the last_user_info array,
        # then substring the text to take the 2nd character till end.
        # Convert the result to string and addition by 1 .
        # Reference: https://stackoverflow.com/a/12572391
        existing_user_id = '0' if string_is_blank(last_user_info[0]) else last_user_info[0].split('U', 1)[1]

        new_user_id = 1 if string_is_blank(last_user_info[0]) else int(existing_user_id) + 1
        user_file = open('User.txt', 'a') if os.path.isfile('User.txt') else open('User.txt', 'w')

        user_file.write(
            'U' + str(new_user_id) + '\t' + username + '\t' + password + '\t' + name + '\t' + user_type + '\n')
        print('User saved successfully.')
        user_file.close()
    except Exception as e:
        print('Exception caught. e: ', e)


# Create admin user in the system
def create_admin_user():
    admin_default_username = 'admin'
    admin_default_password = 'password'

    print('An admin user is required for initial usage of this system.')

    admin_username = get_username('admin', admin_default_username)
    admin_password = get_user_password('admin', admin_default_password)
    admin_name = get_user_name('admin')

    # Create local data files
    create_user(admin_username, admin_password, admin_name, 'Admin')


# Register a new customer into the system
def create_customer_user():
    print('Register customer selected.')
    customer_username = get_username('customer', None)
    customer_password = get_user_password('customer', None)
    customer_name = get_user_name('customer')

    # Create local data files
    create_user(customer_username, customer_password, customer_name, 'Customer')


def create_transaction(user_id, transaction_type, amount):
    transaction_file = open('Transaction.txt', 'a') if os.path.isfile('Transaction.txt') else \
        open('Transaction.txt', 'w')

    transaction_file.write('{}\t{}\t{}\n'.format(user_id, transaction_type, amount))
    transaction_file.close()


# Update balance of a user in Balance.txt file.
# Returns True or False to indicate success.
def update_balance(user_id, transaction_type, amount):
    update_success = False
    withdrawal_eligible = True

    print('Saving...')

    balance_file = open('Balance.txt', 'a') if os.path.isfile('Balance.txt') else open('Balance.txt', 'w')

    # If File is blank, by checking file size.
    # https://stackoverflow.com/a/2507871
    empty_file = os.stat('Balance.txt').st_size == 0

    if empty_file:
        if transaction_type == 'Deposit':
            balance_file.write(user_id + '\t' + str(amount) + '\n')
            update_success = True
        else:
            withdrawal_eligible = False
    else:
        for line in fileinput.input('Balance.txt', inplace=True):
            user_balance = line.rstrip().split('\t')
            if user_id in user_balance:
                # Use Decimal for precise currency
                # Reference: https://docs.python.org/3/library/decimal.html
                balance = decimal.Decimal(user_balance[1])
                if transaction_type == 'Deposit':
                    balance += amount
                    # Replace a line in file
                    # Reference: https://stackoverflow.com/a/290494
                    print('{}\t{}'.format(user_id, balance), end='')
                    update_success = True
                    fileinput.close()
                    break
                else:
                    if balance < amount:
                        withdrawal_eligible = False
                        fileinput.close()
                        break
                    else:
                        balance -= amount
                        print('{}\t{}'.format(user_id, balance), end='')
                        update_success = True
                        fileinput.close()
                        break

    if not withdrawal_eligible:
        print('You don\'t have that amount of money to withdraw.')
    return update_success


def login():
    while True:
        username = input('Please enter your username: ')
        if string_is_blank(username):
            print('Username is empty.')
            continue
        else:
            break

    while True:
        password = input('Please enter your password: ')
        if string_is_blank(password):
            print('Password is empty.')
            continue
        else:
            break
    # Create local data files
    user_info = get_user_info(username, password)

    if user_info:
        print('Welcome, ', user_info[3], ' ', user_info[0])
        if user_info[4] == 'Admin':
            display_admin_menu(user_info)
        else:  # Customer
            display_customer_menu(user_info)
    else:
        login()  # Recurring function (Reference: https://www.programiz.com/python-programming/recursion)


def deposit(user_info):
    while True:
        try:
            amount = decimal.Decimal(input('Please enter the amount that you want to deposit: '))
            update_balance_success = update_balance(user_info[0], 'Deposit', amount)
            create_transaction(user_info[0], 'Deposit', amount)
            print('Deposit ', 'successful.' if update_balance_success else 'failed.')
            break
        except ValueError:
            print('Please enter a number.')


def withdrawal(user_info):
    while True:
        try:
            amount = decimal.Decimal(input('Please enter the amount that you want to withdraw: '))
            update_balance_success = update_balance(user_info[0], 'Withdrawal', amount)
            create_transaction(user_info[0], 'Withdrawal', amount)
            print('Withdrawal', 'successful.' if update_balance_success else 'failed.')
            break
        except ValueError:
            print('Please enter a number.')


# ID \t username \t password \t name \t user_type
def view_customer_profile(user_info):
    print('View Customer Profile selected.')
    if user_info[4] == 'Admin':
        search_keyword = input('Please enter the customer\'s ID or name')
        customer_search_result_list = find_user(search_keyword)

        if customer_search_result_list:
            while True:
                print('Here are the search result: \n')
                # Loop with index. Reference: https://stackoverflow.com/a/522578
                for index in range(len(customer_search_result_list)):
                    print(index + 1, '. ', customer_search_result_list[index][0], ' ',
                          customer_search_result_list[index][3])
                selection = int(input('Enter the number to select a customer to continue.'))

                if selection > len(customer_search_result_list) or selection < 1:
                    print('Invalid selection. Please try again.')
                    continue
                else:
                    display_customer_profile(customer_search_result_list[selection - 1])
                    input('Press ENTER to continue...')
                    break
        else:
            print('No users are found.')
            input('Press ENTER to continue...')
    else:
        display_customer_profile(user_info)


def display_customer_profile(user_info):
    print('Here are the profile details: \n',
          'Username: ', user_info[1], '\n',
          'Name: ', user_info[3], '\n',
          'User Type: ', user_info[4]), '\n',


def view_customer_transactions(user_info):
    pass


def display_about_this_system():
    pass


# Display welcome menu.
def display_welcome():
    print('Welcome to Online Banking System.')
    while True:
        try:
            selection = int(input('Here are a list that you can perform: \n' +
                                  '1. Login\n' +
                                  '2. About this system\n' +
                                  '3. Exit\n' +
                                  'Enter the number of the functions above to proceed.\n'))

            # Switch case in Python.
            # References:   https://towardsdatascience.com/switch-case-statements-are-coming-to-python-d0caf7b2bfd3
            #               https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
            if selection == 1:
                login()
            elif selection == 2:
                display_about_this_system()
            elif selection == 3:
                print('Thank you for using this system. See you next time!')
                # Exit the program.
                # Reference: https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
                sys.exit("System exited successfully.")
            else:
                print('Invalid input. Please try again.')
        except ValueError:
            print('Please enter a number.')
            continue


def display_admin_menu(user_info):
    while True:
        try:
            selection = int(input('Here are a list that you can perform: \n' +
                                  '1. Create new customer\n' +
                                  '2. View Customer\'s Profile\n' +
                                  '3. View Customer\'s Transactions\n' +
                                  '4. Logout\n' +
                                  'Enter the number of the function to proceed.\n'))

            # Switch case in Python.
            # References:   https://towardsdatascience.com/switch-case-statements-are-coming-to-python-d0caf7b2bfd3
            #               https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
            if selection == 1:
                create_customer_user()
            elif selection == 2:
                view_customer_profile(user_info)
            elif selection == 3:
                view_customer_transactions(user_info)
            elif selection == 4:
                print('Logged out.')
                break
            else:
                print('Invalid input. Please try again.')
        except ValueError:
            print('Please enter a number.')
            continue


def display_customer_menu(user_info):
    while True:
        try:
            selection = int(input('Here are a list that you can perform: \n' +
                                  '1. Make Deposit\n' +
                                  '2. Make Withdrawal\n' +
                                  '3. View Transactions\n' +
                                  '4. View Own Profile\n' +
                                  '5. Logout\n' +
                                  'Enter the number of the function to proceed.\n'))

            if selection == 1:
                deposit(user_info)
            elif selection == 2:
                withdrawal(user_info)
            elif selection == 3:
                view_customer_transactions(user_info)
            elif selection == 4:
                view_customer_profile(user_info)
            elif selection == 5:
                print('Logged out.')
                break
            else:
                print('Invalid input. Please try again.')

        except ValueError:
            print('Please enter a number.')
            continue


# Initialization of the program to check the user existence
def init():
    print('Initialize first time running...')
    # Check local data files exist
    if os.path.isfile('User.txt'):
        print('Local data exists.')
    else:
        create_admin_user()
        # transaction_file = open('Transaction.txt', 'w')
        # transaction_file.close()
    display_welcome()


def main():
    init()


if __name__ == '__main__':
    main()
