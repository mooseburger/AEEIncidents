var Tickets = function () {
  this.respondsWith = ['html', 'json', 'xml', 'js', 'txt'];

  this.index = function (req, resp, params) {
    var self = this;

    geddy.model.Ticket.all(function(err, tickets) {
      self.respond({params: params, tickets: tickets});
    });
  };

  this.add = function (req, resp, params) {
    this.respond({params: params});
  };

  this.create = function (req, resp, params) {
    var self = this
      , ticket = geddy.model.Ticket.create(params);

    if (!ticket.isValid()) {
      params.errors = ticket.errors;
      self.transfer('add');
    }

    ticket.save(function(err, data) {
      if (err) {
        params.errors = err;
        self.transfer('add');
      } else {
        self.redirect({controller: self.name});
      }
    });
  };

  this.show = function (req, resp, params) {
    var self = this;

    geddy.model.Ticket.first(params.id, function(err, ticket) {
      if (!ticket) {
        var err = new Error();
        err.statusCode = 404;
        self.error(err);
      } else {
        self.respond({params: params, ticket: ticket.toObj()});
      }
    });
  };

  this.edit = function (req, resp, params) {
    var self = this;

    geddy.model.Ticket.first(params.id, function(err, ticket) {
      if (!ticket) {
        var err = new Error();
        err.statusCode = 400;
        self.error(err);
      } else {
        self.respond({params: params, ticket: ticket});
      }
    });
  };

  this.update = function (req, resp, params) {
    var self = this;

    geddy.model.Ticket.first(params.id, function(err, ticket) {
      ticket.updateProperties(params);
      if (!ticket.isValid()) {
        params.errors = ticket.errors;
        self.transfer('edit');
      }

      ticket.save(function(err, data) {
        if (err) {
          params.errors = err;
          self.transfer('edit');
        } else {
          self.redirect({controller: self.name});
        }
      });
    });
  };

  this.destroy = function (req, resp, params) {
    var self = this;

    geddy.model.Ticket.remove(params.id, function(err) {
      if (err) {
        params.errors = err;
        self.transfer('edit');
      } else {
        self.redirect({controller: self.name});
      }
    });
  };

};

exports.Tickets = Tickets;
