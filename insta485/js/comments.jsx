import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      typedContent: '',
      commentList: [],
    };
    this.handlePress = this.handlePress.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    this.fetchRequest();
  }

  fetchRequest() {
    const { url } = this.props;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          commentList: data.comments,
        });
      })
      .catch((error) => console.log(error));
  }

  handlePress(event) {
    const { url } = this.props;
    if (event.key === 'Enter') {
      const { typedContent } = this.state;
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: typedContent }),
      };
      console.log(`url: ${url}\n`);
      console.log(`${typedContent}\n`);
      console.log(JSON.stringify({ text: typedContent }));
      fetch(url, requestOptions)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .then(() => {
          this.fetchRequest();
        })
        .catch((error) => console.log(error));

      this.setState({
        typedContent: '',
      });
    }
  }

  handleChange(event) {
    this.setState({ typedContent: event.target.value });
  }

  render() {
    const { commentList } = this.state;
    const { typedContent } = this.state;
    const parent = [];
    commentList.forEach((comment) => {
      parent.push(
        <p>
          <a href={comment.owner_show_url}><strong>{comment.owner}</strong></a>
          {comment.text}
        </p>,
      );
    });
    parent.push(
      <form className="comment-form" onSubmit={(e) => e.preventDefault()}>
        <input type="text" value={typedContent} onChange={this.handleChange} onKeyPress={this.handlePress} />
        <input type="submit" value="Submit" style={{ display: 'none' }} />
      </form>,
    );

    return (parent);
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
