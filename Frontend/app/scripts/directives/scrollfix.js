'use strict';

/**
 * @ngdoc directive
 * @name inAppTranlsationApp.directive:scrollFix
 * @description
 * # scrollFix
 */
angular.module('inAppTranlsationApp')
  .directive('scrollFix', function () {
    return {
      restrict: 'A',
      link: function ($scope, $element) {
        var $top_link = $('#top-link-wrapper');
        var $dummy_box = $('#dummy-box');
        var $header = $('.row.header');
        $element.bind('scroll', function () {
          var $elements = $($element).find('.fixed, .popover.small.key-modal');
          var left = $element.scrollLeft();
          var top = $element.scrollTop();
          if (left > 0) {
            $dummy_box.addClass('under');
          } else {
            $dummy_box.removeClass('under');
          }
          $header.css('top', top);
          $top_link.css('top', top);
          $elements.css('left', left);
          $top_link.css('left', left);
          $dummy_box.css('left', left);
        });
      }
    };
  });
