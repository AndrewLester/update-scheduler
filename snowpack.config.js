const production = process.env.FLASK_ENV !== 'development';

module.exports = {
    mount: {
        client: '/'
    },
    buildOptions: {
        sourcemap: !production,
        out: 'app/bundle/build',
        watch: true
    },
    optimize: {
        bundle: production
    },
    packageOptions: {
        rollup: {
            plugins: [
                require('rollup-plugin-postcss')({
                    extract: true,
                    minimize: true,
                    use: [
                        ['sass', {
                            includePaths: [
                                './client/theme',
                                './node_modules'
                            ]
                        }]
                    ]
                }),
                require('rollup-plugin-svelte')({
                    include: ["./node_modules"],
                })
            ]
        },
        polyfillNode: true
    },
    alias: {
        "@api": "./client/api",
        "@attachments": "./client/attachments",
        "@editor": "./client/editor",
        "@layouts": "./client/layouts",
        "@notifications": "./client/notifications",
        "@realms": "./client/realms",
        "@theme": "./client/theme",
        "@updates": "./client/updates",
        "@utility": "./client/utility",
    },
    plugins: [
        '@snowpack/plugin-svelte',
        '@snowpack/plugin-typescript',
        '@snowpack/plugin-dotenv',
        [
            '@snowpack/plugin-sass', 
            {
                compilerOptions: {
                    loadPath: "./node_modules"
                }
            }
        ]
    ]
}
