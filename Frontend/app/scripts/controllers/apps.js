'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:AppsCtrl
 * @description
 * # AppsCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('AppsCtrl', function ($scope, App, _) {
    $scope.apps = App.query();
    $scope.appRegShown = false;
    $scope.toggleModal = function() {
      $scope.appRegShown = !$scope.appRegShown;
    };
    $scope.registerApp = function() {
      App.save({'name': this.app_name}, function(data) {
        $scope.apps.push(data);
      });
      $scope.appRegShown = !$scope.appRegShown;
      $scope.app_name = '';
    };
  });
