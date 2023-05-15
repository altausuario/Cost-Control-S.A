$(function(){
    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();
    var output = d.getFullYear() + '-' + (month<10 ? '0' : '') + month + '-' + (day<10 ? '0' : '') + day;

    var now =  new Date().toLocaleTimeString('es-EU');
    console.log(now)
    console.log(d)
    $('#data_joined').val(output);
});