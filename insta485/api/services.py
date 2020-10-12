"""REST API for available servicese."""
import flask
import insta485

@insta485.app.route('/api/v1/', methods=["GET"])
def get_servics():
  """Return a list of services available."""

  context = {
    "posts": "/api/v1/p/",
    "url": "/api/v1/"
  }

  return flask.jsonify(**context)