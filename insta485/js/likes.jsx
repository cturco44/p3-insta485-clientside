import React from 'react';
import PropTypes from 'prop-types';

const Likes = ({ numLikes }) => (
  <div className="likes">
    <p>
      {numLikes}
      {' '}
      like
      {numLikes !== 1 ? 's' : ''}
    </p>
  </div>
);

Likes.propTypes = {
  numLikes: PropTypes.number.isRequired,
};

export default Likes;
