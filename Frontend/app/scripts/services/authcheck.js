'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.authcheck
 * @description
 * # authcheck
 * Service in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .service('authcheck', ['$q', '$injector', function($q, $injector) {
    var authcheck = {
      responseError: function (rejection) {
        console.log('Failed with', rejection.status, 'status');
        if (rejection.status === 401 || rejection.status === 403) {
          var api = $injector.get('api');
          var $location = $injector.get('$location');
          api.destroy();
          $location.url('/login');
        }
        /*if (rejection.status === 400) {
          var msg = "";
          for (var key in rejection.data.__all__) {
            if (msg !== '') {
              msg += "<br>";
            }
            msg += rejection.data.__all__[key];
          }
          window.alertify.error(msg);
        }*/
        return $q.reject(rejection);
      }
    };
    return authcheck;
  }]);
