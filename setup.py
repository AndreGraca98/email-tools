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
