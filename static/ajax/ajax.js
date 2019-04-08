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
$("#modal1").on("submit", ".js-book-create-form", function (e) {
    
    var form = $(this);
    var data = $("#form :input").serializeArray();
    for (var i = 0; i < data.length; i+=1) {
        if(data[i].name == "cedula"){
            //console.log('cedula: ', data[i].value.length);
            if(data[i].value.length <=6 || data[i].value.length >8 ){
                $( "#id_cedula" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">La cedula no es correcta</p>');
                //alert('La cedula no cumple con lo requerido');
                return false;                
            }
        } 
    }
    formulario = form.serialize()+'&'+$.param({ 'url': "http://google.co.ve" })
    console.log(formulario);
    $.ajax({
    url: form.attr("action"),
    data: formulario,
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        console.log(data);
        if (data.form_is_valid) {
            Materialize.toast('Miembro Registrado', 3000, 'rounded')
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal1 .modal-content").html(data.html_form);
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
        console.log(url);
        $.ajax({
        url: url+"actualizar/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            $("#modal1 .modal-content").html(data.html_form);
        }
        });
    });
}
//Ajax para Actualizar
$("#modal1").on("submit", ".js-book-update-form", function (e) {
    
    var form = $(this);
    var data = $("#form :input").serializeArray();
    for (var i = 0; i < data.length; i+=1) {
        if(data[i].name == "cedula"){
            //console.log('cedula: ', data[i].value.length);
            if(data[i].value.length <=6 || data[i].value.length >8 ){
                $( "#id_cedula" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">La cedula no es correcta</p>');
                //alert('La cedula no cumple con lo requerido');
                return false;                
            }
        } 
    }

    $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
        if (data.form_is_valid) {
            Materialize.toast('Miembro Actualizado', 3000, 'rounded')
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
        $("#modal1 .modal-content").html(data.html_form);
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
            $("#modal1 .modal-content").html(data.html_form);
        }
        });
    });
}

//Ajax para borrar
$("#modal1").on("submit", ".js-book-borrar-form", function (e) {
            
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
        $("#modal1 .modal-content").html(data.html_form);
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

function ver(numero){
    mostrar_modal();
    var url = window.location;

    $.ajax({
        url: url+"ver_persona/"+numero,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            var  form = `
                <style>
                table, th, td {
                border-collapse: collapse;
                background-color:#00b0f0;
                color:#fff;
                border-radius:10px;
                }
                th, td {
                padding: 5px;
                border-bottom: 2px solid #fff;

                text-align: center;
                }
                td{
                    border-left: 5px solid #fff;

                    padding:15px;
                }
                td{
                    text-align:left;
                    font-weight:bold;
                }
                </style>
            <div class="row">
                <div class="col m3 offset-m3">
                    <i class="mdi-action-account-circle prefix large left" style="font-size: 190px;"></i>

                </div>
                <div class="col m2" style="padding:0px;">
                <h5 class="left" style="font-size:60px;margin-top:80px;font-weight:bold;">${data.persona.nombre} ${data.persona.apellido}</h5>

                </div>

            </div>
            <div class="row">
                <div class="col col m6 offset-m3 s12">
                <table style="width:100%;margin-bottom:5px;" class="table">
                <tr>
                  <th>Cedula:</th>
                  <td>${data.persona.cedula}</td>
                </tr>
                <tr>
                  <th>Nombre:</th>
                  <td>${data.persona.nombre}</td>
                </tr>
                <tr>
                <th>Apellido:</th>
                  <td>${data.persona.apellido}</td>
                </tr>
                <tr>
                  <th>Telefono:</th>
                  <td>${data.persona.telefono}</td>
                </tr>
                <th>Direcion:</th>
                  <td>${data.persona.direccion}</td>
                </tr>
                <tr>
                <th>Correo:</th>
                  <td>${data.persona.correo}</td>
                </tr>
                <tr>
                <th>Rol:</th>
                  <td>${data.persona.rol}</td>
                </tr>
                <tr>
              </table>
              <button class="center btn btn-primary red" onclick="cerrar_modal();">Salir</button>    
                </div>
            </div>
            `;
            console.log(data);
            $("#modal1 .modal-content").html(form);

            //$("#modal1 .modal-content").append("<p>"+data.persona.cedula+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.nombre+"</p>");
            
            //$("#modal1 .modal-content").append("<p>"+data.persona.apellido+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.telefono+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.direccion+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.rol+"</p>");
            //$("#modal1 .modal-content").append("<p>"+data.persona.correo+"</p>");

        }
        });
}
function mostrar_modal(){
    $('#modal1 .modal-content').html(loader);
    $('.modal-full').css("display", "block");
    $('.modal-full').css("z-index", "1003");
}

//modals personalizados
function cerrar_modal(){
    $('.modal-full').css("display", "none");
    $('#modal1 .modal-content').html(loader);
}