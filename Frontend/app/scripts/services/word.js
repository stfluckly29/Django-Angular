'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.word
 * @description
 * # word
 * Service in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .service('Word', ['$resource', 'config', function ($resource, config) {
    var url = config.api_url+'/words/:id';
    return $resource(url, {id:'@id'},
      {
      });
  }]);
