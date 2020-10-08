"""REST API for newest posts."""
import flask
import insta485

@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_post_list():
  """Return list of posts of users logname is following with size and page."""
  page_size = flask.request.args.get("size", default=10, type=int)
  page_num = flask.request.args.get("page", default=0, type=int)
  connection = insta485.model.get_db()

  if "username" in flask.session:
      logname = flask.session["username"]
  else:
      return redirect(url_for("login"))

  # All users logname follow
  cur = connection.execute("""
    SELECT username2 from following
    WHERE username1 = ?
  """, [logname]
  )

  # Generate SQL query for posts in order
  following = cur.fetchall()
  following.append({"username2": logname})

  query = "Select * FROM posts\nWHERE"
  for i, item in enumerate(following):
    if i == 0:
      query += " owner = " + "'" + item["username2"] + "'"
    else:
      query += " OR owner = " + "'" + item["username2"] + "'"
  query += "\nORDER BY postid DESC"
  cur = connection.execute(query)
  posts = cur.fetchall()


  # making the json data to send
  start_idx = page_size * page_num
  end_idx = start_idx + page_size #EXCLUSIVE

  if end_idx < len(posts):
    next_page = "/api/v1/p/?size=" + str(page_size) + "&page=" + str(page_num + 1)
  else:
    next_page = ""

  context = {
    "next": next_page,
    "results": [],
    "url": flask.request.path  # Should be without page and size parameters btw
  }

  for i in range(start_idx, end_idx):
    if i < len(posts):
      curr_post = posts[i]

      new_post = {
        "postid": curr_post["postid"],
        "url": "/api/v1/p/" + str(curr_post["postid"]) + "/"
      }

      context["results"].append(new_post)

  return flask.jsonify(**context)

