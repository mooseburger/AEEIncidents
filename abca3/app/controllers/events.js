var Events = function () {
  this.respondsWith = ['html', 'json', 'xml', 'js', 'txt'];

  this.index = function (req, resp, params) {
    var self = this;
    var today = new Date();

    today.setHours(today.getHours() - 24);
    
    geddy.model.Event.all({lastUpdate: {gt: today}}, function(err, events) {
      self.respond({params: params, events: events});
    });
  };

  this.add = function (req, resp, params) {
    this.respond({params: params});
  };

  this.create = function (req, resp, params) {
    var self = this
      , event = geddy.model.Event.create(params);

    if (!event.isValid()) {
      params.errors = event.errors;
      self.transfer('add');
    }

    event.save(function(err, data) {
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

    geddy.model.Event.first(params.id, function(err, event) {
      if (!event) {
        var err = new Error();
        err.statusCode = 404;
        self.error(err);
      } else {
        self.respond({params: params, event: event.toObj()});
      }
    });
  };

  this.edit = function (req, resp, params) {
    var self = this;

    geddy.model.Event.first(params.id, function(err, event) {
      if (!event) {
        var err = new Error();
        err.statusCode = 400;
        self.error(err);
      } else {
        self.respond({params: params, event: event});
      }
    });
  };

  this.update = function (req, resp, params) {
    var self = this;

    geddy.model.Event.first(params.id, function(err, event) {
      event.updateProperties(params);
      if (!event.isValid()) {
        params.errors = event.errors;
        self.transfer('edit');
      }

      event.save(function(err, data) {
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

    geddy.model.Event.remove(params.id, function(err) {
      if (err) {
        params.errors = err;
        self.transfer('edit');
      } else {
        self.redirect({controller: self.name});
      }
    });
  };

};

exports.Events = Events;
