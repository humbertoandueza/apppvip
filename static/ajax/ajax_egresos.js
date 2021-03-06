var tables= $('#postsTable').DataTable({
    "language": {
        "url": "/static/datatables/spanish.json"
        },
    responsive: true,
    ordering: true,
    responsive: true,
    scrollY: 380,
    scrollCollapse: true,

    "iDisplayLength": 10,
    dom: 'frti<"right"p>'
    });
$(document).ready(function(){
    listado_s()
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
        $('#id_monto').addClass('number')
        
        }
    });
    });

});

//Ajax para crear el Egreso
$("#modal1").on("submit", ".js-book-create-form", function (e) {

    var form = $(this);
    var data = $("#form :input").serializeArray();
    if($('#id_monto').val()<1){
        $('#error').html('<p style="color:red; margin-left:40px;">Introduzca un valor valido</p>');
        $( "#id_monto" ).addClass( "invalid" );

        return false;
    }
    if(moment($('#id_fecha').val()) >moment()){
        $('#error').html('<p style="color:red; margin-left:40px;">Fecha invalida: Introduzca una fecha igual o menor a la actual.</p>');
        $( "#id_fecha" ).addClass( "invalid" );

        return false;
    }
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
            Materialize.toast('Egreso Registrado', 3000, 'rounded')
            listado_s()
            capital();
            cerrar_modal();  // <-- This is just a placeholder for now for testing
        }
        else {
            $("#modal1 .modal-content").html(data.html_form);
            $("#error").html("<p style='color:red;' class='center'>"+data.error+"</p>");
            console.log(data.error);

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
    $('#modal1 .modal-content').html(loader);
    $('.modal-full').css("display", "block");
    $('.modal-full').css("z-index", "1003");
}

//modals personalizados
function cerrar_modal(){
    $('.modal-full').css("display", "none");
    $('#modal1 .modal-content').html(loader);
}
function ver(numero){
    mostrar_modal();
    var url = window.location;
    console.log(url)
     /*
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
        */
}
function listado_s(){
    $.ajax({
        url : url_list,
        type:'GET',
        success:function(data){
            if (data.length>0) {
                actualizar_data(data)
                $('.impr').css('display','block');
            }else{
                $('.impr').css('display','none');
            }


    }
    })
}
function actualizar_data(data){
    count = 0
    count1 = 0
    tables.clear().draw();
    for(var i = 0;i<data.length;i++){
        datos = data[i]
        var row1 = '<a class="btn btn-primary js-borrar" onclick="ver('+datos.pk+')"><i class="mdi-image-remove-red-eye"></i></a>'
        var row = [count+=1,datos.fields.fecha,datos.fields.monto,datos.fields.descripcion,datos.fields.concepto]
        tables.row.add(row).draw().node();
    }
}