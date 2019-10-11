$(function () {

    var tableClasses = [];
    $("table").each(function () {tableClasses.push($(this).attr("class"))});
    tableClasses.pop();
    var howManyDivs = tableClasses[tableClasses.length-1];
    for (var i=0; i<howManyDivs+1; i++) {
        var div = $("<div>");
        var table = $("table." + (i+1));
        table.appendTo(div);
        div.appendTo($(".container"));
        div.addClass('containeritems');
        table.css("width", "250px");
        table.css("margin-left", "25px");
        table.css("margin-right", "25px");
        if (table.attr("class") > 1) {
          var divtab = $("div.containeritems");
          table.css("margin-top", "93px");
          table.css("margin-bottom", "93px");
        }
        if (table.attr("class") > 2) {
          var divtab = $("div.containeritems");
          table.css("margin-top", "248px");
          table.css("margin-bottom", "248px");
        }
        $('td').last().css("background-color", "gold");
        $('td').last().css("text-align", "center");

    }
    var $table = $('table');
    $table.addClass('bordered');
    // $table.last().remove()

    var $tbodys = $("tbody");
    $tbodys.each(function () {
      var points1 = $(this).find(".points").first();
      var points2 = $(this).find(".points").eq(1);
      if (points1.text() > points2.text()) {
        points1.css("background-color", "#ADD8E6")
      } else {
        points2.css("background-color", "#ADD8E6")
      }
  });
  /*

  */
    var name = $('.nice');
    name.on("mouseover", function() {
      var thisClass = $(this).attr('class');
      if (thisClass != ".nice winner") {
        thisClass = thisClass.split(' ').join('.');
        var playerName = $("." + thisClass);
        playerName.addClass('mouseover');
    }
  });
  var name = $('.nice');
  name.on("mouseout", function() {
    var thisClass = $(this).attr('class');
    thisClass = thisClass.split(' ').join('.');
    var playerName = $("." + thisClass);
    if (thisClass!=".points") {
      playerName.toggleClass('mouseover');
    }
  });


//    var $add_team = $("#add_team"),
//        $team_name = $("#team_name");
//
//    $add_team.on("submit", function (event) {
//
//        event.preventDefault();
//        if ($team_name.val().length === 0) {
//            alert("Drużyna musi mieć nazwę.")
//        } else {
//            this.submit()
//        }
//    });


    var $select_button = $('#select-all');
    $select_button.click(function(event) {
        if(this.checked) {
            $(':checkbox').each(function() {
                this.checked = true;
            });
        }
        else {
            $(':checkbox').each(function() {
                this.checked = false;
            });
        }
    });

  });

