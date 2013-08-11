
angular.module('rhino.directives', []).
  directive('rhinoMap', ['', function() {
    return function(scope, elm, attrs) {
      elm.css('border', '1px solid red');
    };
  }]);
