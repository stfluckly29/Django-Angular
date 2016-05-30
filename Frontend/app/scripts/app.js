'use strict';

/**
 * @ngdoc overview
 * @name inAppTranlsationApp
 * @description
 * # inAppTranlsationApp
 *
 * Main module of the application.
 */
var app = angular
  .module('inAppTranlsationApp', [
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngAnimate',
    'webStorageModule',
    'ngModal',
    'underscore',
    'mgcrea.ngStrap.tooltip',
    'mgcrea.ngStrap.popover',
    'angularFileUpload',
    'filereader',
    'mgcrea.ngStrap.alert',
    'lr.upload'

  ])
  .config(function ($routeProvider, $httpProvider) {
    $httpProvider.interceptors.push('authcheck');
    $routeProvider
      .when('/apps/:id/edit', {
        templateUrl: 'views/appedit.html',
        controller: 'AppeditCtrl'
      })
      .when('/apps/:id/view', {
        templateUrl: 'views/appview.html',
        controller: 'AppviewCtrl'
      })
      .when('/apps', {
        templateUrl: 'views/apps.html',
        controller: 'AppsCtrl'
      })
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl'
      })
      .when('/signup', {
        templateUrl: 'views/signup.html',
        controller: 'SignupCtrl'
      })
      .when('/profile', {
        templateUrl: 'views/profile.html',
        controller: 'ProfileCtrl'
      })
      .when('/logout', {
        templateUrl: 'views/logout.html',
        controller: 'LogoutCtrl'
      })
      .when('/stats', {
        templateUrl: 'views/stats.html',
        controller: 'StatsCtrl'
      })
      .otherwise({
        redirectTo: '/apps'
      });
  });

app.run(function($rootScope, $location, api, _, authorization, user, webStorage) {
  api.init();
  $rootScope._ = _;
  $rootScope.$on("$locationChangeStart", function() {
    var load_path = $location.path().replace('/', '');
    $rootScope.current_path = load_path;
    if (!$rootScope.authenticated) {
      if (load_path != "login" && load_path != 'signup') {
        $location.path( "/login" );
      }
    } else {
      if ( load_path == "login" ) {
        $location.path("/");
      }

      if (!$rootScope.isSuper) {
        user.query({}, function(data) {
          var val = data[0].is_superuser ? 'Y' : 'N';
          webStorage.add('isSuper', val);
          $rootScope.isSuper = val;
        });
      }
    }
  });

  $rootScope.showPopup = false;
  $rootScope.popup = {
    name: '',
    email: '',
    message: ''
  };
  $rootScope.togglePopup = function() {
    $rootScope.showPopup = !$rootScope.showPopup;
    console.log($rootScope.showPopup);
  };
  $rootScope.popupSubmit = function() {
    var data = $rootScope.popup;
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    if (data.name && data.email && data.message && re.test(data.email)) {
      $rootScope.popupInvalid = false;
      authorization.sendMessage(data);
      $rootScope.msgSent = true;
    } else {
      $rootScope.popupInvalid = true;
    }
  };

});
