$(document).ready(function(){
    $('select').material_select();
    });

    //ajax para obtener el formulario
 $(function () {

    $(".modal-full-screen").click(function () {
        mostrar_modal();
    $.ajax({
        url: url_crear,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
        $("#modal1 .modal-content").html(data.html_form);
        }
    });
    });

});

//Ajax para crear el miembro
$("#modal2").on("submit", ".js-book-create-form", function (e) {
    var form = $(this);
    var datos = $("#form :input").serializeArray();
    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Actividad Registrada', 3000, 'rounded')
            $('#calendar').fullCalendar('renderEvent', {
                id: data.id,
                title: data.title,
                start: data.start,
                descripcion:data.descripcion,
                lugar:data.lugar,
                estatus:'Por Realizar',
                color : '#00B0F0',
                allDay: false
              });
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal2 .modal-content").html(data.html_form);
            var error = data.error.split(',');
            for(var i = 0;i < error.length; i+=1){
                $('#error').append('<p style="color:red;">'+error[i]+'</p>');
                console.log(error[i]);
            }

        }
    }
    });
    return false;
});

//Ajax para obtener form Actualizar
function actualizar(numero){
    mostrar_modal();
    //$('#modal1 .modal-content').html(numero);

    var btn = $('.js-update');
     $(function () {
        var url = window.location;
        $.ajax({
        url: url+"actualizar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal2 .modal-content").html(data.html_form);
        }
        });
    });
}
//Ajax para Actualizar
$("#modal2").on("submit", ".js-book-update-form", function (e) {
    
    var form = $(this);
    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Estatus Actualizado', 3000, 'rounded');
            if(data.create){
                $('#calendar').fullCalendar('renderEvent', {
                    id: data.id,
                    title: data.title,
                    start: data.start,
                    descripcion:data.descripcion,
                    lugar:data.lugar,
                    estatus:data.estatus,
                    color : data.color,
                    allDay: false
                  });
            }else{
                evento.color = data.color,
                evento.estatus = data.estatus,
                evento.start = data.start,
                $('#calendar').fullCalendar('updateEvent', evento);
            }

            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal2 .modal-content").html(data.html_form);
        }
    }
    });
    return false;
});

//Ajax para obtener los datos a Borrar
function borrar(numero){
    mostrar_modal();
    //$('#modal1 .modal-content').html(numero);

    var btn = $('.js-borrar');
     $(function () {
        var url = window.location;
        $.ajax({
        url: url+"borrar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal2 .modal-content").html(data.html_form);
        }
        });
    });
}

//Ajax para borrar
$("#modal2").on("submit", ".js-book-borrar-form", function (e) {
            
    var form = $(this);
    $.ajax({
    url: form.attr("action"),
    type: 'get',
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Miembro Eliminado', 3000, 'rounded')
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal2 .modal-content").html(data.html_form);
        }
    }
    });
    return false;
});
var loader = `
<div class="preloader-wrapper active" style="margin-top:5%;">
    <div class="spinner-layer spinner-blue-only">
        <div class="circle-clipper left">
        <div class="circle"></div>
        </div>
        <div class="gap-patch">
        <div class="circle"></div>
        </div>
        <div class="circle-clipper right">
        <div class="circle"></div>
        </div>
    </div>
</div>
`;


function mostrar_modal(){
    $('#modal2 .modal-content').html(loader);
    $('.modal-full').css("display", "block");
    $('.modal-full').css("z-index", "1003");
}

//modals personalizados
function cerrar_modal(){
    $('#cargar').css("display","none");
    $('#gallery').css("display","none");
    $("#gallery").html("");

    $('#cerrar').css("display","none");
    $('.modal-full').css("display", "none");
    $('#modal2 .modal-content').html(loader);
}