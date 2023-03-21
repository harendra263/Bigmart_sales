import sys

def error_message_details(error: str, error_details: sys):
    _, _, exc_tbl = error_details.exc_info()
    filename = exc_tbl.tb_frame.f_code.co_filename
    return f'Error occcured in python script {filename} line number {exc_tbl.tb_lineno} error message {error}'


class CustomException(Exception):
    def __init__(self, error_message: str, error_details: sys) -> None:
        super().__init__(error_message)
        self.error_message = error_message_details(error=error_message, error_details=error_details)
    
    def __str__(self) -> str:
        return self.error_message


