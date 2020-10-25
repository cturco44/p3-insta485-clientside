"""Following."""
import flask
from flask import request, redirect, abort, url_for, session
import insta485


@insta485.app.route("/u/<user_url_slug>/following/", methods=["POST", "GET"])
def show_following(user_url_slug):
    """Show following."""
    if "username" in session:
        user = session["username"]
    else:
        return redirect(url_for("login"))
    if not check_user_url_slug_exists(user_url_slug):
        abort(404)

    # Connect to database
    cur = insta485.model.get_db()

    # IF Post
    if request.method == "POST":
        if "unfollow" in request.form:
            unfollow(user, request.form["username"])
        elif "follow" in request.form:
            follow(user, request.form["username"])
    # GET
    cur.execute(
        """
        SELECT username2 FROM following
        WHERE username1 = %s
    """,
        [user_url_slug],
    )
    test = cur.fetchall()
    list2 = []
    for item in test:
        pair = (
            item["username2"],
            check_login_following(user, item["username2"]),
            get_profile_image(item["username2"]),
        )
        list2.append(pair)
    context = {"list": list2}
    return flask.render_template(
        "following.html", **context, logname=user, slug=user_url_slug
    )


def check_user_url_slug_exists(user_url_slug):
    """Check exist."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT COUNT(*) FROM users
        WHERE username = %s
    """,
        [user_url_slug],
    )
    num_as_string = cur.fetchall()
    # pdb.set_trace()
    return int(num_as_string[0]["COUNT(*)"]) == 1


def unfollow(logged_in, following):
    """Unfollow."""
    cur = insta485.model.get_db()

    cur.execute(
        """
        DELETE FROM following
        WHERE username1 = %s AND username2 = %s
        """,
        [logged_in, following],
    )


def follow(logged_in, follows):
    """Check follow."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        INSERT INTO following (username1, username2)
        VALUES (%s, %s)
        """,
        [logged_in, follows],
    )


def check_login_following(logname, user):
    """Check logged in following."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT COUNT(*) FROM following
        WHERE username1 = %s AND username2 = %s
    """,
        [logname, user],
    )
    num_as_string = cur.fetchall()
    return int(num_as_string[0]["COUNT(*)"]) == 1


def get_profile_image(user):
    """Get profile image filename."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT filename FROM users
        WHERE username = %s
    """,
        [user],
    )
    img = cur.fetchall()
    return img[0]["filename"]
