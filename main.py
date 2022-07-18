from goit_project1.AddressBook import *
from goit_project1.AddressBook import main as addressbook
from Notes import *
from Notes import main as notes
from goit_project1.Sorter import *

def main():
    print('Hello, this bot has 3 functions:')
    while True:
        print('1. Addressbook\n2. Notes\n3. Sorter\nTo chose function print the number of function which you want to work with or print help to get more information')
        user_input = input("Please, enter command: ")
        if user_input.lower() == 'addressbook' or user_input == '1':
            print(f'Opening Adressbook\nPrint help to get all commands')
            addressbook()
        elif user_input.lower() == 'notes' or user_input == '2':
            print(f'Opening Notes\nPrint help to get all commands')
            notes()
        elif user_input.lower() == 'sorter' or user_input == '3':
            print(f'Opening Sorter')
            sorter()
        elif user_input.lower() == 'help':
            print('With Addressbook you can save such information as name, phone, date of bitrhday, email and address.\nWith Notes you can save notes and tags to them.\nWith Sorter you can sort all your files in folder by types.')
        elif user_input.lower() == 'exit' or user_input == '.':
            print('Good bye!')
            break
        else:
            print('Wrong command, print help to get more information or exit to turn off this bot')

if __name__ == "__main__":
    main()