import React from 'react';
import PropTypes from 'prop-types';
import Likes from './likes';
import Post from './post';

class PostParent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { numLikes: 0, liked: false };
    this.likePost = this.likePost.bind(this);
    this.doubleClickLike = this.doubleClickLike.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { likesUrl } = this.props;

    // Call REST API to get number of likes
    fetch(likesUrl, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          numLikes: data.likes_count,
          liked: Boolean(Number(data.logname_likes_this)),
        });
      })
      .catch((error) => console.log(error));
  }

  likePost() {
    const { liked } = this.state;
    const { likesUrl } = this.props;

    let requestType;
    if (liked === true) {
      requestType = 'DELETE';
      this.setState((state) => ({
        numLikes: state.numLikes - 1,
      }));
    } else {
      requestType = 'POST';
      this.setState((state) => ({
        numLikes: state.numLikes + 1,
      }));
    }
    const requestOptions = {
      method: requestType,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    };
    fetch(likesUrl, requestOptions)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .catch((error) => console.log(error));
    this.setState((state) => ({
      liked: !state.liked,
    }));
  }

  doubleClickLike() {
    const { liked } = this.state;
    const { likesUrl } = this.props;

    if (liked !== true) {
      let requestType = 'POST';
      this.setState((state) => ({
        numLikes: state.numLikes + 1,
        liked: true,
      }));

      const requestOptions = {
        method: requestType,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      };
  
      fetch(likesUrl, requestOptions)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .catch((error) => console.log(error));
        this.setState((state) => ({
          liked: true,
        }));
    }
    
  }

  render() {
    const { postUrl } = this.props;
    const { likesUrl } = this.props;

    const { numLikes } = this.state;
    const { liked } = this.state;

    return (
      <div className="post-page-div">
        <Post url={postUrl} handleClick={this.doubleClickLike} />
        <div className="post-page-comments">
          <Likes url={likesUrl} numLikes={numLikes} />
          <button type="button" onClick={this.likePost} className="like-unlike-button">
            {liked ? 'Unlike' : 'Like'}
          </button>
          {/* Comments element goes here */}
        </div>
      </div>
    );
  }
}

PostParent.propTypes = {
  postUrl: PropTypes.string.isRequired,
  likesUrl: PropTypes.string.isRequired,
};

export default PostParent;
