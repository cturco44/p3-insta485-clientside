import React from 'react';
import PropTypes from 'prop-types';
import Likes from './likes';
import moment from 'moment';

class Post extends React.Component {

  constructor(props){
    super(props);
    this.state = { post_obj: {} };
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
          post_obj: data
        });
      })
      .catch((error) => console.log(error));
  }


  render(){
    const { url } = this.props;
    const { post_obj } = this.state;

    let profile_alt = post_obj.owner + " profile pic";
    let post_alt = "post image";
    let likes_url = url + "likes/";
    let comments_url = url + "comments/";

    return(
      <div className="post-page-div">
        <div className="post-page-img-wrapper">
          <img className="post-page-img" src={post_obj.img_url} alt={post_alt}></img>
        </div>
        <div className="post-page-user">
          <a href={post_obj.owner_show_url}><img className="profile-pic" src={post_obj.owner_img_url} alt={profile_alt}></img></a>
          <a href={post_obj.owner_show_url}>{post_obj.owner}</a>
          <a href={post_obj.post_show_url} className="post-page-timestamp">{moment.utc(post_obj.age).fromNow()}</a>
        </div>
        <div className="post-page-comments">
          <Likes url={likes_url}/>
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