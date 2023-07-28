function getData(){
$('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        retrieve: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'searchdata'
            },
            dataSrc: "",
        },
        columns: [
            {'data': 'position'},
            {'data': 'full_name'},
            {'data': 'username'},
            {'data': 'date_joined'},
            {'data': 'image'},
            {'data': 'groups'},
            {'data': 'is_active'},
            {'data': 'id'},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/list/usuarios/edit/'+row.id+'" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>  ';
                    buttons +=  '<a href="/list/usuarios/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons +=  '<button type="button" value="'+row.id+'"class="btn btn-secondary btn-xs btn-flat blockUser"><i class="fas fa-ban"></i></button>';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = row.is_active
                    if (estado == false){
                         return '<span class = "badge badge-danger"> Inactivo </span> ';
                    }else{
                        return '<span class = "badge badge-success"> Activo </span> ';
                    }
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups,function (key, value){
                     html += '<span class = "badge badge-success">' + value.name +' </span> ';
                    });
                    return html;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image +'" class="img-fluid mx-auto d block" style="width: 40px; height:40px;">';
                }
            },
        ],
        initComplete: function(settings, json) {

          }
        });
}
function getBlockUser(pk){
    $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'block_user',
                'pk':pk
            },
            dataType: 'json',
        }).done(function(data){
            if(!data.hasOwnProperty('error')){
                Swal.fire({
                  title: 'Alerta',
                  text: data.text,
                  icon: data.icon,
                  timer: 5000,
                  onClose: () => {
                    if (data.url != ''){
                        location.href = data.url
                    }
                  }
                });
                return false;
            }
            mensaje_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown){
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data){
        });
}
$(function(){
   getData();
   $('#data').on('click', '.blockUser' , function(){
        var pk = $(this).val()

        $.confirm({
        theme: 'material',
        title: 'Notificación',
        icon: 'fa fa-info',
        content: '¿Estas segura de bloquear al usuario?',
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
                    getBlockUser(pk)
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
   })
});
