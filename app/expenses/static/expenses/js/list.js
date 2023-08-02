 function formatCurrency(number) {
    return parseFloat(number).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
 }
$(function () {
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
                'action': 'searchdata'
            },
            dataSrc: "",
        },
        columns: [
            { 'data': 'position' },
            { 'data': 'description' },
            { 'data': 'date_joined' },
            { 'data': 'categorie' },
            { 'data': 'state' },
            { 'data': 'amount' },
            { 'data': 'iva' },
            { 'data': 'totaliva' },
            { 'data': 'total' },
            { 'data': 'valor' }
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/expenses/update/' + row.id + '" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>  ';
                    buttons += '<a href="/expenses/delete/' + row.id + '" class="btn btn-danger btn-xs btn-flat ml-1"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(0)
                }
            },
            {
                targets: [-5, -3, -2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
//                    return '$ ' + data
                      return formatCurrency(data)
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});