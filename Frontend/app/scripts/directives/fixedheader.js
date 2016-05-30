'use strict';

/**
 * @ngdoc directive
 * @name inAppTranlsationApp.directive:fixedHeader
 * @description
 * # fixedHeader
 */
angular.module('inAppTranlsationApp')
  .directive('fixedHeader', ['$timeout', function ($timeout) {
    return {
      link: function ($scope, element, attrs) {
        $scope.$on('dataloaded', function () {
          var $rootDiv = $('.language_table');
          var _created = false;
          $scope.$watch('windowHeight', function() {
            if (_created) {
              element.fixedHeaderTable({height: $scope.windowHeight-260});
            }
          });
          $scope.$watch('windowWidth', function() {
            if (_created) {
              element.fixedHeaderTable('destroy');
              element.fixedHeaderTable({fixedColumn: true});
            }
          });
          $scope.$watch('avail_langs', function() {
            if (_created) {
              $timeout(function() {
                element.fixedHeaderTable('destroy');
                element.fixedHeaderTable({fixedColumn: true});
              });
            }
          });
          $timeout(function () { // You might need this timeout to be sure its run after DOM render.
            element.fixedHeaderTable({fixedColumn: true });
            _created = true;

            /*$rootDiv.on('scroll', '.fht-tbody', function() {
              console.log('aaa');
              var left = $(this).scrollLeft();
              if (left > 0) {
                $rootDiv.addClass('under');
              } else {
                $rootDiv.removeClass('under');
              }
            });*/
          }, 0, false);
        });


      }
    };
  }]);
