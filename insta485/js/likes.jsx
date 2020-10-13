import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    //this.state = { numLikes: 0, liked: false };

    //this.handleClick = this.handleClick.bind(this);
  }

  /*
  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get number of likes
    fetch(url, { credentials: 'same-origin' })
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
  */
  /*
  handleClick() {
    const { liked } = this.state;
    const { url } = this.props;
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
    fetch(url, requestOptions)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .catch((error) => console.log(error));
    this.setState((state) => ({
      liked: !state.liked,
    }));
  }
  */



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
