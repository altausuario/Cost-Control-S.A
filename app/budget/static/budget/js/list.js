function formatCurrency(number) {
    return parseFloat(number).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
 }
var tblBudget;
function getData(){
 tblBudget = $('#data').DataTable({
//        responsive: true,
        scrollX: true,
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
            {
                className: 'details-control',
                orderable: false,
                data: null,
                defaultContent: '',
            },
            {'data': 'position'},
            {'data': 'name'},
            {'data': 'date_joined'},
            {'data': 'total_income'},
            {'data': 'total_expenses'},
            {'data': 'total'},
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
                    var buttons = '<a href="/budget/update/'+row.id+'" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" data-placement="top" title="Editar"><i class="fas fa-edit"></i></a>  ';
                    buttons +=  '<a href="/budget/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" data-placement="top" title="Eliminar"><i class="fas fa-trash-alt"></i></a>';
                    buttons +=  '<a href="/budget/invoice/pdf/'+row.id+'" target="_blank" class="btn btn-success btn-xs btn-flat ml-1" data-toggle="tooltip" data-placement="top" title="PDF"><i class="fa-solid fa-file-pdf"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-2,-3,-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return formatCurrency(data)
                }
            },
        ],
        initComplete: function(settings, json) {

          }
        });
}
function format(d) {
    var html = '';
    if (d.detIncome.length > 0) {
    html += '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr>';
    html += '<th scope="col" colspan="7" class="bg-success">Detalle de ingresos</th>';
    html += '</tr>';
    html += '<tr>';
    html += '<th scope="col">Descripción</th>';
    html += '<th scope="col">Fecha del ingreso</th>';
    html += '<th scope="col">Monto</th>';
    html += '<th scope="col">Iva (%)</th>';
    html += '<th scope="col">Total Iva</th>';
    html += '<th scope="col">Total</th>';
    html += '<th scope="col">Estado</th>';
    html += '</tr>';
    html += '</thead>';
    html += '<tbody>'
    $.each(d.detIncome, function(key, value){
        html += '<tr>'
        html += '<td>'+ value.description +'</td>'
        html += '<td>'+ value.date_joined +'</td>'
        html += '<td>'+ formatCurrency(value.amount) +'</td>'
        html += '<td>'+parseFloat(value.iva).toFixed(0) +'</td>'
        html += '<td>'+ formatCurrency(value.totaliva) +'</td>'
        html += '<td>'+ formatCurrency(value.total) +'</td>'
        html += '<td>'+ value.state +'</td>'
        html += '</tr>'
    })
    html += '</tbody>'
    }
    if (d.detExpenses.length > 0) {
    html += '<table class="table mt-5">';
    html += '<thead class="thead-dark">';
    html += '<tr>';
    html += '<th scope="col" colspan="7" class="bg-danger">Detalle de egresos</th>';
    html += '</tr>';
    html += '<tr>';
    html += '<th scope="col">Descripción</th>';
    html += '<th scope="col">Fecha del gasto</th>';
    html += '<th scope="col">Monto</th>';
    html += '<th scope="col">Iva (%)</th>';
    html += '<th scope="col">Total Iva</th>';
    html += '<th scope="col">Total</th>';
    html += '<th scope="col">Estado</th>';
    html += '</tr>';
    html += '</thead>';
    html += '<tbody>'
    $.each(d.detExpenses, function(key, value){
        html += '<tr>'
        html += '<td>'+ value.description +'</td>'
        html += '<td>'+ value.date_joined +'</td>'
        html += '<td>'+ formatCurrency(value.amount) +'</td>'
        html += '<td>'+ parseFloat(value.iva).toFixed(0) +'</td>'
        html += '<td>'+ formatCurrency(value.totaliva) +'</td>'
        html += '<td>'+ formatCurrency(value.total) +'</td>'
        html += '<td>'+ value.state +'</td>'
        html += '</tr>'
    })
    html += '</tbody>'
    }
    return html;
}
$(function(){
   getData();
    $('#data tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = tblBudget.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
});
