import os
from pathlib import Path
from typing import List

import pandas as pd
from cryptography.fernet import Fernet


def generate_key():
    if os.path.isfile(f"{Path.home()}/.fernet_key"):
        print(f'Key already exists in {Path.home()/".fernet_key"}')
        return
    
    key = Fernet.generate_key()
    with open(f"{Path.home()}/.fernet_key", "w") as f:
        f.write(str(key))


def get_key() -> bytes:
    with open(f"{Path.home()}/.fernet_key") as f:
        key = eval(f.readline())

    return key


def encrypt(message: str, key: bytes):
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage


def decrypt(encMessage: str, key: bytes):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage


def create_credentials_csv(email_list: List[str]=None, pwd_list: List[str]=None, force=False, path: Path = Path.home() / ".email_credentials", MANUAL=False):
    """ Creates encrypted file with emails and respective passwords

    Args:
        email_list (List[str], optional): Email list. Defaults to None.
        pwd_list (List[str], optional): Password list. Defaults to None.
        force (bool, optional): Force new file creation. Defaults to False.
        path (Path, optional): Base directory. Defaults to Path.home()/"tools".
    """
    if MANUAL:
        generate_key()
        email_list=[input('Enter sender email ["user@isr.uc.pt"]: ')]; pwd_list=[input('Enter sender pwd ["password"]: ')]
        
    base_dir = path if __name__ != '__main__' else Path('')
    if not force:
        if os.path.isfile(str(base_dir / "credentials.csv")):
            print("File credentials.csv already exists")
            return
        # assert not os.path.isfile(str(base_dir / "credentials.csv")), "File credentials.csv already exists"
        
    assert len(email_list)>0 and len(email_list) == len(pwd_list), f'Email and Password list must have same number of elements greater than zero! Email: {len(email_list)} ; Password: {len(pwd_list)}'
    
    key = get_key()

    data = [[email.split("@")[1].split(".")[0], encrypt(email, key), encrypt(pwd, key)] for email, pwd in zip(email_list, pwd_list) ]

    df = pd.DataFrame(data, columns=["domain", "email", "password"], dtype=str)
    df.set_index(['domain', df.groupby(['domain']).cumcount()], inplace=True)
    
    # print(df)
    if not base_dir.exists(): Path.mkdir(path)

    df.to_csv(str(base_dir / "credentials.csv"), sep=" ")#, index_label="index")  # , index=None)


def get_data(domain: str, column_name: str, path: Path = Path.home() / ".email_credentials") -> str:
    """ Retrieves decrypted data from emails/passwords dataframe

    Args:
        domain (str): email domain. Can be split with : to access different values in the dataset 
        column_name (str): email or password
        path (Path, optional): Base directory. Defaults to Path.home()/"tools".

    Returns:
        str: decrypted data from specified column
    """
    assert column_name in ["email", "password"], f"Column name {column_name} does not exist. Choose from [password, email]"
    base_dir = path if __name__ != '__main__' else Path('')

    key = get_key()
    df = pd.read_csv(str(base_dir / "credentials.csv"), sep=" ", index_col=[0,1])  # , sep=" ")

    # assert domain in df.index, f"Domain '{domain}' does not exist. Choose from {df.index.values}"
    if len(domain.split(':')) > 1:
        dom, n = domain.split(':')
        index_ = (dom, int(n))
    else:
        index_ = (domain, 0)
               
    return decrypt(eval(df.loc[index_, column_name]), key)


def get_email(domain: str):
    return get_data(domain=domain, column_name="email")


def get_pwd(domain: str):
    return get_data(domain=domain, column_name="password")


def get_credentials(domain: str):
    return get_email(domain=domain), get_pwd(domain=domain)

def get_all_credentials(path: Path = Path.home() / ".email_credentials"):
    base_dir = path if __name__ != '__main__' else Path('')
    
    df = pd.read_csv(str(base_dir / "credentials.csv"), sep=" ")
    key = get_key()
    emails = [decrypt(eval(e), key=key) for e in df['email'].values.tolist()]
    passwords = [decrypt(eval(p), key=key) for p in df['password'].values.tolist()]

    return list(zip(emails, passwords)), df.domain.values.tolist()
