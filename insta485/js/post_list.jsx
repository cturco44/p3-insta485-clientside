import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import PostParent from './post_parent';

class PostList extends React.Component {
  constructor(props) {
    super(props);
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'manual';
    }
    if (performance.getEntriesByType('navigation')[0].type === 'back_forward') {
      this.state = {
        posts: window.history.state.posts,
        nextPage: window.history.state.nextPage,
        hasMore: window.history.state.hasMore,
        currUrl: window.history.state.currUrl,
      };
    } else {
      this.state = {
        posts: [], nextPage: '', hasMore: true, currUrl: '',
      };
      window.history.pushState(this.state, '');
    }
    this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    const { currUrl } = this.state;

    if (currUrl === '') {
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
            hasMore: (data.next !== ''),
            currUrl: url,
          });
          window.history.replaceState(this.state, '');
        })
        .catch((error) => console.log(error));
    }
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
          currUrl: nextPage,
        }));
        window.history.replaceState(this.state, '');
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { posts, hasMore } = this.state;

    const postItems = posts.map((post) => (
      <ul key={post.postid}>
        <li style={{ listStyle: 'none' }} key={post.postid}>
          <PostParent postUrl={post.url} likesUrl={`${post.url}likes/`} />
        </li>
      </ul>
    ));

    return (
      <InfiniteScroll
        dataLength={posts.length}
        next={this.fetchData}
        hasMore={hasMore}
        loader={<h2>Loading...</h2>}
        scrollThreshold={0.9}
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
