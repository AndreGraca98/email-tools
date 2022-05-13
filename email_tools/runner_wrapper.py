import time
import traceback as tb
from datetime import datetime

if __name__ == '__main__':
    from email_class import Email
else:
    from email_tools.email_class import Email


def email_notification(func):
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


@email_notification
def example_func(a, b=99):
    for _ in range(1_000):
        time.sleep(0.01)

    print(a, b)


if __name__ == "__main__":
    # example_func(123, b=54)

    pass
