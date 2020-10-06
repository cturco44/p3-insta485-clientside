import React from 'react';
import ReactDOM from 'react-dom';
//import Likes from './likes';
import Post from './post';

// This method is only called once
ReactDOM.render(
  // Insert the likes component into the DOM
  // <Likes url="/api/v1/p/1/likes/" />,
  <Post url="/api/v1/p/1/" />, // TODO: this will be replace later
  document.getElementById('reactEntry'),
);
