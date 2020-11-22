// Webpack configuration shared by development and production builds
//
// Webpack Docs:
// https://webpack.js.org/guides/production/

const path = require('path');

module.exports = {
  entry: './insta485/js/main.jsx',
  output: {
    path: path.join(__dirname, '/insta485/static/js/'),
  },
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'],
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
