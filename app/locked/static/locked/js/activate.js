var vents = {
    items: {
        datos:[]
    },
    add: function(item){
        this.items.datos.push(item);
        this.list()
    },
    list: function(){
        var first_name = '';
        var last_name = '';
        var username = '';
        var password = '';
        var date_joined = '';
        var email = '';
        var image = '';
        $.each(this.items.datos, function(pos, dict){
            first_name = dict.first_name
            last_name = dict.last_name
            username = dict.username
            password = dict.password
            date_joined = dict.date_joined
            email = dict.email
            image = dict.image
        })
        $('input[name="first_name"]').val(first_name)
        $('input[name="last_name"]').val(last_name)
        $('input[name="username"]').val(username)
        $('input[name="password"]').val(password)
        $('input[name="date_joined"]').val(date_joined)
        $('input[name="email"]').val(email)
        $('#img').attr("src", image);
    }
  }


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
           $("#buscar").removeAttr("style");
          $(this).val('');
      }
    });

 $('form').on('submit', function(e){
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        nombre = $('input[name="first_name"]').val()
        apellidos = $('input[name="last_name"]').val()
        username = $('input[name="username"]').val()
        password = $('input[name="password"]').val()
        fecha = $('input[name="date_joined"]').val()
        email = $('input[name="email"]').val()

        if(nombre == '' && apellidos == '' && username == '' && password == '' && fecha == '' && email == ''){
            Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Se debe selecionar un usuario',
            })
            $("#buscar").css("border-color", "red");
        }else{
            alert_activate_user(window.location.pathname,'Notificacion', '¿Estas seguro de habilitar al usuario?', parameters, function(){

            });
            }
    });
});