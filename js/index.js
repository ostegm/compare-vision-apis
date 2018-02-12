`use strict`;

// Object to control namespace issues.
var CVA__ = {};

CVA__.docReady = function () {
  console.log('Im ready!');
};

CVA__.testGoogle = function () {
  const data = {};
  $.post('/google', data, function (response) {
    console.log(response);
  });
};

$(CVA__.docReady);
