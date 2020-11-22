"""
Insta485 development configuration.
Andrew DeOrio <awdeorio@umich.edu>
"""

# Secret key for encrypting cookies.  Never hardcode this in production!
SECRET_KEY = b'M\x98\x10\x8d\xb3Z`\xb6L9g\x82\xc8={\x04\x046\xc6\xbb,\xf2@\x05'

# Development Database Config
POSTGRESQL_DATABASE_HOST = "localhost"
POSTGRESQL_DATABASE_PORT = 5432
POSTGRESQL_DATABASE_USER = "danielchentailee" # OS or WSL username
POSTGRESQL_DATABASE_PASSWORD = None
POSTGRESQL_DATABASE_DB = "insta485"
