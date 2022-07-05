def list_valid_input(input_message, error_message, valid_entries):
    """This function gets valid string input that is in a list (valid_entries)"""
    user_input = ''
    
    while not user_input in valid_entries:
        user_input = input(input_message).lower()
        
        if not (user_input in valid_entries):
            print(error_message)
    
    return user_input

def int_valid_input(input_message, error_message, low, high):
    """This function gets valid int input that is between two numbers (high and low)"""
    is_valid = False
    
    while not is_valid:
        try:
            user_input = int(input(input_message))
            if  user_input >= low and user_input <= high:
                is_valid = True
            
            else:
                print(error_message)
        
        except ValueError:
            print(error_message)
    
    return user_input