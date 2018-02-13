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
      CVA__.showImage(url);
    }
  });
};

CVA__.showImage = function (url) {
  $('.results').prop('hidden', false);
  $img = $('.result-image');
  $img.prop('src', url).prop('alt', 'An image input by the user.');
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
  CVA__.googleRequest(data);
};

CVA__.googleRequest = function (data) {
  $.post('/google', data, function (response) {
    console.log('Sending image for classification to Google Vision.');
    const $container = $('.google');
    const labelObjects = response.responses[0].labelAnnotations;
    CVA__.parseResponse(labelObjects, 'description', 'score', $container);
  });
};

CVA__.clarifaiRequest = function (data) {
  $.post('/clarifai', data, function (response) {
    console.log('Sending image for classification to clarifai.');
    const $container = $('.clarifai');
    const labelObjects = response.outputs[0].data.concepts;
    CVA__.parseResponse(labelObjects, 'name', 'value', $container);
  });
};

CVA__.parseResponse = function (labelObjects, labelFieldName, scoreFieldName, $container) {
  labelsList = labelObjects.map(function (i) {
    return {
      label: i[labelFieldName],
      score: i[scoreFieldName],
    };
  });

  $container.append(`<pre>${JSON.stringify(labelsList, null, 2)}</pre>`);
};

$(CVA__.watchsubmit);
