'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('LoginCtrl', function($scope, $location, webStorage, authorization, api, $rootScope, $http, config) {
    if ($rootScope.fromRegister) {
      $scope.error_msg = 'Please verify your email address to login.';
      delete $rootScope.fromRegister;
    }
    $scope.login = function () {
      $scope.error_msg = '';
      var credentials = {
        username: this.username,
        password: this.password
      };
      console.log(this.remember);
      if (!this.remember) {
        webStorage.order(['session', 'memory', 'local']);
      } else {
        webStorage.order(['local', 'session', 'memory']);
      }
      var success = function (data) {
        console.log(data);
        var token = data.token;
        webStorage.add('token', token);
        webStorage.add('username', $scope.username);
        webStorage.local.add('remember', $scope.remember);
        api.init(token);

        $location.path('/apps');
      };

      var error = function (data) {
        var msg = '';
        for (var key in data) {
          msg += data[key];
        }
        $scope.error_msg = msg;
      };

      authorization.login(credentials).success(success).error(error);
    };

    $scope.forgot_password = function() {
      window.alertify.prompt("Please enter your email address.",
        function(evt, value ){
          var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          if (!re.test(value)) {
            window.alertify.error("Please input valid email address");
          } else {
            var url = config.api_url + '/users/forget_password';
            $rootScope.loading = true;
            $http.post(url, {'email': value})
              .success(function () {
                window.alertify.success("You'll get reset request email shortly.");
                $rootScope.loading = false;
              })
              .error(function (data) {
                $rootScope.loading = false;
                var msg = '';
                for (var key in data) {
                  msg += data[key];
                }
                window.alertify.error(msg);
              });

          }
        });
    };
  });
