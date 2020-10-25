"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'M\x98\x10\x8d\xb3Z`\xb6L9g\x82\xc8={\x04\x046\xc6\xbb,\xf2@\x05'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
INSTA485_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'

POSTGRESQL_DATABASE_HOST = "insta485.c3ds50lv2eig.us-east-2.rds.amazonaws.com"
POSTGRESQL_DATABASE_PORT = 5432
POSTGRESQL_DATABASE_USER = "insta485" # OS or WSL username
POSTGRESQL_DATABASE_PASSWORD = 'SLLeexyz01'
POSTGRESQL_DATABASE_DB = "insta485"
