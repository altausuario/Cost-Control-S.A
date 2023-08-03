function getselect(){
    $('.ms').change(function() {
            console.log($(this).val());
        }).multipleSelect({
            placeholder: 'Seleccione los permisos',
            openOnHover: true,
            filter: true,
            filterPlaceholder: 'Buscar...',
            locale: 'es-ES'
        });
}
$(function(){
    getselect();
    $('#btnAddGroup').on('click', function (){
      $('#formAddGroup').modal('show');
   });
   $('#formAddGroup').on('hidden.bs.modal', function (e){
      $('form[id="newGroup"]').trigger('reset');
   });
   $('form[id="newGroup"]').on('submit', function(e){
        e.preventDefault();
        var parameters = new FormData(this);
         parameters.append('action', 'new_group');
        alert_confirm(window.location.pathname,'Notificacion', '¿Estas seguro de crear un nuevo grupo?', parameters, function(response){
            var newOption = new Option(response.group_name, response.group_id, false, true)
            $('select[name="groups"]').append(newOption).trigger('change')

             var $lista = $(".ms-parent ul");

             var nuevoElemento = '<li class="">' +
                          '<label class="">' +
                            '<input type="checkbox" value="'+ response.group_id +'" data-key="option_'+ response.group_id +'" data-name="selectItemgroups">' +
                            '<span>'+ response.group_name +'</span>' +
                          '</label>' +
                        '</li>';
             $lista.append(nuevoElemento);
             $('li input[value="'+ response.group_id +'"]').first().prop('checked', true);
             var $textActual =  $('.ms-choice span')
             $textActual.text(response.group_name)
            $('#formAddGroup').modal('hide');
        });
    });
});