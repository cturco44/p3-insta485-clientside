"""Deletes page."""
import os
import flask
from flask import request, redirect, url_for
import insta485
from insta485.config_common import UPLOAD_FOLDER


@insta485.app.route("/accounts/delete/", methods=["POST", "GET"])
def delete_account():
    """Delete page."""
    if "username" not in flask.session:
        return redirect(url_for("login"))
    user = flask.session["username"]
    if request.method == "POST":
        if "delete" in request.form:
            delete_user(user)
            del flask.session["username"]
            return redirect(url_for("create_account"))
    return flask.render_template("delete.html", logname=user)


def delete_user(user):
    """Delete user from database."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT filename FROM posts
        WHERE owner = %s
        """,
        [user],
    )
    filenames = cur.fetchall()
    delete_images(filenames)

    cur.execute(
        """
        SELECT filename FROM users
        WHERE username = %s
        """,
        [user],
    )
    profile_pic = cur.fetchall()
    delete_images(profile_pic)

    cur.execute(
        """
        DELETE FROM users
        WHERE username = %s
        """,
        [user],
    )


def delete_images(list_input):
    """Delete image."""
    for item in list_input:
        #os.remove(str(UPLOAD_FOLDER / item["filename"]))
        insta485.model.remove_upload(item['filename'])
