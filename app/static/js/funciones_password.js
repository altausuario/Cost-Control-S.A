$(function() {
  $('#ckeckpassword').on('change', function() {
    var inputPassword = $("#id_password");
    var labelPassword = $("#ckeckpasswordlabel")
    var inputPasswordType = inputPassword.attr("type");
    if (inputPasswordType === 'password') {
      inputPassword.attr("type", "text");
      labelPassword.text("Ocultar contraseña")
    } else {
      inputPassword.attr("type", "password");
      labelPassword.text("Mostrar contraseña")
    }
  });
  $('#ckeckpasswordchange').on('change', function() {
    var input_old_password = $("#id_old_password");
    var input_new_password1 = $("#id_new_password1");
    var input_new_password2 = $("#id_new_password2");
    var labelPassword = $("#ckeckpasswordlabel")
    var inputPasswordType = input_old_password.attr("type");
    if (inputPasswordType === 'password') {
      input_old_password.attr("type", "text");
      input_new_password1.attr("type", "text");
      input_new_password2.attr("type", "text");
      labelPassword.text("Ocultar contraseña")
    } else {
      input_old_password.attr("type", "password");
      input_new_password1.attr("type", "password");
      input_new_password2.attr("type", "password");
      labelPassword.text("Mostrar contraseña")
    }
  });

  $('#ckeckpasswordrecover').on('change', function(){
    var recoverinputpassword = $('#id_password')
    var recoverinputconfirmPassword = $('#id_confirmPassword')
    var labelPassword = $("#ckeckpasswordlabel")
    var typepassword = recoverinputpassword.attr("type");
    if (typepassword === 'password'){
        recoverinputpassword.attr("type", "text");
        recoverinputconfirmPassword.attr("type", "text");
        labelPassword.text("Ocultar contraseña")
    }else{
        recoverinputpassword.attr("type", "password");
        recoverinputconfirmPassword.attr("type", "password");
        labelPassword.text("Mostrar contraseña")
    }
  })

  $('#buttonpassword').on('click', function(){
    var inputPassword = $("#id_password");
    var textButtonI = $('#iButtonPassword')

    var inputPasswordType = inputPassword.attr("type");
    if (inputPasswordType === 'password') {
        inputPassword.attr("type", "text");
        textButtonI.removeClass("fa-eye");
        textButtonI.addClass("fa-eye-slash");
    } else {
        inputPassword.attr("type", "password");
        textButtonI.removeClass("fa-eye-slash");
        textButtonI.addClass("fa-eye");
    }
  })
});