import time
from email_tools import Email, email_notification_wrapper, generate_key, create_credentials_csv, get_all_credentials, get_credentials, example_function


if __name__ == '__main__':
    generate_key()
    email=input('Enter sender email ["user@isr.uc.pt"]: '); pwd=input('Enter sender pwd ["password"]: ')
    create_credentials_csv([email], [pwd], force=False)
    
    print( get_all_credentials() )
    
    email, pwd = get_credentials('isr')

    Email(sender_email=email, sender_pwd=pwd).send(attachments=['email_tools/credentials.csv','email_tools/some_file.txt'])
    
    
    example_function()
    
    
    pass