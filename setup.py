from setuptools import setup, find_packages

setup(
    name='BabyJournalBot Toolkit',
    version='1.0',
    description='Toolkit of common functions used across BabyJournalBot project',
    author_email='katorov.msu@gmail.com',
    python_requires='>=3.8.0',
    packages=find_packages(),
    install_requires=[
      'python-dateutil>=2.8.1',
      'plotly>=4.14.3',
      'pytz>=2021.1',
    ],
)
