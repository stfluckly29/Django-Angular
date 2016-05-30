'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:ProfileCtrl
 * @description
 * # ProfileCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('ProfileCtrl', function ($scope, user) {
    user.query({}, function(data) {
      $scope.user = data[0];
    });
    $scope.submitForm = function(isValid) {
      $scope.success = false;
      $scope.error_msg = '';
      if (isValid) {
        if ($scope.user.password != $scope.user.password1) {
          window.alertify.error("Password doesn't match.");
          return;
        }

        $scope.user.$update(function () {
          $scope.success = true;
        }, function (data) {
          var msg = '';
          for (var key in data) {
            msg += data[key];
          }
          $scope.error_msg = msg;
        });

      }
    };
  });
