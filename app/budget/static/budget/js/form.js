var tblBudget;
var tblBudgetexpenses;
var vents = {
    items: {
        name: '',
        total_income: 0.00,
        total_expenses: 0.00,
        total: 0.00,
        incomes: [],
        expenses:[]
    },
    calculate_budget: function(){
        var incomes_total = 0.00;
        $.each(this.items.incomes, function(pos, dict){
            incomes_total += parseFloat(dict.amount)
        })
        var expenses_total = 0.00;
        $.each(this.items.expenses, function(pos, dict){
            expenses_total += parseFloat(dict.amount)
        })
        this.items.total_income =  incomes_total
        this.items.total_expenses =  expenses_total
        this.items.total = this.items.total_income - this.items.total_expenses
        $('input[name="total_income"]').val(this.items.total_income.toFixed(2));
        $('input[name="total_expenses"]').val(this.items.total_expenses.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function(item){
        this.items.incomes.push(item);
        this.list()
    },
    addExpenses: function(item){
        this.items. expenses.push(item);
        this.listExpenses()
    },
    list: function(){
        this.calculate_budget();
        tblBudget =  $('#tblBudget').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        data: this.items.incomes,
        columns: [
            {'data': 'id'},
            {'data': 'description'},
            {'data': 'amount'},
            {'data': 'date_creation'},
            {'data': 'state'},
        ],
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,

        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>  ';
                    return buttons;
                }
            },
            {
                targets: [-3],
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
    },
    listExpenses: function(){
        this.calculate_budget();
        tblBudgetexpenses = $('#tblBudgetexpenses').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        data: this.items.expenses,
        columns: [
            {'data': 'id'},
            {'data': 'description'},
            {'data': 'amount'},
            {'data': 'date_creation'},
            {'data': 'state'},
        ],
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>  ';
                    return buttons;
                }
            },
            {
                targets: [-3],
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
};

$( function() {
$( "#buscar" ).autocomplete({
      source: function(request, response) {
            $.ajax({
                url:window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'autocomplete',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function(data){
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown){
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data){

            });
      },
      delay: 500,
      minLength: 1,
      select: function(event, ui){
          event.preventDefault();
          vents.add(ui.item);
          $(this).val('');
      }
    });

$( "#busqueda" ).autocomplete({
      source: function(request, response) {
            $.ajax({
                url:window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'autocompleteExpenses',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function(data){
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown){
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data){

            });
      },
      delay: 500,
      minLength: 1,
      select: function(event, ui){
          event.preventDefault();
          vents.addExpenses(ui.item);
          $(this).val('');
      }
    });

$('#tblBudget tbody').on('click', 'a[rel="remove"]', function(){
        var tr = tblBudget.cell($(this).closest('td, li')).index();
         alert_action('Notificación', '¿Estas seguro de eliminar el ingreso de tu detalle?', function(){
             vents.items.incomes.splice(tr.row, 1);
             vents.list()
         })
     });

$('#tblBudgetexpenses tbody').on('click', 'a[rel="remove"]', function(){
        var tr = tblBudgetexpenses.cell($(this).closest('td, li')).index();
        alert_action('Notificación', '¿Estas seguro de eliminar el egreso de tu detalle?', function(){
             vents.items.expenses.splice(tr.row, 1);
             vents.listExpenses();
         })
     });

$('#remove_incomes').on('click', function(){
       if(vents.items.incomes.length === 0) return false;
     alert_action('Notificación', '¿Estas seguro de eliminar todos los items del detalle de ingresos?', function(){
        vents.items.incomes = [];
        vents.list();
     })
});

$('#remove_expenses').on('click', function(){
     if(vents.items.expenses.length === 0) return false;
     alert_action('Notificación', '¿Estas seguro de eliminar todos los items del detalle de egresos?', function(){
        vents.items.expenses = [];
        vents.listExpenses();
     })
})

//Event submit
 $('form').on('submit', function(e){
        e.preventDefault();
        if(vents.items.incomes.length === 0 && vents.items.expenses.length === 0){
            mensaje_error('Debe tener almenos un item en su detalle de ingresos o egresos');
            return false;
        }
        vents.items.name =$('input[name="name"]').val();
        var parameters = new FormData(this);
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        var action = $('input[name="action"]').val()
        if (action == 'add'){
            alert_confirm(window.location.pathname,'Notificacion', '¿Estas seguro de crear un nuevo registro?', parameters, function(){
                Swal.fire({
                      title: 'Alerta',
                      text: 'Balance creado correctamente',
                      icon: 'success',
                      timer: 3000,
                      onClose: () => {
                        location.href = '/budget/list/'
                      }
                });
            });
        }
        if(action == 'edit'){
            alert_confirm(window.location.pathname,'Notificacion', '¿Estas seguro de editar el registro', parameters, function(){
                Swal.fire({
                      title: 'Alerta',
                      text: 'Balance actualizado correctamente',
                      icon: 'success',
                      timer: 3000,
                      onClose: () => {
                        location.href = '/budget/list/'
                      }
                });
            });
        }
    });
});