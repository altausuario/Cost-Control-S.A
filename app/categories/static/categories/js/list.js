$(function(){
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
            {'data': 'name'},
            {'data': 'description'},
            {'data': 'date_creation'},
            {'data': 'valor'}
        ],

        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/categories/update/'+row.id+'" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>  ';
                    buttons +=  '<a href="/categories/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat ml-1"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {

          }
        });
});
