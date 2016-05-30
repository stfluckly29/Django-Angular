'use strict';

describe('Directive: cloneWords', function () {

  // load the directive's module
  beforeEach(module('inAppTranlsationApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<clone-words></clone-words>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the cloneWords directive');
  }));
});
