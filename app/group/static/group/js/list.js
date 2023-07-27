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
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/update/group/'+data+'" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>  ';
                    buttons +=  '<a href="/delete/group/'+data+'" class="btn btn-danger btn-xs btn-flat ml-1"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-justify',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    data.forEach((element) => {
                         html += '<span class = "badge badge-success">' + element +' </span> ';
                    });
                    return html
                }
            },
        ],
        initComplete: function(settings, json) {
          }
        });
});
