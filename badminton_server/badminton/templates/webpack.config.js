const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require('path');
module.exports = {
    entry: {
        'index': path.resolve(__dirname, 'src/js/index.tsx'),
        'interested': path.resolve(__dirname, 'src/js/interested.tsx'),
        'election': path.resolve(__dirname, 'src/js/election.tsx'),
        'stats': path.resolve(__dirname, 'src/js/stats.tsx'),
        'css': path.resolve(__dirname, 'src/js/css.tsx'),
    },
    output: {
        path: path.resolve(__dirname, 'dist/'),
        filename: 'js/[name].js'
    },
    devtool: "source-map",
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json", ".scss", ".sass", ".css"]
    },

    module: {
        rules: [

            {
                test: /\.tsx?$/,
                loader: "awesome-typescript-loader"
            },
            {
                enforce: "pre",
                test: /\.js$/,
                loader: "source-map-loader" 
            },
            {
              test: /\.scss$/,
              use: ExtractTextPlugin.extract({
                fallback: 'style-loader',
                use: ['css-loader', 'sass-loader']
              })
            }
        ]
    },

    plugins: [
        new ExtractTextPlugin({ // define where to save the file
            filename: 'css/[name].css',
            allChunks: true,
        }),
        new CopyWebpackPlugin([ { from: 'src/templates', to: 'html' } ], {debug: 'info'}),
    ],

    externals: {
        "react": "React",
        "react-dom": "ReactDOM"
    },
};