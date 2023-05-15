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
            dataSrc: ""
        },
        columns: [
            {'data': 'position'},
            {'data': 'nombre'},
            {'data': 'fecha'},
            {'data': 'total_ingreso'},
            {'data': 'total_egreso'},
            {'data': 'total_presupuesto'},
            {'data': 'valor'}
        ],

        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [1],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Editar"><a href="/meses/edit/'+row.id+'" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a></span>  ';
                    buttons +=  '<span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Eliminar"><a href="/meses/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat ml-1"><i class="fas fa-trash-alt"></i></a></span> ';
                    buttons +=  '<span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Editar"><a href="/meses/facture/'+row.id+'" class="btn btn-info btn-xs btn-flat ml-2"><i class="far fa-calendar-check"></i></a></span> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {

          }
        });
}

function getSave(){
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {'action': 'get_calcular_agregar'},
        dataType: 'json',
    }).done(function (data) {
        if(!data.hasOwnProperty('error')) {

        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown){
        aler(textStatus +': ' + errorThrown);
    }).always(function (data){

    });
}

$(function(){
   getSave()
   getData();
});

