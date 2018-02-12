`use strict`;

// Object to control namespace issues.
var CVA__ = {};

CVA__.watchsubmit = function () {
  console.log('Im ready!');
  const form = $('.search-box');
  const urlInput = $('#image-url');
  form.submit(e => {
    e.preventDefault();
    const url =  urlInput.val();
    const urlOk = CVA__.validateURL(url);
    if (urlOk) {
      CVA__.classifyImage(url);
    }
  });
};

CVA__.validateURL = function (url) {
  console.log('TODO - Validate url', url);
  return true;
};

CVA__.classifyImage = function (url) {
  const data = {
    imageUrl: url,
  };

  $.post('/google', data, function (response) {
    console.log(response);
  });

  $.post('/clarifai', data, function (response) {
    console.log(response);
  });
};

$(CVA__.watchsubmit);
