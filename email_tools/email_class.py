import os
import smtplib
import socket
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import Tuple, Union

if __name__ == '__main__':
    from encryption import get_email, get_pwd
else:
    from email_tools.encryption import get_email, get_pwd


class Email:
    """ Email class
    
        Sends email with attachments to an email. """

    def __init__(self, smtp_server: str = None, receiver_email: str = None, sender_email: str = None, sender_pwd: str = None) -> None:
        """ Initialize the email class
            
            Args:
                smtp_server (str, optional): Email server. Defaults to None. * If port 25 is available you might want to do smtp_server='localhost:25' *
                receiver_email (str, optional): Receiver email. Defaults to None.
                sender_email (str, optional): Sender email. Defaults to None.
                sender_pwd (str, optional): Sender password. Defaults to None. """

        if sender_email is not None:
            assert sender_pwd, "If you specify a sender email you must also specify a password"

        self.hostname = socket.gethostname()
        self.smtp_server = smtp_server or "smtp.isr.uc.pt:587"

        self.receiver_email = receiver_email or get_email("isr")
        self.sender_email = sender_email or get_email("isr")
        self.password = sender_pwd or get_pwd("isr")

    def __call__(self, *args, **kwds) -> None:
        """ Sends an email with specified subject, body and attachments """
        self.send(*args, **kwds)

    def create_message(self, subject: str, body: str, attachments: Union[Tuple[str], str]):
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.hostname + ": " + subject

        # send these files
        if attachments is not None:
            if isinstance(attachments, tuple) or isinstance(attachments, list):
                for file in attachments:
                    assert isinstance(file, str), f"Filename: {file} , must be of type str"
                    # print(file)
                    if os.path.isfile(file):  # File exosts
                        self.append_attachment_to_message(file)
                    else:
                        body += f"\n\nFile: {file} , does not exist"

            elif isinstance(attachments, str):
                # print(attachments)
                if os.path.isfile(attachments):  # File exosts
                    self.append_attachment_to_message(attachments)
                else:
                    body += f"\n\nFile: {attachments} , does not exist"

            else:
                raise TypeError(f"Filenames: {attachments} , must be of type str, list of str or tuple of str")

        self.message.attach(MIMEText(body, "plain"))

    def append_attachment_to_message(self, filename: str):
        with open(filename, "rb") as file:
            part = MIMEApplication(file.read(), Name=basename(filename))
            part["Content-Disposition"] = f"attachment; filename={basename(filename)}"

            self.message.attach(part)

    def connect_server_and_send_email(self):
        with smtplib.SMTP(*(self.smtp_server.split(":"))) as server:
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(self.message["From"], self.password)

            server.sendmail(self.message["From"], self.message["To"], self.message.as_string())

    def send(self, subject: str = "Subject", body: str = "Body", attachments: Tuple[str] = None):
        self.create_message(subject=subject, body=body, attachments=attachments)
        self.connect_server_and_send_email()
        self.cleannup()

    def cleannup(self):
        pass


if __name__ == "__main__":
    ### EMAIL USAGE
    Email().send(subject="subject", body="this is the body", attachments=["email_tools/credentials.csv", "email_tools/some_file.txt", "email_tools/not_a_file.txt"])  # or
    # Email()(subject='this is the subject', body='this is the body', attachments=['some_file.txt', 'not_a_file.txt'])

    pass
