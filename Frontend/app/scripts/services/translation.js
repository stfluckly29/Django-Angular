'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.translation
 * @description
 * # translation
 * Service in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .service('Translation', ['$resource', 'config', function ($resource, config) {
    var url = config.api_url+'/translations/:id';
    return $resource(url, {id:'@id'},
      {
        'update': { method:'PUT' }
      });
  }]);
