module.exports = function(config) {
  config.set({
    frameworks: ['ng-scenario'],
    basePath: '',
    files: [
      '../../test/localtest/*.js'
    ],
    browsers: ['Chrome'],
    singleRun: true,
    proxies: {
      '/': 'http://localhost:8000/'
    },
    urlRoot: '/__karma__/',
  });
};
