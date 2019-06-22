$(document).ready( function(){
          $('#auto').load('{% url 'hash_rate' %}');
          refresh();
          });

          function refresh()
          {
          	setTimeout( function() {
          	  $('#auto').fadeOut('slow').load('{% url 'hash_rate' %}').fadeIn('slow');
          	  refresh();
          	}, 2000);
          }