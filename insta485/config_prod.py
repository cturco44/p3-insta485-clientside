"""
Production configuration.
Andrew DeOrio <awdeorio@umich.edu>
"""
import os

# Secret key for encrypting cookies.  It's bad practice to save this in the
# source code, so in production, the secret key should be set as an environment
# variable.
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No FLASK_SECRET_KEY environment variable.")
POSTGRESQL_DATABASE_PASSWORD = os.environ.get("POSTGRESQL_DATABASE_PASSWORD")
if not POSTGRESQL_DATABASE_PASSWORD:
    raise ValueError("No POSTGRESQL_DATABASE_PASSWORD environment variable.")

# Production Database Config

# Use your own AWS database host
POSTGRESQL_DATABASE_HOST = "insta485.c5wh75qgggje.us-east-2.rds.amazonaws.com" 
POSTGRESQL_DATABASE_PORT = 5432
POSTGRESQL_DATABASE_USER = "insta485"
POSTGRESQL_DATABASE_DB = "insta485"

# AWS S3 static files
# https://flask-s3.readthedocs.io/en/latest/
FLASKS3_DEBUG = True
FLASKS3_ACTIVE = True
FLASKS3_BUCKET_NAME = "eroyama.static.insta485.com" # Use your own AWS bucket name
FLASKS3_REGION = "us-east-2"
FLASKS3_FORCE_MIMETYPE = True
FLASKS3_USE_HTTPS = False
FLASKS3_CDN_DOMAIN = "d7ndtapyu5ir1.cloudfront.net" # Use your own CDN domain name

# AWS S3 file upload
AWS_S3_UPLOAD_BUCKET = "eroyama.uploads.insta485.com" # Use your own uploads S3 bucket name
AWS_S3_UPLOAD_REGION = "us-east-2"
AWS_S3_UPLOAD_FOLDER = "uploads"