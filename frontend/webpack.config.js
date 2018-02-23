var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    entry: ["./src/index.tsx"],
    output: {
        filename: "bundle.js",
        path: __dirname + "/dist"
    },

    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
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
            filename: '[name].css',
            allChunks: true,
        }),
    ],

    externals: {
        "react": "React",
        "react-dom": "ReactDOM"
    },
};