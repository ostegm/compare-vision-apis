`use strict`

// Object to control namespace issues.
var CVA__ = {}

CVA__.docReady = function() {
  console.log('Im ready!');
};

CVA__.testClarifai = function() {
  const data = {
    'image_url': 'https://samples.clarifai.com/metro-north.jpg',
    'image_category': 'dogs'
  }
  $.post('/clarifai', data, function(response) {
    console.log(response)
  })
}


$(CVA__.docReady)