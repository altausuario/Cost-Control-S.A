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
                    var estado = row.is_active
                    if (estado == false){
                         return '<span class = "badge badge-danger"> Inactivo </span> ';
                    }else{
                        return '<span class = "badge badge-success"> Activo </span> ';
                    }
                }
            },
            {
                targets: [-2],
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
                targets: [-3],
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
