# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os


# Strip whitespace first and check the string is empty or not: (https://stackoverflow.com/a/9573278)
def string_is_blank(myString):
    return not (myString and myString.strip())


# Read last line of file efficiently (Reference: https://stackoverflow.com/a/54278929)
def get_last_line_of_file(file_name):
    with open(file_name, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        return f.readline().decode()


def save_user(username, password, user_type):
    print('Saving user info...')
    user_file = open('User.txt', 'rb')
    last_user_line = get_last_line_of_file('User.txt')

    # Split the last line user info into an array of texts
    last_user_info = last_user_line.split('\t')

    print('last_user_line: ' + last_user_line)
    print('last_user_info: ', last_user_info)

    # Get the 1st information of the last_user_info array, then substring the text to take the 2nd character till end.
    # Convert the result to string and addition by 1 .
    # Reference: https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
    new_user_id = (int(last_user_info[0][1:-1]) + 1)

    user_file.write('U' + str(new_user_id) + "\t" + username + "\t" + password + "\t" + user_type + "\n")
    print('User saved successfully.')
    user_file.close()


def create_admin_user():
    admin_username = 'admin'
    admin_default_password = 'password'
    admin_password = ''

    print('An admin user is required for initial usage of this system.')
    while True:
        admin_username = input(
            'Please enter the admin\'s username. (Default admin username: ' + admin_username + ')')
        if string_is_blank(admin_username):
            print('Username is required. Please try again.')
        else:
            break

    while True:
        admin_password = input(
            'Please enter the admin\'s password: (Default admin password: ' + admin_default_password + ')')
        if string_is_blank(admin_password):
            admin_password = admin_default_password
        else:
            admin_confirm_password = input('Confirm the admin\'s password: ')
            if string_is_blank(admin_confirm_password):
                print('Please try again. Confirm the admin\'s password: ')
            else:
                if admin_password != admin_confirm_password:
                    print('The passwords are not the same. Please enter the details again.')
                else:
                    break
    # Create local data files
    save_user(admin_username, admin_password, 'Admin')


# Initialization of the program to check the user existence
def init():
    print('Initialize first time running...')
    # Check local data files exist
    if os.path.isfile("Users.txt") and os.path.isfile("Transaction.txt"):
        create_admin_user()
        transaction_file = open('Transaction.txt', 'w')
        transaction_file.close()
    else:
        print('Local data exists.')

def register_customer():

def login():

def deposit():

def withdrawal():


# Return a list of customer names with customer ID (Dictionaries)
def search_customer(search_term):

def view_customer_transaction(customer_id):

def main():
    init()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
