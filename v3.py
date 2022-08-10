"""
Filename: v3.py
Author: Varun Goel
Date: 10 / 08 / 22
Description: This program will allow the user to:
    interact with a google spreadsheet and add books to a database
    allow the user to loan books to students
    allow users to return books
    
Version: 3.0

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
    
    if (book_name in worksheet_items):
        book_row = worksheet_items.index(book_name) + 1
    
    else:
        book_row = -1

    return book_row

def move_book(worksheet1, worksheet2, rows, range1='A', range2='Z'):
    """This function moves a book from one worksheet to another"""
    
    new_cells = []
    
    for _ in range(len(rows)):
        new_cells.append([])
    
    # stores the row
    for index in range(len(rows)):
        
        # gets the current rows data
        cells = worksheet1.range('{}{}:{}{}'.format(range1, rows[index], 
                                                    range2, rows[index]))
        
        
        # clears all the old cells
        for cell in cells:
            new_cells[index].append(cell.value)
            cell.value = ''
        
        
        # updates with old cells that have been cleared
        worksheet1.update_cells(cells)
        
    # adds cells from other worksheet
    worksheet2.update('A{}'.format(next_available_row(worksheet2)), new_cells)
    
def delete_gaps(worksheet):
    """Takes a worksheet and gets rid of white spaces"""
    good_rows = []
    good_rows_content = []
    # gets the first coloumn of the worksheet
    worksheet_coloumn = list(worksheet.col_values(1))
    
    for row in range(len(worksheet_coloumn)):
        if (worksheet_coloumn[row] != ''):
            good_rows.append(row + 1)
    
    for good_row in good_rows:
        good_rows_content.append(worksheet.get('A{}:Z{}'.format(good_row, good_row))[0])
    
    worksheet.clear()
    
    worksheet.update('A1', good_rows_content)
        
    

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
                                          'Please enter a positive integer between (1 - 100)!\n',
                                          1, 100)
        
        if (amount_of_books + next_available_row(self.available_books) <= 1000):
        
            new_book = []
            for _ in range(amount_of_books):
                new_book.append([])
            print() # blank line

            for x in range(amount_of_books):
                #populates list
                book_name = input('What is the name of the book: ').lower()
                
                # checks if book is in library
                if (find_book(self.available_books, book_name) == -1):
                    # if it is not, it adds the name
                    new_book[x].append(book_name)
                
                else:
                    # otherwise it restarts at the top of the loop
                    print('This book has already been added to the library.\n')
                    continue 

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
        
        else:
            print('Sorry, the library does not have enough space for that amount of books.')
    
    def loan_book(self):
        """This function allows the user to loan books to students"""
        
        # this list is used for storing all the rows of te books that the user is loaning
        book_rows = []
        
        # name of book
        loan_book = ''
        
        # repeats until user enters '#'
        while loan_book != '#':
            loan_book = input('Please enter the name of the book (# to exit): ').lower()
            
            # finds the row of the said book name
            book_row = find_book(self.available_books, loan_book)
            
            # if the function does not return -1 (not found) it adds the new row to a list
            if (book_row != -1):
                book_rows.append(book_row)
                print('Found book!')
            
            # if the book row is not found and not '#' (exit char) it will tell the user
            elif (book_row == -1 and loan_book != '#'):
                print('Sorry, could not find your book.')
        
        # moves the books if there are books to move
        if (book_rows != []):
            move_book(self.available_books, self.loaned_books, book_rows, range2='B')
            print('Loaned out books.')
        
        
        # gets rid of gaps
        delete_gaps(self.available_books)
        
        print(self.spacer)
    
    def return_book(self):
        """This function allows users to reutrn books"""
        book_rows = []
        
        # name of book
        return_book = ''
        
        # repeats until user enters '#'
        while return_book != '#':
            return_book = input('Please enter the name of the book (# to exit): ').lower()
            
            # finds the row of the said book name
            book_row = find_book(self.loaned_books, return_book)
            
            # if the function does not return -1 (not found) it adds the new row to a list
            if (book_row != -1):
                book_rows.append(book_row)
                print('Found book!')
            
            # if the book row is not found and not '#' (exit char) it will tell the user
            elif (book_row == -1 and return_book != '#'):
                print('Sorry, could not find the book.')
        
        # moves the books 
        
        if (book_rows != []):
            move_book(self.loaned_books, self.available_books, book_rows, range2='D')
            print('Returned books.')
        
        # gets rid of gaps
        delete_gaps(self.loaned_books)
        
        print(self.spacer)
        
             

def main():
    """This is the main function for this program where everything is being run"""    

    # make new object of 'library_manager' class
    manager = library_manager()

    # this list contains all the functions to be referenced later
    # to add more functions, add another nested list with the print statment and the function
    OPTIONS = [['Add Book', manager.add_book], 
               ['Loan Book', manager.loan_book], 
               ['Return Book', manager.return_book]]
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
            time.sleep(0.2)
 
        user_choice = int_valid_input("Pick an option ({} to exit): ".format(exit_number), 
                                    "Please enter a valid option!\n", 
                                    1, exit_number)
        print('\n_______________________________________________\n')
        if (user_choice != exit_number):
            OPTIONS[user_choice - 1][1]() # runs the specified function (index 1 of nested list)
            



    print('Thanks for using this program!')

if (__name__ == '__main__'):    
    main()  # runs the program
    