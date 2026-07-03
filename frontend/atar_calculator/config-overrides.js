const path = require('path');

module.exports = function override(config, env) {
  // Add source map loader configuration
  config.module.rules.unshift({
    test: /\.js$/,
    enforce: 'pre',
    use: ['source-map-loader'],
  });

  return config;
};

