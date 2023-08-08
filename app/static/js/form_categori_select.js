$(function () {
    $('select[name="categorie"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_categories'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una categoria',
        minimumInputLength: 1,
    });

    $('.btnAddCategories').on('click', function () {
        $('#myModelAddCategories').modal('show')
    })
    $('#myModelAddCategories').on('hidden.bs.modal', function (e) {
//         $('body').addClass('modal-open');
          if ($('.modal.show').length > 0) {
             $('body').addClass('modal-open');
          }
         $('#frmAddCategories').trigger('reset')
    })
    $('#frmAddCategories').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_categories');
        alert_confirm(window.location.pathname, 'Notificacion', '¿Estas seguro de crear un nuevo registro para Categorias', parameters, function (response) {
            var newOption = new Option(response.name, response.id, false, true)
            $('select[name="categorie"]').append(newOption).trigger('change')
            Swal.fire({
                title: 'Alerta',
                text: 'Registro creado correctamente',
                icon: 'success',
                timer: 3000,
                onClose: () => {
                    $('#myModelAddCategories').modal('hide')
                }
            });
        });
    })
})