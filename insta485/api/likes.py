"""REST API for likes."""
import flask
from flask import jsonify, url_for, request
import insta485
from insta485.api.comments import InvalidUsage, handle_invalid_usage
from insta485.api.post import checkPostid
from insta485.views.index import num_likes, logname_liked
from insta485.views.post import like_post, unlike_post
import pdb


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=['GET', 'POST', 'DELETE'])
def get_likes(postid_url_slug):
  """Return likes on postid"""
  if "username" in flask.session:
        logname = flask.session["username"]
  else:
    raise InvalidUsage("Forbidden", status_code=403)

  if not checkPostid(postid_url_slug) and request.method != "DELETE":
    raise InvalidUsage("Not Found", status_code=404)
  pdb.set_trace()
  if request.method == "POST":
    if logname_liked(postid_url_slug, logname):
      context = {
        "logname": logname,
        "message": "Conflict",
        "postid": postid_url_slug,
        "status_code": 409
      }
      return jsonify(**context), 409
    context = {
      "logname": logname,
      "postid": postid_url_slug
    }
    like_post(logname, postid_url_slug)
    return jsonify(**context)

  
  if request.method == "DELETE":
    if checkPostid(postid_url_slug):
      unlike_post(logname, postid_url_slug)
    return '', 204
  
  context = {
    "logname_likes_this": int(logname_liked(postid_url_slug, logname)),
    "likes_count": num_likes(postid_url_slug),
    "postid": postid_url_slug,
    "url": flask.request.path
  }
  return jsonify(**context)

