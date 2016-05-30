'use strict';

describe('Service: authcheck', function () {

  // load the service's module
  beforeEach(module('inAppApp'));

  // instantiate service
  var authcheck;
  beforeEach(inject(function (_authcheck_) {
    authcheck = _authcheck_;
  }));

  it('should do something', function () {
    expect(!!authcheck).toBe(true);
  });

});
