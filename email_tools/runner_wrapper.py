import time
import traceback as tb
from datetime import datetime

from .email_class import Email
from .encryption import get_email

def email_notification_wrapper(func):
    """ Wrapper function to send an email if an error occurs while running the main function. 

    Args:
        func (function): main function
    """

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except:
            e = tb.format_exc()
            Email()(
                subject="Error occured !", body=f'Time: {datetime.today().strftime("%Y-%m-%d %Hh%Mm%Ss")}\n\nERROR:\n\n{e}\n-----',
            )
            print("ERROR:\n\n", e)
        finally:
            print("DONE!")

    return wrapper


@email_notification_wrapper
def example_function():
    email = get_email('isr')
    
    print(f'Press Ctrl+C to send an error message to {email}')
    for t in range(10, 0, -1):
        print(f'Time left: {t} seconds', end='\r')
        time.sleep(1)
        
    raise RuntimeError(f'Ctrl+C not pressed. Sending Runtime Error message to {email}')
        
