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
            $('#formAddGroup').modal('hide');
        });
    });
});