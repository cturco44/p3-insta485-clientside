import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';
import PostParent from './post_parent';

class PostList extends React.Component {
  constructor(props) {
    super(props);
    this.state = { posts: [], nextPage: '', hasMore: false }; // TODO: hasMore default?
    this.fetchData = this.fetchData.bind(this);

    if(performance){
      if(performance.getEntriesByType("navigation")[0].type == "back_forward"){
        this.setState({posts: history.state.posts,
                       next_page: history.state.next_page,
                       has_more: history.state.has_more});
      }
    }
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
          posts: data.results,
          nextPage: data.next,
        });
        history.replaceState(this.state, null, '');
      })
      .catch((error) => console.log(error));
  }

  fetchData() {
    const { nextPage } = this.state;
    fetch(nextPage, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          posts: prevState.posts.concat(data.results),
          nextPage: data.next,
          hasMore: (data.next !== ''),
        }));
        history.replaceState(this.state, null, '');
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { posts, hasMore } = this.state;

    //const postItems = posts.map((post) => <li style={{ listStyle: 'none' }} key={post.postid}><Post url={post.url} /></li>);
    const postItems = posts.map((post) => 
      <li style={{ listStyle: 'none' }} key={post.postid}>
        <PostParent postUrl={post.url} likesUrl={post.url + "likes/"} />
      </li>
    );

    return (
      <InfiniteScroll
        dataLength={posts.length}
        next={this.fetchData}
        hasMore={hasMore}
        loader={<h2>Loading...</h2>}
        endMessage={<p>You&#39;ve reached the end.</p>}
      >
        {postItems}
      </InfiniteScroll>
    );
  }
}

PostList.propTypes = {
  url: PropTypes.string.isRequired,
};

export default PostList;
