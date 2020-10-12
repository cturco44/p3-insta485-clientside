"""REST API for on post."""
import flask
import insta485
from insta485.api.comments import InvalidUsage, handle_invalid_usage


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
def get_post(postid):
  """Return details for one post."""
  if "username" in flask.session:
        logname = flask.session["username"]
  else:
    raise InvalidUsage("Forbidden", status_code=403)

  if not checkPostid(postid):
    raise InvalidUsage("Not Found", status_code=404)

  connection = insta485.model.get_db()

  cur = connection.execute("""
    SELECT * FROM posts
    WHERE postid = ?
  """, [postid]
  )
  post_obj = cur.fetchall()

  cur = connection.execute("""
    SELECT filename FROM users
    WHERE username = ?
  """, [post_obj[0]["owner"]]
  )
  owner_img_url = cur.fetchall()[0]["filename"]

  context = {
    "age": post_obj[0]["created"],
    "img_url": "/uploads/" + post_obj[0]["filename"],  # TODO: url_for?
    "owner": post_obj[0]["owner"],
    "owner_img_url": "/uploads/" + owner_img_url,
    "owner_show_url": "/u/" + post_obj[0]["owner"] + "/",
    "post_show_url": "/p/" + str(postid) + "/",
    "url": flask.request.path
  }

  return flask.jsonify(**context)


def checkPostid(postid):
  connection = insta485.model.get_db()

  cur = connection.execute("""
    SELECT postid FROM posts
    WHERE postid = ?
  """, [postid]
  )
  post = cur.fetchall()

  return len(post) > 0
