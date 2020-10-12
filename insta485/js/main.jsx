import React from 'react';
import ReactDOM from 'react-dom';
//import Likes from './likes';
import Post from './post';
import PostList from './post_list';

// This method is only called once
ReactDOM.render(
  <PostList url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);
