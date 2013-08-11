module.exports = function(config) {
    config.set({

        basePath: '',
        files: [
            ANGULAR_SCENARIO,
            ANGULAR_SCENARIO_ADAPTER,
            '../test/*.js'
        ],
        autoWatch: true,
        browsers: ['Chrome'],
        singleRun: true,
        proxies: {
            '/': 'http://localhost:8000/'
        },
        urlRoot: '/__karma__/',

        plugins: [
            'karma-chrome-launcher',]
    });
};