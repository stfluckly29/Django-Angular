'use strict';

angular.module('inAppTranlsationApp')
  .controller('SignupCtrl', function ($scope, user, $location, $rootScope) {
    $scope.pw_input_type = 'password';
    $scope.signup = function() {
      $scope.error_msg = '';
      $rootScope.loading = true;
      user.save(this.user,
        function() {
          $rootScope.loading = false;
          $rootScope.fromRegister = true;
          $location.path('/login');
        }, function (data) {
          $rootScope.loading = false;
          data = data.data;
          var msg = '';
          for (var key in data) {
            msg += data[key][0];
          }
          msg = msg.replace('Username', 'email');
          $scope.error_msg = msg;
        }
      );
    };

    $scope.tick_pw_type = function() {
      if ($scope.pw_input_type == 'password') {
        $scope.pw_input_type = 'text';
      } else {
        $scope.pw_input_type = 'password';
      }
    };
  });
