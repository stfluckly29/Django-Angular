'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:AppeditCtrl
 * @description
 * # AppeditCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('AppeditCtrl', function ($scope, $routeParams, App, $timeout, webStorage,upload, config, $rootScope, $http, $location) {
    $scope.token = webStorage.get('token');
    $scope.show_cert_upload = false;
    $scope.prod_cert = false;
    $scope.dev_cert = false;
    $scope.api_url = config.api_url;
    App.get({id: $routeParams.id}, function(data) {
      $scope.app = data;
      for (var i in data['certs']) {
        if (data.certs[i].cert_type) {
          $scope.prod_cert = data['certs'][i];
        } else {
          $scope.dev_cert = data['certs'][i];
        }
      }
    });
    $scope.save=function(app) {
      $scope.success = false;
      App.update(app, function() {
        $scope.success = true;
        $timeout(function() {$scope.success = false;}, 3000);
      });
    };

    $scope.show_upload=function(cert_type) {
      $scope.cert_pwd = '';
      $scope.cert_type = cert_type;
      $scope.show_cert_upload = true;
    };

    $scope.upload=function(file, cert_pwd) {
      if (!file.length) return;
      var file_name = file[0].name, suffix = '.p12';
      if (file_name.indexOf(suffix, file_name.length - suffix.length) === -1) {
        window.alertify.alert('Please select p12 file.');
        return;
      }

      upload({
        url: config.api_url+'/apps/'+$routeParams.id+'/add_cert',
        method: 'POST',
        data: {
          'cert_file': file[0],
          'cert_type': $scope.cert_type,
          'password': cert_pwd
        }
      }).then(
        function (res) {
          $scope.show_cert_upload = false;
          $rootScope.loading = false;
          var cert = res.data['cert'];
          if (cert.cert_type) {
            $scope.prod_cert = cert;
          } else {
            $scope.dev_cert = cert;
          }
          window.alertify.success("Successfully added a certificate.");
        },
        function (response) {
          console.log(response);
          $scope.show_cert_upload = false;
          $rootScope.loading = false;
          window.alertify.error(response.data['errors']);
        }
      );
      $rootScope.loading = true;
    };

    $scope.delete_cert=function(type) {
      $http.delete(config.api_url+'/apps/'+$routeParams.id+'/remove_'+type+'_cert').then(
        function() {
          $scope[type+'_cert'] = false;
          $rootScope.loading = false;
          window.alertify.success("Successfully removed a certificate.");
        },
        function(res) {
          window.alertify.error(res.data['errors']);
          $rootScope.loading = false;
        }
      );
      $rootScope.loading = true;
    };

    $scope.deleteApp = function(appId) {
      window.alertify.confirm('Do you really want to delete this app?', function(e) {
        if (e) {
          $rootScope.loading = true;
          $http.delete(config.api_url+'/apps/'+appId).then(function() {
            $rootScope.loading = false;
            $location.path('/apps');
          }, function(res) {
            window.alertify.error(res.data['errors']);
            $rootScope.loading = false;
          });
        }
      });
    };
  });
