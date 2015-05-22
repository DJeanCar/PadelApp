$(document).ready(function() {

  $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
    var relativeURL = $(e.target).data('location');
    if (relativeURL) {
      $.ajax({
        url : relativeURL,
        type : 'get',
        async : false,
        success : function (data) {
          $($(e.target).attr('href')).html(data);
        }
      });
    }
  });

  //Activate placeholder plugin for browsers not supporting it
  $('input, textarea').placeholder();

  //Activate tooltips
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  });

  //Load content in tab
  $('a[data-toggle="tab"],a[data-toggle="pill"]').on('show.bs.tab', function (e) {
    var targetUrl = $(e.target).attr('href');
    var sectionTab = $($(e.target).data("target"));
    sectionTab.load(targetUrl);
  });

  //Change collapse icon
  $(".collapse[id^='team']").on('show.bs.collapse', function (e) {
    $('[href="#'+this.id+'"]').find("span.arrow").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
  });
  $(".collapse[id^='team']").on('hide.bs.collapse', function (e) {
    $('[href="#'+this.id+'"]').find("span.arrow").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
  });

  //Adjust multiselect size
  $('select[multiple]').on('change', function (e) {
    if (this.options.length > 4)
      this.size = this.options.length;
    else
      this.size = 4;
  });

  //Enable category select before submitting create tournament form
  $('#createTournament').on('submit', function(e){
    e.preventDefault();
    $("#categoryClassification").prop("disabled", false);
    this.submit();
  });

  //Check the game results
  $("#resultForm").submit(function( event ) {
    var errorMessage = "";
    var error = false;
    var game = [];
    for (var i=1; i<=2; i++) {
      game[i-1] = [];
      for (var j=1; j<=3; j++) {
        game[i-1][j-1] = $("#set"+i+"_"+j).val();
        $("#set"+i+"_"+j).tooltip('destroy').removeClass("setError"); //clean any arror message
        if ((j < 3) && (game[i-1][j-1].length == 0)) {
          $("#set"+i+"_"+j).tooltip({ title: 'Indica los juegos en este set' }).addClass("setError");
          error = true;
        }
        else if (((game[i-1][j-1].length > 0)) && (!/^([0-7])$/.test(game[i-1][j-1]))) {
          $("#set"+i+"_"+j).tooltip({ title: 'Los juegos ganados debe ser un número entre 0 y 7' }).addClass("setError");
          error = true;
        }
      }
    }

    if ((game[0][2].length == 0) && (game[1][2].length > 0)) {
      $("#set1_3").tooltip({ title: 'Indica los juegos en este set' }).addClass("setError");
      error = true;
    }
    else if ((game[0][2].length > 0) && (game[1][2].length == 0)) {
      $("#set2_3").tooltip({ title: 'Indica los juegos en este set' }).addClass("setError");
      error = true;
    }

    if (error) {
      errorMessage = "<li>La puntuación no es correcta.</li>";
    }
    else {
      var numSets = 2;
      if (game[0][2].length > 0)
        numSets = 3;

      for (var j=1; j<=numSets; j++) {
        if (!( ((game[0][j-1] == 6) && (game[1][j-1] <= 4)) ||
               ((game[0][j-1] <= 4) && (game[1][j-1] == 6)) ||
               ((game[0][j-1] == 7) && ((game[1][j-1] == 5) || (game[1][j-1] == 6))) ||
               (((game[0][j-1] == 5) || (game[0][j-1] == 6)) && (game[1][j-1] == 7))
           )) {
          error = true;
          errorMessage = errorMessage + "<li>El resultado del set " + j + " no es correcto.</li>";
          $("#set1_"+j).tooltip({ title: 'Corrige el resultado de este set' }).addClass("setError");
          $("#set2_"+j).tooltip({ title: 'Corrige el resultado de este set' }).addClass("setError");
        }
      }

      if (!error) {
        var wonSetsTeam1 = 0;
          var wonSetsTeam2 = 0;
        for (var j=1; j<=numSets; j++) {
          if ( ((game[0][j-1] == 6) && (game[1][j-1] <= 4)) ||
               ((game[0][j-1] == 7) && ((game[1][j-1] == 5) || (game[1][j-1] == 6)))
             ) {
            wonSetsTeam1++;
          }
          else
            wonSetsTeam2++;
        }

        if ((wonSetsTeam1 == 1) && (wonSetsTeam2 == 1)) {
          error = true;
          errorMessage = "<li>El partido no puede acabar en empate a sets.</li>";
          $("#set1_3").tooltip({ title: 'Indica el resultado de este set para deshacer el empate' }).addClass("setError");
          $("#set2_3").tooltip({ title: 'Indica el resultado de este set para deshacer el empate' }).addClass("setError");
        }
        else if ((wonSetsTeam1 == 3) || (wonSetsTeam2 == 3)) {
          error = true;
          errorMessage = "<li>El partido no puede acabar en 3 sets a 0. El máximo son 2-0.</li>";
          $("#set1_3").tooltip({ title: 'Elimina el resultado de este set para que el partido acabe 2-0' }).addClass("setError");
          $("#set2_3").tooltip({ title: 'Elimina el resultado de este set para que el partido acabe 2-0' }).addClass("setError");
        }
      }
    }

    if (errorMessage.length > 0) {
      $("#errorDiv").html("<p>Hay algún problema con la información que nos has enviado. Por favor, revisa estos datos antes de volver a enviarlos:</p><ul>"
                     + errorMessage + "</ul>");
      $("#errorDiv").removeClass("hidden");
      //Move to error div
      $('html, body').animate({
        scrollTop: $("#errorDiv").offset().top
      }, 750);
      event.preventDefault();
      return false;
    }

    return true;
  });

  //Set the game result if not presented - individual players
  $("select[id^='player']").change(function() {
    if (this.value == -1) {
      var team = this.name.substring(this.name.length-3, this.name.length-2);
      var player = this.name.substring(this.name.length-1);

      var mate;
      if (player == 1) mate = 2;
      else if (player == 2) mate = 1;

      //If both values are not presented
      if ($("#player"+team+"_"+mate).val() == -1) {
        var opposingTeam;
        if (team == 1) opposingTeam = 2;
        else if (team == 2) opposingTeam = 1;

        $("#set"+team+"_1").val("0");
        $("#set"+team+"_2").val("0");
        $("#set"+team+"_3").val("");
        $("#set"+opposingTeam+"_1").val("6");
        $("#set"+opposingTeam+"_2").val("6");
        $("#set"+opposingTeam+"_3").val("");
      }
    }
  });

  //Set the game result if not presented - pairs
  $("select[id^='pair']").change(function() {
    if (this.value == -1) {
      var pair = this.name.substring(this.name.length-1);
      var opposingPair;
      if (pair == 1) opposingPair = 2;
      else if (pair == 2) opposingPair = 1;

      $("#set"+pair+"_1").val("0");
      $("#set"+pair+"_2").val("0");
      $("#set"+pair+"_3").val("");
      $("#set"+opposingPair+"_1").val("6");
      $("#set"+opposingPair+"_2").val("6");
      $("#set"+opposingPair+"_3").val("");
    }
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
  * Show tournamentType explain and tournamentType fields
  */
  $("select[name='tournamentType']").change(function() {
    for (i=0; i<this.options.length; i++) {
      if (this.options[i].value == this.value) {
        $("#"+this.options[i].value+"Explain").removeClass("hidden");
        if (!$("#"+this.options[i].value+"Fields").hasClass('in')) {
          $("#"+this.options[i].value+"Fields").collapse('show');
        }
      }
      else {
        $("#"+this.options[i].value+"Explain").addClass("hidden");
        if ($("#"+this.options[i].value+"Fields").hasClass('in')) {
          $("#"+this.options[i].value+"Fields").collapse('hide');
        }
      }
    }
  });

  /**
  * Swap between created and own category classifications
  */
  $("#newCategoryClassificationButton").on("click", function() {
    if ($("#fixedCategoryClassification").hasClass('in')) {
      $("#fixedCategoryClassification").collapse('hide');
      $("#fixedCategoryClassification").html("");
    }
    else {
      $("#fixedCategoryClassification").html(fixedCategoryClassification);
      $("#fixedCategoryClassification").collapse('show');
    }

    if ($("#newCategoryClassification").hasClass('in')) {
      $("#newCategoryClassification").collapse('hide');
      $("#newCategoryClassification").html("");
    }
    else {
      $("#newCategoryClassification").html(newCategoryClassification);
      $("#newCategoryClassification").collapse('show');
    }
  });

  /**
  * Swap between created and own level classifications
  */
  $("#newLevelClassificationButton").on("click", function() {
    if ($("#fixedLevelClassification").hasClass('in')) {
      $("#fixedLevelClassification").collapse('hide');
      $("#fixedLevelClassification").html("");
    }
    else {
      $("#fixedLevelClassification").html(fixedLevelClassification);
      $("#fixedLevelClassification").collapse('show');
    }

    if ($("#newLevelClassification").hasClass('in')) {
      $("#newLevelClassification").collapse('hide');
      $("#newLevelClassification").html("");
    }
    else {
      $("#newLevelClassification").html(newLevelClassification);
      $("#newLevelClassification").collapse('show');
    }
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
                          .replace("addOne("+group+","+index+")", "addOne("+group+","+(index+1)+")")
                          .replace("enableOne("+group+","+index+")", "enableOne("+group+","+(index+1)+")");
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
                           .replace("addOne("+group+","+(index+1)+")", "addOne("+group+","+(index)+")")
                           .replace("enableOne("+group+","+(index+1)+")", "enableOne("+group+","+(index)+")");
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

/**
* Enable the form controls for one team member.
*/
function enableOne(group, index) {
  if (index > 1) {
    $("#memberName_"+group+"_"+index).prop( "disabled", false );
    $("#memberSurname1_"+group+"_"+index).prop( "disabled", false );
    $("#memberSurname2_"+group+"_"+index).prop( "disabled", false );
    $("#memberEmail_"+group+"_"+index).prop( "disabled", false );
  }
};

/**
* Add another member in the form.
*/
function addOneElement(type, index) {
  if (index > 1) {
    var lastElement = $("#"+type+"_"+(index-1));
    var lastElementButton = lastElement.find("#"+type+"Button_"+(index-1));
    var newElement = $("#"+type+"_"+(index-1)).clone();
    var newElementHtml = newElement.html().replace(new RegExp("_"+(index-1), 'g'), "_"+index)
                          .replace("addOneElement('"+type+"',"+index+")", "addOneElement('"+type+"',"+(index+1)+")");
    newElement.attr("id",type+"_"+index);
    newElement.html(newElementHtml);
    newElement.appendTo("#"+type+"Group");
    newElement.find("input").val("");
    lastElementButton.attr("onclick","removeOneElement('"+type+"',"+(index-1)+")");
    lastElementButton.find(".glyphicon").toggleClass("glyphicon-plus").toggleClass("glyphicon-remove").toggleClass("text-success").toggleClass("text-danger");
    lastElementButton.blur();
  }
};

/**
* Remove a member from the form.
*/
function removeOneElement(type, index) {
  if (index > 0) {
    var removed = false;
    var elem;
    while ((elem = $("#"+type+"_"+index)).size() > 0) {
      if (!removed) {
        elem.remove();
        removed = true;
      }
      else {
        var nameValue = $("#"+type+"Name_"+index).val();
        var elemHtml = elem.html().replace(new RegExp("_"+index, 'g'), "_"+(index-1))
                           .replace("removeOneElement('"+type+"',"+index+")", "removeOneElement('"+type+"',"+(index-1)+")")
                           .replace("addOneElement('"+type+"',"+(index+1)+")", "addOneElement('"+type+"',"+(index)+")");
        elem.attr("id",type+"_"+(index-1));
        elem.html(elemHtml);
        $("#"+type+"Name_"+(index-1)).val(nameValue);
      }
      index ++;
    }
  }
};

var categoryRow =
"<tr id=\"row-1\"> \
  <td class=\"text-center cell-center categoryCellWidth\"> \
    <label class=\"sr-only\" for=\"catName-1\">Categoría</label> \
    <input type=\"text\" class=\"form-control\" id=\"catName-1\" name=\"catName-1\" disabled> \
  </td> \
  <td class=\"text-center cell-center\"> \
    <div id=\"div-1Group\"> \
      <div id=\"div-1_1\" class=\"form-group smallMargin\"> \
        <label class=\"sr-only\" for=\"div-1Name_1\">Nombre de la división</label> \
        <div class=\"input-group\"> \
          <input type=\"text\" class=\"form-control\" id=\"div-1Name_1\" name=\"div-1Name_1\" maxlength=\"\" placeholder=\"Nombre de la división\"> \
          <span class=\"input-group-btn\"> \
            <button id=\"div-1Button_1\" class=\"btn btn-default\" type=\"button\" onclick=\"addOneElement('div-1',2);\"> \
              <span class=\"glyphicon glyphicon-plus text-success\"></span> \
            </button> \
          </span> \
        </div> \
      </div> \
    </div> \
  </td> \
</tr>";

var noCategoryRow =
"<tr id=\"row-1\"> \
  <td class=\"text-center cell-center\" colspan=\"2\"> \
    <strong class=\"text-danger\">Para poder crear las divisiones, antes debes seleccionar una clasificación de categorías o generar una propia</strong> \
  </td> \
</tr>";

/**
* Creates the table with the selected categories in order to enable divisions creation.
* In order to avoid problems, disables changes in categories.
*/
function createDivisions() {
  //Control visibility state. It can only be invoked once
  if (!$("#divisions").hasClass('in')) {
    //Show divisions
    $("#divisions").collapse('show');
    //Disable changes in categories
    $("#categoryClassification").prop("disabled", true);
    $("#newCategoryClassificationButton").prop("disabled", true);
    $("#categoryClassificationName").prop("readonly", true);
    $("input[id^='categoryName_']").prop("readonly", true);
    $("button[id^='categoryButton_']").prop("disabled", true);

    var categories = [];
    //The user selects an existing category classification
    if (($("#categoryClassification").length > 0) && ($("#categoryClassification").val().length > 0)) {
      var id_categoryClassification = $('#categoryClassification').val();
      $.ajax({
        data : { 'id' : id_categoryClassification},
        url : '/crear-divisiones-ajax/',
        type : 'get',
        async: false,
        success : function (data) {
          console.log(data);
          categories = data.lista_divisiones;
        }
      });
    }
    //The user creates a new category classification (all category names should not be empty)
    else if (($("#categoryName_1").val()) && ($("#categoryName_1").val().length > 0)) {
      for (var i = 0; i < 20; i++) {
        if (($("#categoryName_"+(i+1)).val()) && ($("#categoryName_"+(i+1)).val().length > 0))
          categories[i] = $("#categoryName_"+(i+1)).val();
        else
          break;
      }
    }

    if (categories.length > 0) {
      for (var i = 0; i < categories.length; i++)
        addCategory(categories[i], (i+1));
    }
    else {
      var newRow = document.createElement("tr");
      newRow.innerHTML = noCategoryRow;
      newRow.id = "row-1";
      document.getElementById("categoriesTableBody").appendChild(newRow);
    }

    //Change button to enable category modification and drop divisions
    $("#createDivisionsButton").attr("onclick","enableCategories()");
    $("#createDivisionsButton").html("Habilitar cambios en las categorías");
  }
};

/**
* Enables changes in categories and drops created divisions.
*/
function enableCategories() {
  //It can only be invoked if divisions are visible
  if ($("#divisions").hasClass('in')) {
    //Hide divisions
    $("#divisions").collapse('hide');
    //Enable changes in categories
    $("#categoryClassification").prop("disabled", false);
    $("#newCategoryClassificationButton").prop("disabled", false);
    $("#categoryClassificationName").prop("readonly", false);
    $("input[id^='categoryName_']").prop("readonly", false);
    $("button[id^='categoryButton_']").prop("disabled", false);
    //Drop divisions
    $("#categoriesTableBody").empty();
    //Change button to create divisions
    $("#createDivisionsButton").attr("onclick","createDivisions()");
    $("#createDivisionsButton").html("Deseo crear ahora las divisiones");
  }
};

/**
* Adds a new category row in the category/divisions table.
*/
function addCategory(categoryName, index) {
  if (index >= 1) {
    var newRowHtml = categoryRow.replace(new RegExp("row-1", 'g'), "row-"+index)
                                .replace(new RegExp("catName-1", 'g'), "catName-"+index)
                                .replace(new RegExp("div-1", 'g'), "div-"+index);
    var newRow = document.createElement("tr");
    newRow.innerHTML = newRowHtml;
    newRow.id = "row-"+index;
    document.getElementById("categoriesTableBody").appendChild(newRow);
    $("#catName-"+index).val(categoryName);
  }
};

/**
* Moves selected options from one select to another.
*/
function moveOptions(from, to) {
  $("#"+from+" :selected").each(function() {
    $('#'+to).append($('#'+from+' option[value="'+$(this).val()+'"]').remove());
    $('#'+to+' option[value="'+$(this).val()+'"]').prop("selected", false);
    $('#'+from).change();
    $('#'+to).change();
  });
};

var fixedCategoryClassification =
"<div class=\"form-group\"> \
  <label for=\"categoryClassification\">Clasificación de categorías <sup><span class=\"glyphicon glyphicon-asterisk text-danger\"></span></sup><span class=\"sr-only\">Obligatorio</span></label> \
  {{ form.categoryClassification }} \
  {{ form.categoryClassification.errors }} \
</div>";

var newCategoryClassification =
"<fieldset id=\"categoryGroup\"> \
  <legend class=\"legendAsLabel\">Clasificación de categorías personalizada <sup><span class=\"glyphicon glyphicon-asterisk text-danger\"></span></sup><span class=\"sr-only\">Obligatorio</span></legend> \
  <div class=\"form-group\"> \
    <label class=\"sr-only\" for=\"categoryClassificationName\">Nombre de la clasificación de categorías</label> \
    <input type=\"text\" class=\"form-control\" id=\"categoryClassificationName\" name=\"categoryClassificationName\" maxlength=\"\" placeholder=\"Nombre de la clasificación\" required> \
  </div> \
  <div id=\"category_1\" class=\"form-group\"> \
    <label class=\"sr-only\" for=\"categoryName_1\">Nombre de la categoría</label> \
    <div class=\"input-group\"> \
      <input type=\"text\" class=\"form-control\" id=\"categoryName_1\" name=\"categoryName_1\" maxlength=\"\" placeholder=\"Nombre\" required> \
      <span class=\"input-group-btn\"> \
        <button id=\"categoryButton_1\" class=\"btn btn-default\" type=\"button\" onclick=\"addOneElement('category',2);\"> \
          <span class=\"glyphicon glyphicon-plus text-success\"></span> \
        </button> \
      </span> \
    </div> \
  </div> \
</fieldset>";

var fixedLevelClassification =
"<div class=\"form-group\"> \
  <label for=\"levelClassification\">Clasificación de niveles</label> \
  {{ form.levelClassification }} \
</div>";

var newLevelClassification =
"<fieldset id=\"levelGroup\"> \
  <legend class=\"legendAsLabel\">Clasificación de niveles personalizada</legend> \
  <div class=\"form-group\"> \
    <label class=\"sr-only\" for=\"levelClassificationName\">Nombre de la clasificación de niveles</label> \
    <input type=\"text\" class=\"form-control\" id=\"levelClassificationName\" name=\"levelClassificationName\" maxlength=\"\" placeholder=\"Nombre de la clasificación\"> \
  </div> \
  <div id=\"level_1\" class=\"form-group\"> \
    <label class=\"sr-only\" for=\"levelName_1\">Nombre del nivel</label> \
    <div class=\"input-group\"> \
      <input type=\"text\" class=\"form-control\" id=\"levelName_1\" name=\"levelName_1\" maxlength=\"\" placeholder=\"Nombre\" required> \
      <span class=\"input-group-btn\"> \
        <button id=\"levelButton_1\" class=\"btn btn-default\" type=\"button\" onclick=\"addOneElement('level',2);\"> \
          <span class=\"glyphicon glyphicon-plus text-success\"></span> \
        </button> \
      </span> \
    </div> \
  </div> \
</fieldset>";
