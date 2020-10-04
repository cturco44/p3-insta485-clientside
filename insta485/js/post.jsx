import React from 'react';
import PropTypes from 'prop-types';

class Post extends React.Component {

  constructor(props){
    super(props);
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      // TODO: No state right?
      .catch((error) => console.log(error));
  }


  render(){
    
    return(
      <div className="post">
        <div className="post-page-user">
          
        </div>

      </div>

    );

  }

}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};