const production = process.env.FLASK_ENV !== 'development';

module.exports = {
    mount: {
        client: '/'
    },
    buildOptions: {
        sourceMaps: !production,
        out: 'app/bundle/build'
    },
    scripts: {
        "run:tsc": "tsc --noEmit",
        "run:tsc::watch": "$1 --watch"
    },
    installOptions: {
        rollup: {
            plugins: [
                require('rollup-plugin-scss')()
            ]
        }
    },
    plugins: [
        '@snowpack/plugin-svelte',
        '@snowpack/plugin-typescript',
        '@snowpack/plugin-dotenv',
        '@snowpack/plugin-sass',
        '@snowpack/plugin-babel'
    ]
}
