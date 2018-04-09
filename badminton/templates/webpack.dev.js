const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require('path');
module.exports = {
    entry: {
        'index': path.resolve(__dirname, 'src/js/index.tsx'),
        'interested': path.resolve(__dirname, 'src/js/interested.tsx'),
        'election': path.resolve(__dirname, 'src/js/election.tsx'),
        'home': path.resolve(__dirname, 'src/js/home.tsx'),
        'profile': path.resolve(__dirname, 'src/js/profile.tsx'),
        'members': path.resolve(__dirname, 'src/js/members.tsx'),
        'mail': path.resolve(__dirname, 'src/js/mail.tsx'),
        'queue': path.resolve(__dirname, 'src/js/queue.tsx'),
        'settings': path.resolve(__dirname, 'src/js/settings.tsx'),
        'ranking': path.resolve(__dirname, 'src/js/ranking.tsx'),
        'tournament': path.resolve(__dirname, 'src/js/tournament.tsx'),
        'css': path.resolve(__dirname, 'src/js/css.tsx'),
    },
    output: {
        path: path.resolve(__dirname, 'dist/'),
        filename: 'js/[name].js'
    },
    stats: "minimal",
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
