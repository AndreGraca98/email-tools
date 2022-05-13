from setuptools import setup

setup(name='email_tools',
      version='1.0',
      description='A package to send emails and error notifications from python scripts',
      author='André Graça',
      author_email='andre.graca@isr.uc.pt',
      platforms='Python',
      packages=['email_tools'],
      install_requires=[
        'pandas',
        'cryptography',
    ],
     )


from email_tools import create_credentials_csv, generate_key

generate_key()
create_credentials_csv(force=True, MANUAL=True)