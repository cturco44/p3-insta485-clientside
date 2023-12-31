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

      fetch(url, requestOptions)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState((prevState) => ({
            commentList: prevState.commentList.concat(data),
            typedContent: '',
          }));
        })
        .catch((error) => console.log(error));
    }
  }

  handleChange(event) {
    this.setState({ typedContent: event.target.value });
  }

  render() {
    const { commentList } = this.state;
    const { typedContent } = this.state;

    const commentItems = commentList.map((comment) => (
      <p key={comment.commentid}>
        <a
          key={comment.commentid}
          href={comment.owner_show_url}
        >
          <strong>{comment.owner}</strong>
        </a>
        {comment.text}
      </p>
    ));

    const commentForm = (
      <form className="comment-form" onSubmit={(e) => e.preventDefault()}>
        <input type="text" value={typedContent} onChange={this.handleChange} onKeyPress={this.handlePress} />
        <input type="submit" value="Submit" style={{ display: 'none' }} />
      </form>
    );

    return (
      <div>
        {commentItems}
        {commentForm}
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
