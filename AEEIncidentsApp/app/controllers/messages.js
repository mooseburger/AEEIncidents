var Messages = function () {
  this.respondsWith = ['html', 'json', 'xml', 'js', 'txt'];

  this.index = function (req, resp, params) {
    var self = this;
    var lastHour = new Date();
    lastHour.setHours(lastHour.getHours() - 1);
      geddy.model.Message.all({valid:'false',sent:'false',createdAt: {gt: lastHour}},function(err, messages) {
      self.respond({params: params, messages: messages});
    });
    
  };

  this.add = function (req, resp, params) {
    this.respond({params: params});
  };

  this.create = function (req, resp, params) {
    paramsTwilio ={
      action: params.action,
      controller: params.controller,
      method: params.method,
      sent: 'false',
      valid:'false',
      twAccountSid: params.AccountSid,
      twBody: params.Body,
      twFrom: params.From,
      twFromCity: params.FromCity,
      twFromCountry: params.FromCountry,
      twFromState: params.FromState,
      twFromZip: params.FromZip,
      twSmsSid: params.SmsSid,
      twTo: params.To,
      twToCity: params.ToCity,
      twToCountry: params.ToCountry,
      twToState: params.ToState,
      twToZip: params.ToZip,
      response: params.response
    }
    var self = this
      , message = geddy.model.Message.create(paramsTwilio);

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
          console.log("saved: "+data);
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
