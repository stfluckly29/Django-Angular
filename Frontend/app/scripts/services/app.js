'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.App
 * @description
 * # App
 * Factory in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .factory('App', ['$resource', 'config', function ($resource, config) {
    var url = config.api_url+'/apps/:id:custom';
    return $resource(url, {id:'@id', custom: '@custom'},
      {
        'update': { method:'PUT' },
        'localwords': {methods: 'GET', is_array: false}
      });
  }]);
