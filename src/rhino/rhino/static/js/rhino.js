
angular.module('rhino', ['rhino.filters', 'rhino.services', 'rhino.directives', 'restful-api']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider
      .when('/home', {templateUrl: '/static/partials/home.html', controller: 'HomeCtrl'})
      .when('/search', {templateUrl: '/static/partials/search.html', controller: 'SearchCtrl'})
      .when('/:shop/search', {templateUrl: '/static/partials/search.html', controller: 'SearchCtrl'})
      .otherwise({redirectTo: '/home'});
  }]).
  config(['$locationProvider', function($locationProvider){
    $locationProvider.html5Mode(true);
  }]);
