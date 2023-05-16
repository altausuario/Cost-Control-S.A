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
            headers: {'X-CSRFToken': csrftoken}
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
            {'data': 'date_creation'},
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
                    buttons +=  '<a href="/budget/delete/'+row.id+'" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-2,-3,-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$ ' + data
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
    html += '<th scope="col" colspan="4" class="bg-success">Detalle de ingresos</th>';
    html += '</tr>';
    html += '<tr>';
    html += '<th scope="col">Descripción</th>';
    html += '<th scope="col">Fecha del ingreso</th>';
    html += '<th scope="col">Monto</th>';
    html += '<th scope="col">Estado</th>';
    html += '</tr>';
    html += '</thead>';
    html += '<tbody>'
    $.each(d.detIncome, function(key, value){
        html += '<tr>'
        html += '<td>'+ value.description +'</td>'
        html += '<td>'+ value.date_creation +'</td>'
        html += '<td>$ '+ value.amount +'</td>'
        html += '<td>'+ value.state +'</td>'
        html += '</tr>'
    })
    html += '</tbody>'
    }
    if (d.detExpenses.length > 0) {
    html += '<table class="table mt-5">';
    html += '<thead class="thead-dark">';
    html += '<tr>';
    html += '<th scope="col" colspan="4" class="bg-danger">Detalle de egresos</th>';
    html += '</tr>';
    html += '<tr>';
    html += '<th scope="col">Descripción</th>';
    html += '<th scope="col">Fecha del gasto</th>';
    html += '<th scope="col">Monto</th>';
    html += '<th scope="col">Estado</th>';
    html += '</tr>';
    html += '</thead>';
    html += '<tbody>'
    $.each(d.detExpenses, function(key, value){
        html += '<tr>'
        html += '<td>'+ value.description +'</td>'
        html += '<td>'+ value.date_creation +'</td>'
        html += '<td>$ '+ value.amount +'</td>'
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
