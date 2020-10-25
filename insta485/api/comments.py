"""Comments API."""
import flask
from flask import jsonify, url_for, request
from insta485.views.post import comment as comment_func
import insta485


class InvalidUsage(Exception):
    """Check invalid usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """init."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Error handling."""
        rv_var = dict(self.payload or ())
        rv_var["message"] = self.message
        return rv_var


@insta485.app.route(
    "/api/v1/p/<int:postid_url_slug>/comments/", methods=["GET", "POST"]
)
def get_comments(postid_url_slug):
    """Comments api main."""
    if "username" in flask.session:
        logname = flask.session["username"]
    else:
        raise InvalidUsage("Forbidden", status_code=403)

    check_post_exists(postid_url_slug)

    if request.method == "POST":
        if not request.json:
            raise InvalidUsage("No comment attached", status_code=400)

        comment_func(logname, postid_url_slug, request.json["text"])

        cur = insta485.model.get_db()
        cur.execute(
            """
            SELECT last_insert_rowid()
        """
        )

        comment = {
            "commentid": cur.fetchall()[0]["last_insert_rowid()"],
            "owner": logname,
            "owner_show_url": url_for("user", user_url_slug=logname),
            "postid": postid_url_slug,
            "text": request.json["text"],
        }
        return jsonify(**comment), 201

    context = retrieve_comment_from_db(postid_url_slug)
    context["url"] = flask.request.path
    return jsonify(**context)


def retrieve_comment_from_db(postid):
    """GET db."""
    cur = insta485.model.get_db()

    cur.execute(
        """
        SELECT *
        FROM comments
        WHERE postid = %s
    """,
        [postid],
    )
    comments = cur.fetchall()

    context = {"comments": []}
    for comment in comments:
        com = {
            "commentid": comment["commentid"],
            "owner": comment["owner"],
            "owner_show_url": url_for("user", user_url_slug=comment["owner"]),
            "postid": comment["postid"],
            "text": comment["text"],
        }

        context["comments"].append(com)
    return context


def check_post_exists(postid):
    """Return whether post exists."""
    cur = insta485.model.get_db()
    cur.execute(
        """
        SELECT owner FROM posts
        WHERE postid = %s
    """,
        [postid],
    )
    post_obj = cur.fetchall()

    if len(post_obj) < 1:
        raise InvalidUsage("Not Found", status_code=404)


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Error handling."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
