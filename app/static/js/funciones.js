function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
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
function mesaje_success(obj){
    var html = '';
    html += '<h5>'
    html += 'Se ha enviado un mensaje al correo eletronico</br>'
    html += '<b class="text-primary">'+obj+'</b></br>'
    html += 'con los pasos a seguir para que pueda resetear su contraseña'
    html += '</h5>'
    Swal.fire({
      title: 'Notificación',
      icon: 'success',
      html: html,
      timer: 7000,
      onClose: () => {
        location.href = '/'
      }
    });
}
function mesaje_success_activate(obj){
    var html = '';
    html += '<h5>'
    html += 'Se ha enviado un mensaje al correo eletronico</br>'
    html += '<b class="text-primary">'+obj+'</b></br>'
    html += 'con los pasos a seguir para habilitar al usuario'
    html += '</h5>'
    Swal.fire({
      title: 'Notificación',
      icon: 'success',
      html: html,
      timer: 7000,
      onClose: () => {
        location.href = '/user/inative/list/'
      }
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
                        headers: {'X-CSRFToken': csrftoken}
                    }).done(function(data){
                        if(!data.hasOwnProperty('error')){
                            callback(data);
                            console.log(data.success)
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
function alert_confirm_ResetPassword(url, title, content, parameters, callback){
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
                        headers: {'X-CSRFToken': csrftoken}
                    }).done(function(data){
                        if(!data.hasOwnProperty('error')){
                            callback(data);
                            mesaje_success(data.success)
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
function alert_activate_user(url, title, content, parameters, callback){
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
                        headers: {'X-CSRFToken': csrftoken}
                    }).done(function(data){
                        if(!data.hasOwnProperty('error')){
                            callback(data);
                            mesaje_success_activate(data.success)
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
function alert_action(title, content, callback){
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
                    callback();
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






