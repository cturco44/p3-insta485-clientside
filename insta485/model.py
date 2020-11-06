"""Insta485 model (database) API."""
import flask
import psycopg2
import psycopg2.extras
from pathlib import Path
import uuid
import tempfile
import botocore
import boto3
import insta485


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if "db_con" not in flask.g:
        flask.g.db_con = psycopg2.connect(
            host=insta485.app.config['POSTGRESQL_DATABASE_HOST'],
            port=insta485.app.config['POSTGRESQL_DATABASE_PORT'],
            user=insta485.app.config['POSTGRESQL_DATABASE_USER'],
            password=insta485.app.config['POSTGRESQL_DATABASE_PASSWORD'],
            database=insta485.app.config['POSTGRESQL_DATABASE_DB'],
        )
        flask.g.db_cur = flask.g.db_con.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
    return flask.g.db_cur


@insta485.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    db_cur = flask.g.pop('db_cur', None)
    db_con = flask.g.pop('db_con', None)
    if db_con is not None:
        db_con.commit()
        db_cur.close()
        db_con.close()


@insta485.app.route("/uploads/<filename>")
def get_upload(filename):
    """Serve one file from the uploads directory."""
    # In production, download the image from S3 to a temp file and serve it
    if "AWS_S3_UPLOAD_BUCKET" in insta485.app.config:
        s3_client = boto3.client("s3")
        bucket = insta485.app.config["AWS_S3_UPLOAD_BUCKET"]
        key = "{folder}/{filename}".format(
            folder=insta485.app.config.get("AWS_S3_UPLOAD_FOLDER"),
            filename=filename,
        )

        # Download the image to a temporary in-memory file
        # https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj
        tmpfileobj = tempfile.SpooledTemporaryFile()
        try:
            s3_client.download_fileobj(bucket, key, tmpfileobj)
        except botocore.exceptions.ClientError as error:
            LOGGER.error(error)
            flask.abort(400)

        # Serve the file to the user
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.send_file
        tmpfileobj.seek(0)
        return flask.send_file(tmpfileobj, attachment_filename=filename)

    # In development, send the file directly from the file system
    return flask.send_from_directory(
        insta485.app.config['UPLOAD_FOLDER'],
        filename
    )


def allowed_file(filename):
    """Return true if filename has allowed extension."""
    extension = Path(filename).suffix
    extension = extension.replace(".", "").lower()
    return extension in insta485.app.config["ALLOWED_EXTENSIONS"]


def save_upload_to_s3(fileobj, filename):
    """Upload file object to S3.
    This function is used in production for media uploads.
    Docs
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    """
    s3_client = boto3.client("s3")
    bucket = insta485.app.config["AWS_S3_UPLOAD_BUCKET"]
    key = "{folder}/{filename}".format(
        folder=insta485.app.config.get("AWS_S3_UPLOAD_FOLDER"),
        filename=filename,
    )
    try:
        s3_client.upload_fileobj(fileobj, bucket, key)
    except botocore.exceptions.ClientError as error:
        LOGGER.error(error)
        flask.abort(400)
    LOGGER.info("Saved upload to S3 %s/%s", bucket, key)


def delete_upload_from_s3(filename):
    """Delete file object from S3.
    This function is used in production for media uploads.
    Docs
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    """
    s3_client = boto3.client("s3")
    bucket = insta485.app.config["AWS_S3_UPLOAD_BUCKET"]
    key = "{folder}/{filename}".format(
        folder=insta485.app.config.get("AWS_S3_UPLOAD_FOLDER"),
        filename=filename,
    )
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
    except botocore.exceptions.ClientError as error:
        LOGGER.error(error)
        flask.abort(400)
    LOGGER.info("Deleted upload from S3 %s/%s", bucket, key)


def save_upload_to_disk(fileobj, filename):
    """Save file object to on-disk uploads folder.
    This function is used in development for media uplods.
    """
    path = insta485.app.config["UPLOAD_FOLDER"]/filename
    fileobj.save(path)
    LOGGER.info("Saved upload to disk %s", path)


def delete_upload_from_disk(filename):
    """Delete file from on-disk uploads folder.
    This function is used in development for media uplods.
    """
    path = insta485.app.config["UPLOAD_FOLDER"]/filename
    path.unlink()


def create_upload():
    """Handle one upload POST request.  Return filename of saved file."""
    # User is not logged in
    if "username" not in flask.session:
        flask.abort(403)

    # Post request has no file part
    if "file" not in flask.request.files:
        flask.abort(400)
    file = flask.request.files["file"]

    # User did not select file
    if file.filename == "":
        flask.abort(400)

    # Disallowed file extension
    if not allowed_file(file.filename):
        flask.abort(400)

    # New filename is a unique ID
    uuid_filename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=Path(file.filename).suffix
    )

    # Upload to S3 if the configuration provides AWS_S3_UPLOAD_BUCKET.
    # Typically, this would be set in production.
    if "AWS_S3_UPLOAD_BUCKET" in insta485.app.config:
        save_upload_to_s3(file, uuid_filename)
    else:
        save_upload_to_disk(file, uuid_filename)

    # Return hash_basename for adding to database
    return uuid_filename


def remove_upload(filename):
    """Handle one request to delete a media upload."""
    # Upload to S3 if the configuration provides AWS_S3_UPLOAD_BUCKET.
    # Typically, this would be set in production.
    if "AWS_S3_UPLOAD_BUCKET" in insta485.app.config:
        delete_upload_from_s3(filename)
    else:
        delete_upload_from_disk(filename)