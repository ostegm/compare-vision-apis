`use strict`;

// Object to control namespace issues.
var CVA__ = {};

CVA__.watchsubmit = function () {
  console.log('Im ready!');
  const $form = $('.search-box');
  const $urlInput = $('#image-url');
  $form.submit(e => {
    e.preventDefault();
    const url =  $urlInput.val();
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
  CVA__.clarifaiRequest(data);
  // CVA__.googleRequest(data);
};

CVA__.googleRequest = function (data) {
  $.post('/google', data, function (response) {
    console.log('Sending image for classification to Google Vision.');
    const $container = $('.google-results');
    $container.html(`<pre>${JSON.stringify(response, null, 2)}</pre>`);
    $container.prop('hidden', false);
  });
};

CVA__.clarifaiRequest = function (data) {
  $.post('/clarifai', data, function (response) {
    console.log('Sending image for classification to clarifai.');
    const $container = $('.clarifai-results');
    $container.html(`<pre>${JSON.stringify(response, null, 2)}</pre>`);
    $container.prop('hidden', false);
  });
};

$(CVA__.watchsubmit);
