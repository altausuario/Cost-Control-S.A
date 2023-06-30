$(document).ready(function() {
  function setIvaInputWidth() {
    var windowWidth = $(window).width();
    var ivaInput = $('#id_iva');

    if (windowWidth < 920) {
      ivaInput.css('width', '30%');
    } else {
      ivaInput.css('width', '60%');
    }
  }
  function setInputWidth() {
    var divWidth = $('#cont').width();
    var input = $('#id_iva');

    if (divWidth < 1200) {
      input.css('width', '3%');
    } else {
      input.css('width', '60%');
    }
  }

  // Llamada inicial para configurar el ancho del input IVA en función del tamaño de la ventana al cargar la página
  setIvaInputWidth();
  setInputWidth();

  // Vuelve a configurar el ancho del input IVA cuando se redimensiona la ventana
  $(window).resize(function() {
    setIvaInputWidth();
    setInputWidth();
  });
});