# email-tools

## Setup

```bash
git clone https://github.com/AndreGraca98/email-tools.git
# Assuming user is in `email-tools/`
python setup.py develop -U

# OR

pip install git+https://github.com/AndreGraca98/email-tools.git
```

## Usage

### Creating credentials for the first time

Run on a bash terminal:

```bash
python -c "import email_tools as et; et.create_credentials_csv(force=True, MANUAL=True)"
```

Run on python terminal:

```python
from email_tools import create_credentials_csv, generate_key

generate_key()
create_credentials_csv( ["email@domain", "second.email@domain", "third.email.email@different.domain"], 
                        ["password", "pwd", "1234"], 
                        force=True )

# OR
create_credentials_csv(MANUAL=True)
```

### Accessing credentials

```python
from email_tools import get_credentials, get_all_credentials

print( get_credentials('domain') )
print( get_credentials('domain:1') )
print( get_all_credentials() )
```

### Sending email

```python
from email_tools import Email

Email()('this is the subject!', 'and this is the body', 'some_file.txt')
# OR
Email()(attachments='some_file.txt')
# OR
Email().send(attachments='some_file.txt')
# OR
Email(sender_email=input('sender email: '), sender_pwd=input('sender pwd: ')).send(attachments='tools/some_file.txt')
# OR
# If port 25 is available
Email(smtp_server='localhost:25').send(attachments='some_file.txt')

    
```

### Sending error email

```python
from email_tools import email_notification_wrapper, get_email

email = get_email('isr')

@email_notification_wrapper
def function():
    print(f'Press Ctrl+C to send an error message to {email}')
    for t in range(10, 0, -1):
        print(f'Time left: {t} seconds', end='\r')
        time.sleep(1)
        
    raise RuntimeError(f'Ctrl+C not pressed. Sending Runtime Error message to {email}')
        
function()
```

## In this folder

- [x]  `email_tools/email_class.py` :: send an email with subject, body and an attacment using python smtplib
- [x]  `email_tools/runner_wrapper.py` :: wrapper to send an email notification if error occurs
- [x]  `email_tools/encryption.py` :: encrypt and decrypt data using Fernet encryption. Create and retrieve encrypted credentials
