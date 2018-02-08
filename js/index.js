`use strict`

function docReady() {
  console.log('Im ready!');
};

function testClarifai() {
  const data = {
    'image_url': 'https://samples.clarifai.com/metro-north.jpg',
    'image_category': 'dogs'
  }
  $.post('/clarifai', data, function(response) {
    console.log(response)
  })
}


$(docReady)