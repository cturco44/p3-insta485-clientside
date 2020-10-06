"""REST API for on post."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
def get_post(postid):
  """Return details for one post."""
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
