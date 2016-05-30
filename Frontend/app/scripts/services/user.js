'use strict';
angular.module('inAppTranlsationApp')
  .service('user', ['$resource', 'config', function ($resource, config) {
    var url = config.api_url+'/users/:id';
    return $resource(url, {id:'@id'},
      {
        'update': { method:'PUT' }
      });
  }]);
