const JSMinifyPlugin = require('babel-minify-webpack-plugin');
const cssnano = require('cssnano');
const merge = require('webpack-merge');
const common = require('./webpack.dev.js');
var path = require('path');

const OptimizeCSSAssetsPlugin = require(
  "optimize-css-assets-webpack-plugin"
);

module.exports = merge(common, {
	output: {
	    path: path.resolve(__dirname, 'prod/'),
	    filename: 'js/[name].js'
	},
	plugins: [
	new JSMinifyPlugin(),
	]
});
