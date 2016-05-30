angular.module('inAppTranlsationApp')
  .controller('StatsCtrl', function ($scope, user) {
    user.query({id: 'stats'}, function(data) {
      $scope.stats = data[0];
    });
  });
