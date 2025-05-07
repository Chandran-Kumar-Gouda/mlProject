import logging
import sys  # Importing the sys module to access exception and traceback info

# Function to create a detailed error message using traceback info
def error_message_details(error, error_details: sys):
    # Extract traceback info (type, value, traceback object) — we only need the traceback object
    _, _, exc_tb = error_details.exc_info()

    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Create a formatted error message string
    error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,            # File where the error happened
        exc_tb.tb_lineno,     # Line number in that file
        str(error)            # The actual error message (e.g., division by zero)
    )

    return error_message  


#  Custom exception class that inheritate Python's built-in Exception class
class CustomException(Exception):
    # Constructor method to initialize the custom exception
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Call base class constructor to set the original message                                 
        self.error_message = error_message_details(error_message,error_detail) # Generate a full error message using the helper function and store it

    # When the exception object is printed, this method controls what gets shown
    def __str__(self):
        return self.error_message  # Return the detailed error message instead of just a short message
    

