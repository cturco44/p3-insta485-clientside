import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';
import InfiniteScroll from 'react-infinite-scroll-component';

class PostList extends React.Component{
  constructor(props){
    super(props);
    this.state = { posts: [], next_page: "", has_more: true };
    this.fetchData = this.fetchData.bind(this);
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
          posts: data.results,
          next_page: data.next
        });
      })
      .catch((error) => console.log(error));
  }
  
  fetchData(){
    const next_page = this.state.next_page; 
    fetch(next_page, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(prevState => ({
          posts: prevState.posts.concat(data.results),
          next_page: data.next,
          has_more: (data.next !== "") ? true : false
        }));
      })
  };
  

  render(){
    const { posts, has_more, next_page } = this.state;

    const postItems = posts.map((post) =>
      <li style={{listStyle: "none"}} key={post.postid}><Post url={post.url} /></li>
    );

    return(
      <InfiniteScroll
        dataLength={posts.length}
        next={this.fetchData}
        hasMore={has_more}
        loader={<h2>Loading...</h2>}
        endMessage={<p>No more posts.</p>}
      >{postItems}</InfiniteScroll>
    );

  }

}


Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default PostList;