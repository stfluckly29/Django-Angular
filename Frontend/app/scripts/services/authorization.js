'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.authorization
 * @description
 * # authorization
 * Factory in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .factory('authorization', function ($http, config, api) {
  var url = config.api_url;

  return {
    login: function (credentials) {
      return $http.post(url + '/api-token-auth', credentials);
    },
    sendMessage: function(data) {
      return $http.post(url + '/send-message', data);
    },
    logout: function() {
      api.destroy();
    }
  };
});
