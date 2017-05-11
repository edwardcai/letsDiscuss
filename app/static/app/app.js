var $root = $('html, body');

function updateScroll(){
  $('#chat-container').animate({scrollTop:$('#chat-container')[0].scrollHeight} ,700); 
}

$("#query-form").on("submit", function(){
  updateScroll();
  query = $("#query-text").val()
  $("#chatBody").replaceWith("<div class='inline-block'> <div class='panel-body sent-msg'> " + query + "</div></div>" + "<a id=chatBody> </a>");
})


Intercooler.ready( function(elt) { 
  $('[data-toggle="popover"]').popover()
  updateScroll();
  $("#query-text").val("")
});
