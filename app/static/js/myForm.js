$(function(){
$('input[required], textarea[required], select[required]').filter(function() {
    return $(this).prev('label').length > 0; // Solo los inputs que tienen un label anterior
}).each(function() {
//    $(this).prev('label').text($(this).prev('label').text() + ' *');
    $(this).prev('label').append('<b style="color:red; padding-left: 5px;"> *</b>');
});
})