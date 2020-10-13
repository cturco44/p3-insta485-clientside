import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Likes from './likes';

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = { postObj: {} };
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          postObj: data,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { url } = this.props;
    const { postObj } = this.state;

    const profileAlt = `${postObj.owner} profile pic`;
    const postAlt = 'post image';
    const likesUrl = `${url}likes/`;
    const commentsUrl = `${url}comments/`;

    return (
      <div className="post-page-div">
        <div className="post-page-img-wrapper">
          <img className="post-page-img" src={postObj.img_url} alt={postAlt} />
        </div>
        <div className="post-page-user">
          <a href={postObj.owner_show_url}><img className="profile-pic" src={postObj.owner_img_url} alt={profileAlt} /></a>
          <a href={postObj.owner_show_url}>{postObj.owner}</a>
          <a href={postObj.post_show_url} className="post-page-timestamp">{moment.utc(postObj.age).fromNow()}</a>
        </div>
        <div className="post-page-comments">
          <Likes url={likesUrl} />
          {/* TODO: add Comments element here */}
        </div>
      </div>

    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
