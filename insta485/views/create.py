"""Create."""
import uuid
import pathlib
import flask
from flask import request, redirect, abort, url_for
import insta485
from insta485.views.password import hash_password


@insta485.app.route("/accounts/create/", methods=["POST", "GET"])
def create_account():
    """Create account."""
    if "username" in flask.session:
        return redirect(url_for("show_edit"))

    if request.method == "POST":
        if "fullname" not in request.form:
            abort(400)
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        unhashed_password = request.form["password"]

        if user_exists(username):
            abort(409)
        if "file" not in request.files:
            abort(400)
        file = request.files["file"]
        filename = upload_file(file)

        if unhashed_password == "":
            abort(400)
        hashed_password_1 = hash_password(unhashed_password)

        add_user(filename, fullname, username, email, hashed_password_1)
        flask.session["username"] = username
        return flask.redirect(url_for("show_index"))

    return flask.render_template("create.html")


def user_exists(username):
    """Check user exist."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        """
        SELECT COUNT(*) FROM users
        WHERE username = ?
    """,
        [username],
    )
    num_as_string = cur.fetchall()
    return int(num_as_string[0]["COUNT(*)"]) == 1


def add_user(filename, fullname, username, email, hashed_password):
    """Check add user."""
    connection = insta485.model.get_db()
    connection.execute(
        """
        INSERT INTO users(username, fullname, email, filename, password)
        VALUES (?, ?, ?, ?, ?)
    """,
        [username, fullname, email, filename, hashed_password],
    )


def upload_file(fileobj):
    """Upload file."""
    filename = fileobj.filename
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex, suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)

    return uuid_basename
