"""Insta485 index (main) view.

URLs include: /
"""
import arrow
import flask
from flask import request, redirect, url_for
import insta485
from insta485.views.post import like_post, unlike_post, comment


@insta485.app.route("/", methods=["POST", "GET"])
def show_index():
    """Display / route."""
    # Connect to database
    cur = insta485.model.get_db()

    if "username" in flask.session:
        logname = flask.session["username"]
    else:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "like" in request.form:
            like_post(logname, request.form["postid"])
        elif "unlike" in request.form:
            unlike_post(logname, request.form["postid"])
        elif "comment" in request.form:
            comment(logname, request.form["postid"], request.form["text"])
        return redirect(url_for("show_index"))

    # ALL USERS logname follows
    cur.execute(
        """
        SELECT username2 FROM following
        WHERE username1 = %s
    """,
        [logname]
    )

    # Generate SQL query for posts in order
    following = cur.fetchall()
    following.append({"username2": logname})
    query = "SELECT * FROM posts\nWHERE"
    for i, item in enumerate(following):
        if i == 0:
            query += " owner = " + "'" + item["username2"] + "'"
        else:
            query += " OR owner = " + "'" + item["username2"] + "'"
    query += "\nORDER BY postid DESC"
    cur = insta485.model.get_db()
    cur.execute(query)
    posts = cur.fetchall()

    for i in posts:
        # Humanize timestamps
        arrow_obj = arrow.get(i["created"])
        timestamp = arrow_obj.humanize()
        i["created"] = timestamp

        # add comments
        i["comments"] = list_comments(i["postid"])

        # add num_likes
        i["num_likes"] = num_likes(i["postid"])

        # add_owner_liked bool
        i["logname_liked"] = logname_liked(i["postid"], logname)

        # add profile_pic
        i["owner_pic"] = owner_profile_pic(i["owner"])

    return flask.render_template("index.html", posts=posts, logname=logname)


def list_comments(post_id):
    """List comments."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT * FROM comments
        WHERE postid = %s
        ORDER BY commentID ASC
    """,
        [post_id],
    )
    comments = cur.fetchall()
    for i in comments:
        arrow_obj = arrow.get(i["created"])
        timestamp = arrow_obj.humanize()
        i["created"] = timestamp
    return comments


def num_likes(post_id):
    """Get num likes from db."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT COUNT(*) FROM likes
        WHERE postid = %s
    """,
        [post_id],
    )
    num_as_string = cur.fetchall()
    return int(num_as_string[0]["count"])


def logname_liked(post_id, logname):
    """See if logname liked."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT COUNT(*) FROM likes
        WHERE postid = %s AND owner = %s
    """,
        [post_id, logname],
    )
    num_as_string = cur.fetchall()
    return int(num_as_string[0]["count"]) == 1


def owner_profile_pic(owner):
    """Filename profile pic getter."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT filename FROM users
        WHERE username = %s
    """,
        [owner],
    )
    filename = cur.fetchall()
    return filename[0]["filename"]
