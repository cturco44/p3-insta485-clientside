"""
Insta485 common configuration.
Andrew DeOrio <awdeorio@umich.edu>
"""
import pathlib


# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Cookies
SESSION_COOKIE_NAME = 'login'

# File upload limitations
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Local file upload to var/uploads/
INSTA485_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/"var/uploads"

# Database configuration
DATABASE_FILENAME = INSTA485_ROOT/"var/insta485.sqlite3"
