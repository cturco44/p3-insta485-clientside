import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { numLikes } = this.props;
    //const { liked } = this.state;
    // Render number of likes
    return (
      <div className="likes">
        <p>
          {numLikes}
          {' '}
          like
          {numLikes !== 1 ? 's' : ''}
          
        </p>
        
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
