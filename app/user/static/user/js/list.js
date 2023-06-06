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
            headers: {'X-CSRFToken': csrftoken}
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
                    var buttons = '<a href="/list/usuarios/edit/'+row.id+'" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" data-placement="top" title="Editar"><i class="fas fa-edit"></i></a>  ';
                    buttons +=  '<a href="/list/usuarios/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
$(function(){
   getData();
});
