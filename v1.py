"""
Filename: v1.py
Author: Varun Goel
Date: 29 / 06 / 22
Description: This program will allow the user to:
    interact with a google spreadsheet and add books to a database
Version: 1.0

IMPORTANT: you NEED to connected to the internet
           for the database to be connected
"""

import gspread
import time
# other file
from valid_input import list_valid_input, int_valid_input


def next_available_row(worksheet):
    """This function gets then next line in a worksheet"""
    # gets the first coloumn of the worksheet
    worksheet_coloumn = list(worksheet.col_values(1))

    # gets the length of items in the coulumn and returns it
    return len(worksheet_coloumn) + 1


class library_manager():

    def __init__(self):
        """This function initialises all the variables to be used in the program"""
        # connects to the service account
        self.service_account = gspread.service_account(filename='config.json')
        self.library_spreadsheet = self.service_account.open('library database')

        # these are for the 2 different worksheets (available, loaned)
        self.available_books = self.library_spreadsheet.worksheet('available')
        self.loaned_books = self.library_spreadsheet.worksheet('loaned')

    def add_book(self):
        """This function allows the user to add books to the database"""
        # this dict allows that program to turn the 'f' and 'nf' to 
        # 'fiction' and 'non fiction' to be writen to in the worksheet
        KEY_TO_NAME = {'f': 'fiction', 'nf': 'non fiction'}
        # this gets the keys (first part of dict items) and makes a list from them
        # in this case the list would be ['f', 'nf']
        FICTION_OPTIONS = ['f', 'nf', 'fiction', 'non fiction']

        new_book = []

        amount_of_books = int_valid_input('How many books are you adding (1 - 100): ', 
                                          'Please enter a positive integer below (1 - 100)!\n',
                                          1, 100)
        print() # blank line

        for _ in range(amount_of_books):
            #populates list
            new_book.append(input('What is the name of the book: ').lower())

            is_fiction = list_valid_input('Is the book fiction or non / fiction (F / NF): ', 
                                        'Please enter F or NF (fiction or non fiction)!\n', 
                                        FICTION_OPTIONS)
            
            # check if it is first half of list (f, nf) and converts to (fiction, non fiction)
            if (is_fiction in FICTION_OPTIONS[:2]):
                new_book.append(KEY_TO_NAME[is_fiction])
                
            else:
                # if it is in the second half of the list is just appends it
                new_book.append(is_fiction)

            # gets the next row that the program can write on
            # this is to avoid the program from overwriting already existing data
            next_row = next_available_row(self.available_books)
            # next row is passed to get the next line that the program should write on
            self.available_books.update('A{}'.format(next_row), [new_book])
            # resets the list to get rid of old data that has been writen to worksheet
            new_book = []

            print('Added to spreadsheet!\n')

def main():
    """This is the main function for this program where everything is being run"""

    # make new object of 'library_manager' class
    manager = library_manager()

    # this list contains all the functions to be referenced later
    # to add more functions, add another nested list with the print statment and the function
    OPTIONS = [['Add Book', manager.add_book]]
    # exit number is used so the menu can be added to quickly
    exit_number = len(OPTIONS) + 1 
    user_choice = 0

    print('This is a library manager!\n')

    time.sleep(1)

    while user_choice != exit_number:
        print('These are your options:')
        for index in range(len(OPTIONS)):
            # this line prints out the text (index 0) and the index in the list (+ 1) to make it easier for users
            print('[{}] {}'.format(index + 1, OPTIONS[index][0]))
            time.sleep(0.5)
 
        user_choice = int_valid_input("Pick an option ({} to exit): ".format(exit_number), 
                                    "Please enter a valid option!\n", 
                                    1, exit_number)
        print() # blank line
        if (user_choice != exit_number):
            OPTIONS[user_choice - 1][1]() # runs the specified function (index 1 of nested list)



    print('Thanks for using this program!')

if (__name__ == '__main__'):
    main()  # runs the program
    