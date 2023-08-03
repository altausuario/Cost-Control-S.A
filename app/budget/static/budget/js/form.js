function formatCurrency(number) {
    return parseFloat(number).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
}
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
            incomes_total += parseFloat(dict.total)
        })
        var expenses_total = 0.00;
        $.each(this.items.expenses, function(pos, dict){
            expenses_total += parseFloat(dict.total)
        })
        this.items.total_income =  incomes_total
        this.items.total_expenses =  expenses_total
        this.items.total = this.items.total_income - this.items.total_expenses

        this.items.total_income =  this.items.total_income.toFixed(2)
        this.items.total_expenses = this.items.total_expenses.toFixed(2)
        this.items.total = this.items.total.toFixed(2)
        $('input[name="total_income"]').val(formatCurrency(this.items.total_income));
        $('input[name="total_expenses"]').val(formatCurrency(this.items.total_expenses));
        $('input[name="total"]').val(formatCurrency(this.items.total));
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
            {'data': 'iva'},
            {'data': 'totaliva'},
            {'data': 'total'},
            {'data': 'date_joined'},
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
                targets: [-3, -4, -6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var valor = parseFloat(data).toFixed(2)
                    return formatCurrency(valor)
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(0)
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
            {'data': 'iva'},
            {'data': 'totaliva'},
            {'data': 'total'},
            {'data': 'date_joined'},
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
                targets: [-3, -4, -6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var valor = parseFloat(data).toFixed(2)
                    return formatCurrency(valor)
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(0)
                }
            },
        ],
        initComplete: function(settings, json) {
          }
        });
    }
};
 var opcionesOriginales;
function Get_opt_select(opt){
     $("#state").html('');
    if(opt === 'Ingreso'){
        var opcionesNuevas = [
            { value: '', selected: '', text: '---------' },
            { value: 'Esperando a recibir', text: 'Esperando a recibir' },
            { value: 'Ya ha sido recibido', text: 'Ya ha sido recibido' },
        ];
        $.each(opcionesNuevas, function(i, opcion) {
            $("#state").append($('<option>', {
                value: opcion.value,
                text: opcion.text
            }));
        });
    }
    if(opt === 'Gasto'){
        var opcionesNuevas = [
            { value: '', selected: '', text: '---------' },
            { value: 'Por pagar', text: 'Por pagar' },
            { value: 'Ya ha sido pagado', text: 'Ya ha sido pagado' },
        ];
        $.each(opcionesNuevas, function(i, opcion) {
            $("#state").append($('<option>', {
                value: opcion.value,
                text: opcion.text
            }));
        });
    }
}

$( function() {
$('#ModalRegisterIncomeAndExpenses').on('shown.bs.modal', function () {
    $('#myModelAddCategories').modal('show')
  });
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
          console.log(ui.item)
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
 $('form[id="form_budget"]').on('submit', function(e){
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

$('.buttonModal').on('click', function(){
    $('select[name="categorie"]').next().find('.select2-search__field').focus();
    var opt = $(this).val()
    $("input[name='iva']").val(19)
    Get_opt_select(opt)
    var title = ' Nuevo ' + $(this).val()
    $('#inputTypeSelect').val($(this).val())
    $('#exampleModalLabel').html('<i class="fas fa-plus"></i> ' + title);
    $('#ModalRegisterIncomeAndExpenses').modal('show')
})

$('form[id="form_register"]').on('submit', function(e){
    e.preventDefault();
    var type = $('#inputTypeSelect').val()
    var parameters = new FormData(this);
        parameters.append('action', $('#inputTypeSelect').val());
    alert_confirm(window.location.pathname,'Notificacion', '¿Estas seguro de crear un nuevo registro para ' + type + '?', parameters, function(response){
                if(type == 'Ingreso'){
                      vents.add(response);
                }else{
                    vents.addExpenses(response);
                }
                Swal.fire({
                      title: 'Alerta',
                      text: 'Registro creado correctamente',
                      icon: 'success',
                      timer: 3000,
                      onClose: () => {
                        $('#ModalRegisterIncomeAndExpenses').modal('hide')
                      }
                });
            });
})
$('#ModalRegisterIncomeAndExpenses').on('hidden.bs.modal', function (e){
      $('form[id="form_register"]').trigger('reset');
   });
});