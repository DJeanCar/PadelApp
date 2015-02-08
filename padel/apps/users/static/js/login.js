$(document).ready(function() {

  //Activate placeholder plugin for browsers not supporting it
  $('input, textarea').placeholder();

  /**
  * To emulate accordion behaviour, hide all shown components before showing the new one.
  */
  $("[data-toggle='collapse']").click(function() {
    $("[class~='in']").collapse('hide');
  });

});
