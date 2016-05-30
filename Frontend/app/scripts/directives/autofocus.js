app.directive('autofocus', ['$timeout', function($timeout) {
  return {
    restrict: 'A',
    link : function($scope, $element) {
      $timeout(function() {
        //alert('focus');
        $element[0].focus();
      }, 50);
    }
  }
}]);


