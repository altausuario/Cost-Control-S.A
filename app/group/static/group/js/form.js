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
});
