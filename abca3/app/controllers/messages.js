var Messages = function () {
  this.respondsWith = ['html', 'json', 'xml', 'js', 'txt'];

  this.index = function (req, resp, params) {
    var self = this;
    console.log(params);
    geddy.model.Message.all(function(err, messages) {
      self.respond({params: params, messages: messages});
    });
  };

  this.add = function (req, resp, params) {
    this.respond({params: params});
  };

  this.create = function (req, resp, params) {
    var self = this
      , message = geddy.model.Message.create(params);

    if (!message.isValid()) {
      params.errors = message.errors;
      self.transfer('add');
    }

    message.save(function(err, data) {
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

    geddy.model.Message.first(params.id, function(err, message) {
      if (!message) {
        var err = new Error();
        err.statusCode = 404;
        self.error(err);
      } else {
        self.respond({params: params, message: message.toObj()});
      }
    });
  };

  this.edit = function (req, resp, params) {
    var self = this;

    geddy.model.Message.first(params.id, function(err, message) {
      if (!message) {
        var err = new Error();
        err.statusCode = 400;
        self.error(err);
      } else {
        self.respond({params: params, message: message});
      }
    });
  };

  this.update = function (req, resp, params) {
    var self = this;

    geddy.model.Message.first(params.id, function(err, message) {
      message.updateProperties(params);
      if (!message.isValid()) {
        params.errors = message.errors;
        self.transfer('edit');
      }

      message.save(function(err, data) {
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

    geddy.model.Message.remove(params.id, function(err) {
      if (err) {
        params.errors = err;
        self.transfer('edit');
      } else {
        self.redirect({controller: self.name});
      }
    });
  };

};

exports.Messages = Messages;
