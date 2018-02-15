`use strict`;

// Object to control namespace issues.
const CVA__ = {
  clarifaiResults: null,
  googleResults: null,
};

CVA__.watchsubmit = function() {
  CVA__.watchSelector();
  const $form = $('.search-box');
  const $resultsBox = $('.results');
  const $resultsTemplate = $('.results-template').clone();
  $form.submit(e => {
      e.preventDefault();
      $resultsBox.empty();
      $resultsBox.html($resultsTemplate.html());
      const queryText = $('#query-input').val();
      const queryType = $('#query-type').val();
      if (queryType === 'url') {
        CVA__.handleUrlQuery(queryText);
      } else {
        CVA__.handleTextQuery(queryText);
      }
    });
  CVA__.handleTableInteractions();
};

CVA__.watchSelector = function() {
  const pText = {
    text: 'e.g. puppies',
    url: 'e.g. https://samples.clarifai.com/metro-north.jpg'
  };
  const searchText = {
    text: 'Enter a phrase',
    url: 'Enter your image URL'
  };
  $('#query-type').on('change', function() {
      currSelection = $('#query-type option:selected').val();
      $(`label[for='query-url']`).text(searchText[currSelection]);
      $('#query-input').prop('placeholder', pText[currSelection]);

    });
};

CVA__.handleUrlQuery = function(url) {
  //Checks query - if its not a valid URL, alerts urser. Otherwise, classifies
  //the image at the url using various vision apis.
  const urlOk = CVA__.validateURL(url);
  console.log('User input a url, validation check returns:', urlOk);
  if (!urlOk) {
    alert(['It looks like you tried to input a url, but something went wrong.',
           ' If you would like to use a URL, it needs to point to a JPG or',
           ,' PNG file. If you don\'t have a URL, just use a phrase and we',
           ,' will find an image for you!'].join(''));
    return;
  }
  // Good image url input from user, proceed with classifications requests.
  CVA__.classifyImage(url);
};

CVA__.handleTextQuery = function(queryText) {
  // Gets an image url from pixabay and classifies that image.
  const key = '8032843-dc7960ea32e725e1670805c12';
  const requestUrl = `https://pixabay.com/api/?key=${key}&q=${queryText}`;
  CVA__.classifyPixabayImageUrl(requestUrl);
};

CVA__.validateURL = function(url) {
  // Tests for http or https ending in png/jpg/jpeg
  const urlRegex = new RegExp('https?:\/\/.*\.(?:png|jpg|jpeg)');
  const wwwRegex = new RegExp('www\.*');
  return (urlRegex.test(url) || wwwRegex.test(url));
};

CVA__.classifyPixabayImageUrl = function(requestUrl) {
  const encodedUrl = encodeURI(requestUrl);
  responseUrl = $.get(encodedUrl, function(response) {
    CVA__.classifyImage(response.hits[0].webformatURL);
  });
};

CVA__.classifyImage = function(url) {
  const data = {
    imageUrl: url,
  };
  CVA__.clarifaiRequest(data);
  CVA__.googleRequest(data);
  CVA__.showImageAndResults(data.imageUrl);
};

CVA__.showImageAndResults = function(url) {
  $('.results').prop('hidden', false);
  $img = $('.result-image');
  $img.prop('src', url).prop('alt', 'An image input by the user.');
};

CVA__.googleRequest = function(data) {
  $.post('/google', data, function(response) {
    console.log('Sending image for classification to Google Vision.');
    const $container = $('.google');
    CVA__.googleResults = CVA__.parseClassificationResponse(
      response.responses[0].labelAnnotations,
      'description',
      'score',
      $container
    );
    const tableHtml = CVA__.makeTable(CVA__.googleResults, 5);
    $container.append(tableHtml);
  });
};

CVA__.clarifaiRequest = function(data) {
  // Makes request to API, formats response and populates results.
  $.post('/clarifai', data, function(response) {
    console.log('Sending image for classification to clarifai.');
    const $container = $('.clarifai');
    CVA__.clarifaiResults =  CVA__.parseClassificationResponse(
      response.outputs[0].data.concepts,
      'name',
      'value',
      $container
    );
    const tableHtml = CVA__.makeTable(CVA__.clarifaiResults, 5);
    $container.append(tableHtml);
  });
};

CVA__.parseClassificationResponse = function(
  labelObjects, labelFieldName, scoreFieldName, $container) {
  // Parses the responses from vision apis into a common format.
  labelsList = labelObjects.map(function(i) {
    return {
      label: i[labelFieldName],
      score: i[scoreFieldName],
    };
  });
  return labelsList;
};

CVA__.makeTable = function(labelsList, nResults) {
  nResults = Math.min(labelsList.length, nResults);
  $table = $('.scores-table.template').clone();
  $table.removeClass('template');
  $table.prop('hidden', false);
  // Grab the data row from the template. Save it for adding rows.
  $dataRow = $table.find('tbody tr').clone();
  $table.find('tbody tr').remove();
  $tbody = $table.find('tbody');
  for (let i = 0; i < nResults; i++) {
    let $newRow = $dataRow.clone();
    $newRow.find('td').first().html(labelsList[i].label);
    scoreStr = labelsList[i].score.toLocaleString("en", {style: "percent"});
    $newRow.find('td').last().html(scoreStr);
    $tbody.append($newRow);
  };
  return $table.html();
};

CVA__.handleTableInteractions = function() {
  $('.column100').on('mouseover', function() {
      var table1 = $(this).parent().parent().parent();
      var table2 = $(this).parent().parent();
      var verTable = $(table1).data('vertable') + '';
      var column = $(this).data('column') + '';

      $(table2).find('.' + column).addClass('hov-column-' + verTable);
      $(table1).find('.row100.head .' + column).addClass('hov-column-head-' + verTable);
    });

  $('.column100').on('mouseout', function() {
    var table1 = $(this).parent().parent().parent();
    var table2 = $(this).parent().parent();
    var verTable = $(table1).data('vertable') + '';
    var column = $(this).data('column') + '';

    $(table2).find('.' + column).removeClass('hov-column-' + verTable);
    $(table1).find('.row100.head .' + column).removeClass('hov-column-head-' + verTable);
  });
};

$(CVA__.watchsubmit);
