function get_Calcular(){
    var amount = $('#id_amount').val()
    var iva = $('#id_iva').val()
        if(amount==0 && iva==0){
            $('#id_totaliva').val(0.00)
            $('#id_total').val(0.00)
        }
        if(iva > 0){
        var totalIva = parseFloat((amount*iva)/100)
        var total = parseFloat(amount) + parseFloat(totalIva)
        $('#id_totaliva').val(parseFloat(totalIva).toFixed(2))
        $('#id_total').val(parseFloat(total).toFixed(2))
        }
        if(amount > 0){
        var totalIva = parseFloat((amount*iva)/100)
        var total = parseFloat(amount) + parseFloat(totalIva)
        $('#id_totaliva').val(parseFloat(totalIva).toFixed(2))
        $('#id_total').val(parseFloat(total).toFixed(2))
    }
}
$(function(){
$('input[required], textarea[required], select[required]').filter(function() {
    return $(this).prev('label').length > 0;
}).each(function() {
//    $(this).prev('label').text($(this).prev('label').text() + ' *');
    $(this).prev('label').append('<b style="color:red; padding-left: 5px;"> *</b>');
});
get_Calcular()
$('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
//        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
});
$("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
//        decimals: 2,
//        boostat: 5,
//        maxboostedstep: 10,
        postfix: '%'
    }).on('change',function(){
        get_Calcular()
    }).val(19);
$('#id_amount').on('input', function() {
    get_Calcular()
})
$('#id_iva').on('input', function() {
    get_Calcular()
})
})