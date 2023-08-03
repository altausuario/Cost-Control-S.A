function formatCurrency(number) {
    return parseFloat(number).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
}
function get_Calcular(){
    var amount = $('#id_amount').val()
    var iva = $('#id_iva').val()
        if(amount==0 && iva==0){
            $('#id_totaliva').val(0.00)
            $('#total_required').val(0.00)
        }
        if(iva > 0){
        var totalIva = parseFloat((amount*iva)/100)
        var total = parseFloat(amount) + parseFloat(totalIva)
        totalIva = parseFloat(totalIva).toFixed(2)
        total = parseFloat(total).toFixed(2)
        $('#id_totaliva').val(formatCurrency(totalIva))
        $('#total_required').val(formatCurrency(total))
        }
        if(iva > 0 && amount == ''){
        var totalIva = parseFloat((amount*iva)/100)
        var total = 0
        totalIva = parseFloat(totalIva).toFixed(2)
        total = parseFloat(total).toFixed(2)
        $('#id_totaliva').val(formatCurrency(totalIva))
        $('#total_required').val(formatCurrency(total))
        }
        if(amount > 0){
        var totalIva = parseFloat((amount*iva)/100)
        var total = parseFloat(amount) + parseFloat(totalIva)
        totalIva = parseFloat(totalIva).toFixed(2)
        total = parseFloat(total).toFixed(2)
        $('#id_totaliva').val(formatCurrency(totalIva))
        $('#total_required').val(formatCurrency(total))
    }
}
$(function(){
    get_Calcular()
    var originalValue = $("#date_joined").val();
    var ivaOriginal = $('#id_iva').val()
    if(ivaOriginal == ''){
        $('#id_iva').val(19)
    }
    if (originalValue == ''){
      var currentDate = new Date();
      var day = formatNumberWithZero(currentDate.getDate());
      var month = formatNumberWithZero(currentDate.getMonth() + 1); // Los meses en JavaScript van de 0 a 11
      var year = currentDate.getFullYear();

      // Mostrar la fecha en el formato deseado
      originalValue = year + "-" + month + "-" + day;
    }
$('input[required], textarea[required], select[required]').filter(function() {
    return $(this).prev('label').length > 0;
}).each(function() {
//    $(this).prev('label').text($(this).prev('label').text() + ' *');
    $(this).prev('label').append('<b style="color:red; padding-left: 5px;"> *</b>');
});
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
 $("#date_joined").val(originalValue);
})