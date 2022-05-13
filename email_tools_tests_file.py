import time
from email_tools import Email, email_notification, generate_key, create_credentials_csv, get_all_credentials, get_credentials


if __name__ == '__main__':
    generate_key()
    email=input('Enter sender email ["user@isr.uc.pt"]: '); pwd=input('Enter sender pwd ["password"]: ')
    create_credentials_csv([email], [pwd], force=False)
    
    print( get_all_credentials() )
    
    email, pwd = get_credentials('isr')

    Email(sender_email=email, sender_pwd=pwd).send(attachments=['email_tools/credentials.csv','email_tools/some_file.txt'])
    
    @email_notification
    def function():
        print(f'Press Ctrl+C to send an error message to {email}')
        for t in range(10, 0, -1):
            print(f'Time left: {t} seconds', end='\r')
            time.sleep(1)
            
        raise RuntimeError(f'Ctrl+C not pressed. Sending Runtime Error message to {email}')
            
    function()
    
    
    pass