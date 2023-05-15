function mensaje_error(obj){
    var html = ``;
    if (typeof(obj) === 'object'){
        html = `<ul style = "text-align: left; list-style: none;">`
        $.each(obj, function(key, value){
            html += `<li>${key}: ${value}</li>`
        });
        html += `</ul>`
    }
    else{
        html = `<p>${obj}</p>`
    }
    Swal.fire({
      icon: 'error',
      title: 'Error',
      html: html
    });
}

function alert_confirm(url, title, content, parameters, callback){
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url:url,  //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function(data){
                        if(!data.hasOwnProperty('error')){
                            callback(data);
                            return false;
                        }
                        mensaje_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown){
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data){

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}
