'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:LogoutCtrl
 * @description
 * # LogoutCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('LogoutCtrl', function ($location, authorization) {
    console.log('LogoutCtrl');
    authorization.logout();
    $location.path('/login');
  });
