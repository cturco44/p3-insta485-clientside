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
POSTGRESQL_DATABASE_PASSWORD = '2l39RDWX88tOvYGavtjD'
POSTGRESQL_DATABASE_DB = "insta485"

# AWS S3 static files
# https://flask-s3.readthedocs.io/en/latest/
FLASKS3_DEBUG = True # Enables Flask-S3's debug mode
FLASKS3_ACTIVE = True # This setting allows you to toggle whether Flask-S3 is active or not
FLASKS3_BUCKET_NAME = "danclee.static.insta485.com" # Add your own root bucket name here, replacing uniqname with your uniqname
FLASKS3_REGION = "us-east-2" # Sets up the AWS region to host your static assets in
FLASKS3_FORCE_MIMETYPE = True # Always set the Content-Type header on the S3 files irrespective of gzipping
FLASKS3_USE_HTTPS = False # We will only be using HTTP for now
FLASKS3_CDN_DOMAIN = "d31amjvxmoe4es.cloudfront.net" # Add your own CDN Domain Name here
