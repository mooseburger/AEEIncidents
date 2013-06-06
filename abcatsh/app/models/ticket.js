var Ticket = function () {

  this.defineProperties({
    r1TownOrCity: {type: '1TownOrCity'},
    r2Area: {type: '2Area'},
    r3Status: {type: '3Status'},
    r4LastUpdate: {type: '4LastUpdate'}
  });

  /*
  this.property('login', 'string', {required: true});
  this.property('password', 'string', {required: true});
  this.property('lastName', 'string');
  this.property('firstName', 'string');

  this.validatesPresent('login');
  this.validatesFormat('login', /[a-z]+/, {message: 'Subdivisions!'});
  this.validatesLength('login', {min: 3});
  // Use with the name of the other parameter to compare with
  this.validatesConfirmed('password', 'confirmPassword');
  // Use with any function that returns a Boolean
  this.validatesWithFunction('password', function (s) {
      return s.length > 0;
  });

  // Can define methods for instances like this
  this.someMethod = function () {
    // Do some stuff
  };
  */

};

/*
// Can also define them on the prototype
Ticket.prototype.someOtherMethod = function () {
  // Do some other stuff
};
// Can also define static methods and properties
Ticket.someStaticMethod = function () {
  // Do some other stuff
};
Ticket.someStaticProperty = 'YYZ';
*/

Ticket = geddy.model.register('Ticket', Ticket);

