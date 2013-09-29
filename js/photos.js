FLICKR_URL = 'http://api.flickr.com/services/rest/?extras=url_s&method=flickr.photosets.getPhotos&per_page=500&api_key=ef9a4aa6f9d0d5788be60cfb88678bb5&photoset_id=72157622693041967&format=json'

var reblawFillPhotos = function (elem) {
  $.ajax({
    url: FLICKR_URL,
    dataType: 'jsonp',
    success: function(obj) {
      reblawFillPhotosCallback_(elem, obj)
    },
    jsonp: 'jsoncallback'
  });
}

var reblawFillPhotosCallback_ = function(elem, obj) {
  var photoArr = obj.photoset.photo;
  
  var randomPhotos = []
  for (var i = 0; i < 10; i++ ) {
    var randomIndex = Math.floor(photoArr.length * Math.random());
    var photo = photoArr.splice(randomIndex, 1);
    randomPhotos.push(photo[0]);
  }

  $.each(randomPhotos, function(index, value) {
    var a = document.createElement('a');
    var img = document.createElement('img');

    var url = 'http://flickr.com/photo.gne?id=' + value.id;
    a.href = url;

    img.src = value.url_s;
    img.height = 100;
    
    a.appendChild(img);
    elem.appendChild(a);
  });
}

