# TEOH KHENG HONG
# TP030562

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
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            return f.readline().decode()
    else:
        return ''


# Clear console in Python to ensure clear outputs between screens.
# Reference: https://www.delftstack.com/howto/python/python-clear-console/
def clear_console():
    match platform.system():
        case 'Windows':
            os.system('cls')
        case _:
            os.system('clear')


# Get the info of a user in the User.txt data file.
# Returns a list of strings. (Reference: https://stackoverflow.com/a/39397293)
def get_user_info(username, password) -> list[str]:
    if os.path.isfile('User.txt'):
        user_file = open('User.txt')
        for line in user_file:
            line = line.rstrip()
            if username in line and password not in line:
                print('Incorrect Username/password. Please try again.')
            elif username in line and password in line:
                # ID \t username \t password \t name \t user_type
                # Returning ID, username and user type.
                return [line[0], line[3], line[4]]
            else:
                print('User not found. Please try again.')
        print('No user info found.')
        return []
    else:
        print('No user info found.')
        return []


def get_username(user_type, default_username):
    while True:
        customer_username = input('Please enter the' + user_type + '\'s username. ' + (
            '(Default ' + user_type + '\'s' + ' username: ' + default_username + ')' if default_username else ''))
        if string_is_blank(customer_username):
            print('Username is empty.')
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
            if not default_password:
                print(user_type + '\'s password is empty. Please try again')
                continue
            else:
                password = default_password
                break
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
def find_user_by_id(user_id) -> list[str]:
    if os.path.isfile('User.txt'):
        user_file = open('User.txt')
        for line in user_file:
            line = line.rstrip()
            if user_id in line:
                print('User found.')
                return [line[0], line[3], line[4]]
        print('No user info found.')
        return []
    else:
        print('No user info found.')
        return []


# Search user in the User.txt data file by name
def find_user_by_name(user_name):
    search_result_users = []
    if os.path.isfile('User.txt'):
        user_file = open('User.txt')
        for line in user_file:
            line = line.rstrip()
            if user_name in line:
                print('User found.')
                search_result_users.append([line[0], line[3], line[4]])
            else:
                continue

        return search_result_users
    else:
        print('No users are found.')
        return []


# FUNCTIONS
# Admin
# ID \t username \t password \t name \t user_type
# Customer
# ID \t username \t password \t name \t balance \t user_type
# Save user (Admin/Customer) into User.txt file
def save_user(username, password, name, user_type):
    print('Saving user info...')

    last_user_line = get_last_line_of_file('User.txt')

    # Split the last line user info into an array of texts
    last_user_info = last_user_line.split('\t')

    print('last_user_line: ' + last_user_line)
    print('last_user_info: ', last_user_info)

    # Get the 1st information of the last_user_info array, then substring the text to take the 2nd character till end.
    # Convert the result to string and addition by 1 .
    # Reference: https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
    existing_user_id = last_user_info[0][1:-1] if string_is_blank(last_user_info[0]) else '0'
    new_user_id = 1 if string_is_blank(last_user_info[0]) else int(existing_user_id) + 1

    user_file = open('User.txt', 'a') if os.path.isfile('User.txt') else open('User.txt', 'w')

    user_file.write('U' + str(new_user_id) + '\t' + username + '\t' + password + '\t' + name + '\t' + user_type + '\n')
    print('User saved successfully.')
    user_file.close()


# Create admin user in the system
def create_admin_user():
    admin_default_username = 'admin'
    admin_default_password = 'password'

    print('An admin user is required for initial usage of this system.')

    admin_username = get_username('admin', admin_default_username)
    admin_password = get_user_password('admin', admin_default_password)
    admin_name = get_user_name('admin')

    # Create local data files
    save_user(admin_username, admin_password, admin_name, 'Admin')


# Register a new customer into the system
def create_customer_user():
    print('Register customer selected.')
    customer_username = get_username('customer', None)
    customer_password = get_user_password('customer', None)
    customer_name = get_user_name('customer')

    # Create local data files
    save_user(customer_username, customer_password, customer_name, 'Customer')


def update_balance(user_info, transaction_type, amount):
    # Update balance in Balance.txt file, allowing better organized data.
    pass


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

    if not user_info:
        print('Welcome, ', user_info[0])
    else:
        login()  # Recurring function (Reference: https://www.programiz.com/python-programming/recursion)


# ID \t username \t password \t name \t user_type
def view_customer_profile(user_info):
    print('View Customer Profile selected.')
    if user_info[user_info[4]] == 'Admin':
        search_keyword = input('Please enter the customer\'s ID or name')
        customer_user_info = find_user_by_id(search_keyword)

        if not customer_user_info:
            customer_search_result_list = find_user_by_name(search_keyword)

            while True:
                print('Here\' are the search result: \n')
                # Loop with index. Reference: https://stackoverflow.com/a/522578
                for customer, index in customer_search_result_list:
                    print(index, '. ', customer)
                selection = int(input('Enter the number to select a customer to continue.'))

                if selection > len(customer_search_result_list) or selection < 1:
                    print('Invalid selection. Please try again.')
                    continue
                else:
                    display_customer_profile(customer_search_result_list[selection])
                    input('Press any key to continue...')
                    break
        else:
            print('Not able to find the user. Please try again.')
    else:
        display_customer_profile(user_info)


def display_customer_profile(user_info):
    print('Here are the profile details: \n',
          'Username: ', user_info[1],
          'Name: ', user_info[3],
          'Balance: ', user_info[5])


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
                                  '2. About this system' +
                                  '3. Exit\n' +
                                  'Enter the number of the functions above to proceed.'))

            # Switch case in Python.
            # References:   https://towardsdatascience.com/switch-case-statements-are-coming-to-python-d0caf7b2bfd3
            #               https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
            match selection:
                case 1:
                    login()
                case 2:
                    display_about_this_system()
                case 3:
                    print('Thank you for using this system. See you next time!')
                    # Exit the program.
                    # Reference: https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
                    sys.exit("System exited successfully.")
                case _:
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
                                  'Enter the number of the function to proceed.'))

            # Switch case in Python.
            # References:   https://towardsdatascience.com/switch-case-statements-are-coming-to-python-d0caf7b2bfd3
            #               https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
            match selection:
                case 1:
                    create_customer_user()
                case 2:
                    view_customer_profile(user_info)
                case 3:
                    view_customer_transactions(user_info)
                case 4:
                    print('Logged out.')
                    break
                case _:
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
                                  'Enter the number of the function to proceed.'))

            match selection:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    view_customer_profile(user_info)
                case 4:
                    view_customer_transactions(user_info)
                case 5:
                    print('Logged out.')
                case _:
                    print('Invalid input. Please try again.')
                    pass
        except ValueError:
            print('Please enter a number.')
            continue


# Initialization of the program to check the user existence
def init():
    print('Initialize first time running...')
    # Check local data files exist
    if os.path.isfile('User.txt') and os.path.isfile('Transaction.txt'):
        print('Local data exists.')
        display_welcome()
    else:
        create_admin_user()
        transaction_file = open('Transaction.txt', 'w')
        transaction_file.close()


def deposit(user_info):
    pass


def withdrawal(user_info):
    pass


# # Return a list of customer names with customer ID (Dictionaries)
# def search_customer(search_term):
#
# def view_customer_transaction(customer_id):

def main():
    init()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
