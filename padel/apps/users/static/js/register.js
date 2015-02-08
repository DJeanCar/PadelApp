$(document).ready(function() {

  //Activate placeholder plugin for browsers not supporting it
  $('input, textarea').placeholder();

  /**
  * If the user has an account, hide the withoutAccount form and show the withAccount form.
  */
  $("#registerType1").click(function() {
    if ($("#registerType1:checked").length == 1) {
      if ($("#formWithoutAccount").hasClass('in')) {
        $("#formWithoutAccount").collapse('hide');
      }
      if (!$("#formWithAccount").hasClass('in')) {
        $("#formWithAccount").collapse('show');
      }
    }
    $("#registerType1").blur(); //To avoid changing with the arrows keys the radiobutton's value
  });

  /**
  * If the user hasn't an account, hide the withAccount form and show the withoutAccount form.
  */
  $("#registerType2").click(function() {
    if ($("#registerType2:checked").length == 1) {
      if ($("#formWithAccount").hasClass('in')) {
        $("#formWithAccount").collapse('hide');
      }
      if (!$("#formWithoutAccount").hasClass('in')) {
        $("#formWithoutAccount").collapse('show');
      }
    }
    $("#registerType2").blur(); //To avoid changing with the arrows keys the radiobutton's value
  });

  /**
  * Reload division values if category changes
  */
  $("select[name^='category']").change(function() {
    if (divisions.hasOwnProperty(this.value)) {
      var divisionValues = divisions[this.value];
      var divisionSelect = $(this).closest("form").find("select[name^='division']");
      divisionSelect.empty();
      $(divisionValues).each(function() {
        divisionSelect.append($("<option/>").attr('value',this.val).text(this.text));
      });
    }
    else if (this.value == '') {
      $(this).closest("form").find("select[name^='division']").empty();
    }
  });

  /**
  * Check form values
  */
  $('form').submit(function( event ) {
    var gameHourNode = $(this).find("[name^='gameHour']");
    var gameHourValue = gameHourNode.val();
    var rightHour = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(gameHourValue);
    if ((gameHourValue.length > 0) && !rightHour) {
      gameHourNode.focus();
      gameHourNode.tooltip({ title: 'Debes indicar la hora de la forma "hh:mm"' });
      event.preventDefault();
      return false;
    }
    else {
      gameHourNode.tooltip('destroy');
    }

    return true;
  });
});

/**
* Add another team member in the form.
*/
function addOne(group, index) {
  if (index > 1) {
    var lastMember = $("#member_"+group+"_"+(index-1));
    var lastMemberButton = lastMember.find("#memberButton_"+group+"_"+(index-1));
    var newMember = $("#member_"+group+"_"+(index-1)).clone();
    var newMemberHtml = newMember.html().replace(new RegExp("member_"+group+"_"+(index-1), 'g'), "member_"+group+"_"+index)
                          .replace(new RegExp("memberName_"+group+"_"+(index-1), 'g'), "memberName_"+group+"_"+index)
                          .replace(new RegExp("memberSurname1_"+group+"_"+(index-1), 'g'), "memberSurname1_"+group+"_"+index)
                          .replace(new RegExp("memberSurname2_"+group+"_"+(index-1), 'g'), "memberSurname2_"+group+"_"+index)
                          .replace(new RegExp("memberEmail_"+group+"_"+(index-1), 'g'), "memberEmail_"+group+"_"+index)
                          .replace(new RegExp("memberButton_"+group+"_"+(index-1), 'g'), "memberButton_"+group+"_"+index)
                          .replace("addOne("+group+","+index+")", "addOne("+group+","+(index+1)+")");
    newMember.attr("id","member_"+group+"_"+index);
    newMember.html(newMemberHtml);
    newMember.appendTo("#members_"+group);
    $("#memberName_"+group+"_"+index).val("");
    $("#memberSurname1_"+group+"_"+index).val("");
    $("#memberSurname2_"+group+"_"+index).val("");
    $("#memberEmail_"+group+"_"+index).val("");
    lastMemberButton.attr("onclick","removeOne("+group+","+(index-1)+")");
    lastMemberButton.find(".glyphicon").toggleClass("glyphicon-plus").toggleClass("glyphicon-remove").toggleClass("text-success").toggleClass("text-danger");
    lastMemberButton.blur();
  }
};

/**
* Remove a team member from the form.
*/
function removeOne(group, index) {
  if (index > 0) {
    var removed = false;
    var member;
    while ((member = $("#member_"+group+"_"+index)).size() > 0) {
      if (!removed) {
        member.remove();
        removed = true;
      }
      else {
        var nameValue = $("#memberName_"+group+"_"+index).val();
        var surname1Value = $("#memberSurname1_"+group+"_"+index).val();
        var surname2Value = $("#memberSurname2_"+group+"_"+index).val();
        var emailValue = $("#memberEmail_"+group+"_"+index).val();
        var memberHtml = member.html().replace(new RegExp("member_"+group+"_"+index, 'g'), "member_"+group+"_"+(index-1))
                           .replace(new RegExp("memberName_"+group+"_"+index, 'g'), "memberName_"+group+"_"+(index-1))
                           .replace(new RegExp("memberSurname1_"+group+"_"+index, 'g'), "memberSurname1_"+group+"_"+(index-1))
                           .replace(new RegExp("memberSurname2_"+group+"_"+index, 'g'), "memberSurname2_"+group+"_"+(index-1))
                           .replace(new RegExp("memberEmail_"+group+"_"+index, 'g'), "memberEmail_"+group+"_"+(index-1))
                           .replace(new RegExp("memberButton_"+group+"_"+index, 'g'), "memberButton_"+group+"_"+(index-1))
                           .replace("removeOne("+group+","+index+")", "removeOne("+group+","+(index-1)+")")
                           .replace("addOne("+group+","+(index+1)+")", "addOne("+group+","+(index)+")");
        member.attr("id","member_"+group+"_"+(index-1));
        member.html(memberHtml);
        $("#memberName_"+group+"_"+(index-1)).val(nameValue);
        $("#memberSurname1_"+group+"_"+(index-1)).val(surname1Value);
        $("#memberSurname2_"+group+"_"+(index-1)).val(surname2Value);
        $("#memberEmail_"+group+"_"+(index-1)).val(emailValue);
      }
      index ++;
    }
  }
};
