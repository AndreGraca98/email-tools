# tools

## Usage

Assuming user is in `RandomUtilities/tools/`

### Create credentials for the first time

```python
from tools.encryption import create_credentials_csv, generate_key

generate_key()
create_credentials_csv( ["email@domain", "second.email@domain", "third.email.email@different.domain"], 
                        ["password", "pwd", "1234"], 
                        force=True )
```

### Accessing credentials

```python
from tools.encryption import get_credentials, get_all_credentials

print( get_credentials('domain') )
print( get_credentials('domain:1') )
print( get_all_credentials() )
```

### Send email

```python
from tools.email_class import Email

Email().send(attachments='some_file.txt')
# OR
Email()(attachments='some_file.txt')
# OR
Email(sender_email=input('sender email: '), sender_pwd=input('sender pwd: ')).send(attachments='tools/some_file.txt')
# OR
# If port 25 is available
Email(smtp_server='localhost:25').send(attachments='some_file.txt')

    
```

## In this folder

- [x]  `tools/email_class.py` :: send an email with subject, body and an attacment using python smtplib
- [x]  `tools/runner_wrapper.py` :: wrapper to send an email notification if error occurs
- [x]  `tools/encryption.py` :: encrypt and decrypt data using Fernet encryption. Create and retrieve encrypted credentials
