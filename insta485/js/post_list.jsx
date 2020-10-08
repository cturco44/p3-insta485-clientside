import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

class PostList extends React.Component{
  constructor(props){
    super(props);
    this.state = { posts: [] };
  }

  componentDidMount(){
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          posts: data.results
        });
      })
      .catch((error) => console.log(error));
  }

  render(){
    //const { url } = this.props;
    const { posts } = this.state;

    const postItems = posts.map((post) =>
      <li key={post.postid}><Post url={post.url} /></li>
    );

    return(
      <ul>{postItems}</ul>
    );

  }

}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default PostList;