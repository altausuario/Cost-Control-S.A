function get_graph_budget_year_month(){
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
              'action': 'get_graph_budget_year_month'
              },
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            console.log(data)
            graphColumn.addSeries(data)
            return false;
        }
        mensaje_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown){
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data){
    });
}
function get_graph_income_year_month(){
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
              'action': 'get_graph_income_year_month'
              },
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            console.log(data)
            graphColumn.addSeries(data)
            return false;
        }
        mensaje_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown){
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data){

    });
}
function get_graph_expenses_year_month(){
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
              'action': 'get_graph_expenses_year_month'
              },
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            console.log(data)
            graphColumn.addSeries(data)
            return false;
        }
        mensaje_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown){
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data){

    });
}
function get_graph_budget_percentage_year_month(){
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
              'action': 'get_graph_budget_percentage_year_month'
              },
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken}
    }).done(function(data){
        if(!data.hasOwnProperty('error')){
            console.log(data)
            graphPie.addSeries(data)
            return false;
        }
        mensaje_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown){
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data){

    });
}
$(function () {
    get_graph_budget_percentage_year_month()
    get_graph_budget_year_month()
    get_graph_income_year_month()
    get_graph_expenses_year_month()

});