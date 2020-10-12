import flask
from flask import jsonify, url_for
from insta485.views.post import comment
import insta485

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@insta485.app.route('/api/v1/p/<int::postid_url_slug>/comments/', methods=["GET", "POST"])
def get_comments(postid_url_slug):
    if "username" in flask.session:
        logname = flask.session["username"]
    else:
        raise InvalidUsage("Forbidden", status_code=403)

    check_post_exists(postid_url_slug)



    if request.method == "POST":
        if not request.json:
            raise InvalidUsage("No comment attached", status_code=400)

        comment(logname, postid_url_slug, request.json['text'])

        connection = insta485.model.get_db()
        cur = connection.execute("""
            SELECT last_insert_rowid()
        """
        )

        comment = {
            "commentid": cur.fetchall()[0]['last_insert_rowid()'],
            "owner": logname,
            "owner_show_url": url_for('user', user_url_slug=logname),
            "postid": postid_url_slug,
            "text": request.json['text']
        }
        return jsonify(**comment)

    context = retrieve_comment_from_db(postid_url_slug)
    context['url'] = flask.request.path
    return jsonify(**context)

def retrieve_comment_from_db(postid):
    connection = insta485.model.get_db()

    cur = connection.execute("""
        SELECT *
        FROM comments
        WHERE postid = ?
    """, [postid]
    )
    comments = cur.fetchall()

    context = {"comments":[]}
    for comment in comments:
        c = {"commentid": comment['commentid'], "owner": comment['owner'],
            "owner_show_url": url_for('user', user_url_slug=comment['owner']),
            "postid": comment['postid'], 'text': comment['text']}

        context['comments'].append(c)
    return context

def check_post_exists(postid):
    """Return whether post exists."""
    connection = insta485.model.get_db()
    cur = connection.execute("""
        SELECT owner FROM posts
        WHERE postid = ?
    """, [postid]
    )
    post_obj = cur.fetchall()

    if len(post_obj) < 1:
        raise InvalidUsage("Not Found", status_code=404)

@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
