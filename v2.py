"""
Filename: main.py
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
from valid_input import *


def next_available_row(worksheet):
    """This function gets then next line in a worksheet"""
    # gets the first coloumn of the worksheet
    worksheet_coloumn = list(worksheet.col_values(1))

    # gets the length of items in the coulumn and returns it
    return len(worksheet_coloumn) + 1

def find_book(worksheet, book_name):
    """This function finds the line that a certain book is stored"""
    # gets the first coloumn of the worksheet
    worksheet_items = list(worksheet.col_values(1))
    
    try:
        # trys to find the book inside the coloumn
        # it also adds 1 to the index as lists start from 0 and rows start from 1
        book_row = worksheet_items.index(book_name) + 1
    
    except ValueError:
        # sets book row to -1 indicating a error
        book_row = -1

    return book_row

def clear_row(worksheet, row):
    cells = worksheet.range('A{}:Z{}'.format(row, row))
    for cell in cells:
        cell.value = ''
    
    worksheet.update_cells(cells)
    


class library_manager():

    def __init__(self):
        """This function initialises all the variables to be used in the program"""
        # connects to the service account
        self.service_account = gspread.service_account(filename='config.json')
        self.library_spreadsheet = self.service_account.open('library database')

        # these are for the 2 different worksheets (available, loaned)
        self.available_books = self.library_spreadsheet.worksheet('available')
        self.loaned_books = self.library_spreadsheet.worksheet('loaned')
        
        # to make the program look nice
        self.spacer = '\n_______________________________________________\n'

    def add_book(self):
        """This function allows the user to add books to the database"""
        # this dict allows that program to turn the 'f' and 'nf' to 
        # 'fiction' and 'non fiction' to be writen to in the worksheet
        KEY_TO_NAME = {'f': 'fiction', 'nf': 'non fiction'}
        # this gets the keys (first part of dict items) and makes a list from them
        # in this case the list would be ['f', 'nf']
        FICTION_OPTIONS = ['f', 'nf', 'fiction', 'non fiction']

        

        amount_of_books = int_valid_input('How many books are you adding (1 - 100): ', 
                                          'Please enter a positive integer below (1 - 100)!\n',
                                          1, 100)
        
        new_book = []
        for _ in range(amount_of_books):
            new_book.append([])
        print() # blank line

        for x in range(amount_of_books):
            #populates list
            new_book[x].append(input('What is the name of the book: ').lower())

            is_fiction = list_valid_input('Is the book fiction or non fiction (F / NF): ', 
                                        'Please enter F or NF (fiction or non fiction)!\n', 
                                        FICTION_OPTIONS)
            
            # check if it is first half of list [f, nf] and converts to [fiction, non fiction]
            if (is_fiction in FICTION_OPTIONS[:2]):
                new_book[x].append(KEY_TO_NAME[is_fiction])
                
            else:
                # if it is in the second half of the list is just appends it
                new_book[x].append(is_fiction)

            print(self.spacer)
        
        next_row = next_available_row(self.available_books)
        
        self.available_books.update('A{}'.format(next_row), new_book)
    
    def loan_book(self):
        """This function allows the user to loan books to students"""
        user_loan_book_name = ''
        
        while user_loan_book_name != '#':
            user_loan_book_name = input('Enter the name of the book you would like to loan (# to exit): ').lower()
            
            
            # deletes book from available worksheet
            user_loan_book_row = find_book(self.available_books, user_loan_book_name)
            
            if (user_loan_book_row != -1):
                clear_row(self.available_books, user_loan_book_row)
            
            elif (user_loan_book_row == -1 and user_loan_book_name != '#'):
                print('Sorry, could not find your book')
        
        print(self.spacer)
            
                
        

def main():
    """This is the main function for this program where everything is being run"""

    # make new object of 'library_manager' class
    manager = library_manager()

    # this list contains all the functions to be referenced later
    # to add more functions, add another nested list with the print statment and the function
    OPTIONS = [['Add Book', manager.add_book], ['Loan Book', manager.loan_book]]
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
        print('\n_______________________________________________\n')
        if (user_choice != exit_number):
            OPTIONS[user_choice - 1][1]() # runs the specified function (index 1 of nested list)
            



    print('Thanks for using this program!')

if (__name__ == '__main__'):
    main()  # runs the program
    