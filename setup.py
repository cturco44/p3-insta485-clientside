"""
Insta485 python package configuration.

Andrew DeOrio <awdeorio@umich.edu>
"""

from setuptools import setup

setup(
    name='insta485',
    version='0.1.0',
    packages=['insta485'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'nodeenv',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
        'psycopg2-binary',
        'Flask-S3==0.3.3',
        'boto3==1.14.9',
    ],
    python_requires='>=3.6',
)
