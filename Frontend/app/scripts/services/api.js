'use strict';

angular.module('inAppTranlsationApp').factory('api', function ($http, webStorage, $rootScope) {
  return {
    init: function (token) {
      var t = token || webStorage.get('token');
      if (t) {
        t = "Token " + t;
        $http.defaults.headers.common['Authorization'] = t;
        $rootScope.authenticated = true;
        $rootScope.username = webStorage.get('username');
        $rootScope.isSuper = webStorage.get('isSuper');
      }
    },
    destroy: function() {
        delete $http.defaults.headers.common['Authorization'];
        webStorage.clear();
        $rootScope.authenticated = false;
        $rootScope.username = '';
        $rootScope.isSuper = '';
    }
  };
});
