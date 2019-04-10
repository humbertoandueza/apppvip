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
        $('#id_cedula').addClass('number')
        $('#id_telefono').addClass('number')
        $('#id_nombre').addClass('text')
        $('#id_apellido').addClass('text')
        }
    });
    });

});

//Ajax para crear el miembro
$("#modal1").on("submit", ".js-book-create-form", function (e) {
    
    var form = $(this);
    var data = $("#form :input").serializeArray();
    for (var i = 0; i < data.length; i+=1) {
        dato = data[i]
        if(dato.name == "cedula"){
            if(dato.value.length <=6 || dato.value.length >8 ){
                $( "#id_cedula" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">La cedula no es correcta</p>');
                return false;                
            }
        }
        if(dato.name == "nombre"){
            if(dato.value.length <3){
                $( "#id_nombre" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un nombre</p>');
                return false;                
            }
        }
        if(dato.name == "apellido"){
            if(dato.value.length <3){
                $( "#id_apellido" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un apellido</p>');
                return false;                
            }
        }
        if(dato.name == "telefono"){
            if(dato.value.length <11 || dato.value.length >11){
                $( "#id_telefono" ).addClass( "invalid" );
                $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un numero de telefono valido</p>');
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
            $('#id_cedula').addClass('number')
            $('#id_telefono').addClass('number')
            $('#id_nombre').addClass('text')
            $('#id_apellido').addClass('text')
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
                
                color:#000;
                
                }
                th, td {
                padding: 5px;
                border: 2px solid #000;

                text-align: center;
                }
                td{
                    border-left: 5px solid #000;

                    padding:15px;
                }
                td{
                    margin-left:10px;
                    text-align:left;
                    
                }
                </style>
            <div id="imp">
            <div class="row">
                <br><br>
                <img src="/static/assets/img/logo.png" width="150">
                <br><br>

                <div class="col m2 offset-m3">
                    <i class="mdi-action-account-circle prefix large center" style="font-size: 90px;"></i>
                </div>
                <div class="col m6" style="padding:0px;">
                <br>
                <h3 class="left" style="font-weight:bold;margin-left:10px;">${data.persona.nombre} ${data.persona.apellido}</h3>

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
                  <th>Nombres:</th>
                  <td>${data.persona.nombre}</td>
                </tr>
                <tr>
                <th>Apellidos:</th>
                  <td>${data.persona.apellido}</td>
                </tr>
                <tr>
                  <th>Telefono:</th>
                  <td>${data.persona.telefono}</td>
                </tr>
                <th>Dirección:</th>
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
              <br>
              <button  id="salir" class="center btn btn-primary red" onclick="cerrar_modal();">Salir</button>   
              <button  id="impi" class="center btn btn-primary blue" onclick="Imp('${data.persona.nombre}');">Imprimir</button>   
                </div>
            </div>
            </div>
            `;
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
function Imp(nombre){
    $('#imp').css('max-width','1200px')
    $('#imp').css('margin-left','-200px')
    $('#salir').css('display','none')
    $('#impi').css('display','none')
    $('#imp').css('background-color','#fff')
    //$('#imp').css('padding-top','40px')
    //$('#im').css('display','none')
    //$('#sampleTable1_wrapper').css('display','none')
    //$('#info').css('margin-bottom','80px')
    html2canvas(document.querySelector("#imp")).then(canvas => {
    //document.body.appendChild(canvas)
    //$('#impp').append(canvas)
    var pdf = new jsPDF("p", "mm", "a4");
    pdf.addImage(canvas, 'JPG', 0, 0);
    pdf.save(`${nombre}_miembro_reporte.pdf`);
    $('#imp').css('max-width','100%')
    $('#salir').css('display','initial')
    $('#imp').css('margin-left','0px')


    $('#impi').css('display','initial')

    //$('#imp').css('padding-top','-40px')
    //$('#im').css('display','block')
    //$('#sampleTable1_wrapper').css('display','block')
    //$('#info').css('margin-bottom','-80px')

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