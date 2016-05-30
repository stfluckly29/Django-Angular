'use strict';

/**
 * @ngdoc service
 * @name inAppTranlsationApp.config
 * @description
 * # config
 * Factory in the inAppTranlsationApp.
 */
angular.module('inAppTranlsationApp')
  .factory('config', function () {
    var env = (function () {
      var url = window.document.URL;

      if (url.indexOf('//127.0.0.1') !== -1 || url.indexOf('//localhost') !== -1 ) {
        return 'development';
      }

      if (url.indexOf('//ec2-54-65-53-178.ap-northeast-1.compute.amazonaws.com') !== -1) {
        return 'staging';
      }

      if (url.indexOf('inapptranslation.com') !== -1) {
        return 'production';
      }

    })();

    if (!env) {
      throw new Error('failed to detect application env');
    }

    return window.config[env];
  });
